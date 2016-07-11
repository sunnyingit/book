# API 自动熔断机制

### 什么是自动熔断
简单来说，用API的"出错比例"来表示这个API的健康状态，当这个比例值高于设定的阈值，API自动抛出异常，终止服务，这个过程就叫做自动熔断。

API熔断后，可以保护数据库等基础服务不受`unhealth`的API的影响。

大致流程：收集API的相关指标 ----> 判断API是否健康 ----> 通过API的健康状态决定API是否需要自动熔断(恢复)

### 收集API的相关指标
我们在讨论API的健康状态，一定是指在某个时间段内请求的出错次数太多了，那这里就有两个问题我们需要理解：

1，怎么定义"某个时间段"
2，怎么定义"出错太多了"

这里我们使用两个指标去控制:
`metrics_granularity`：时间粒度，设置`metrics_granularity=3`，则是统计这3s内的总出错数。换句话说，`metrics_granularity`就是我们定义的某个时间段。

那么如何定义出错太多了呢，以出错个数来定义吗，好像不行，因为不同的API的请求量是不一样的。

我们考虑使用出错比率来判断，比如同我们统计3s内所有的请求量和3s内出错量，但是仔细不想，还是不行。

例如，我们设定出错率超过45%为`unhealth`, 在`09:14:10 ~ 09:14:13`这3s内是高峰期，访问量是100，出错是20，经判断API为`health`

然后`09:14:13~09:14:16` 访问量是10，出错量是4，那这个时候出错api被设定为`unhealth`, 但这个值很可能是不准确。

更准确的算法是 `20+4 / 10+100`, 也就是需要考虑之前的访问状态。但是我们不能一直累计，这样的话，数据的体量就会太大了，也不利于统计，所以我们设计另一个指标
`metrics_rollingsize`

具体算法如下：
```
设定metrics_rollingsize=5，初始化数据
[0, 0, 0, 0, 0]
每一位代表在metrics_granularity内出错的次数
[0, 0, 0, 0, 11]
每当时间超过metrics_granularity，数据向前偏移一位
[0, 0, 0, 15, 11]

当向前偏移的位超过了5，则去掉最前面的数据，然后在后面补位，保证这个数组的长度总是5位
[11, 123, 99, 11, 0]
```
这种方式类似于一个滑动窗口，每过`metrics_granularity`的时间，窗口向前滑动一格。

参考代码：
```
class RollingNumber(object):

    def __init__(self, rolling_size, granularity=1):
        self.rolling_size = rolling_size
        self.granularity = granularity
        self._values = [0] * rolling_size
        # 上一次偏移的时间
        self._clock_at = time.time()

    def shift(self, length):
        if length <= 0:
            return
        #  如果距离上一次的偏移的时间长度大于了rolling_size，说明
        #  已经过了rolling_size * granularity的时间API没有访问过了
        if length > self.rolling_size:
            self.clear()
        self._values = self._values[length:] + [0] * length

    def shift_on_clock_changes(self):
        pass_time = time.time() - self._clock_at
        length = int(pass_time / self.granularity)
        if length > 0:
            self.shift(length)
            self._clock_at = time.time()

    def incr(self, value=1):
        self.shift_on_clock_changes()
        self._values[-1] += value

    def clear(self):
        self._values = 0 * self.rolling_size

    def value(self):
        self.shift_on_clock_changes()
        # 注意返回的是累加后的数据
        return sum(self._values)

    def __repr__(self):
        return '<rolling number {0} {1}>'.format(self.value(), self._values)

if __name__ == '__main__':
    rolling = RollingNumber(9, 3)
    for i in range(100):
        time.sleep(2)
        rolling.incr(1)
        print repr(rolling)


```
使用一个全局的dict保存每个API访问的结果，参考代码：
```
counters = {}


def incr(key, value=1):

    if key not in counters:
        counters[key] = RollingNumber(ROLLINGSIZE,
                                      rolling_granularity=GRANULARITY)
    counter = counters[key]
    counter.incr(value)


def get(key, default=0):

    if key in counters:
        return counters[key].value()
    return default
```

### API状态检测算法

```
def is_healthy(service, func):
    key_base = '{0}.{1}'.format(service.name, func.func_name)
    key_request = '{0}'.format(key_base)
    key_timeout = '{0}.timeout'.format(key_base)
    key_sys_exc = '{0}.sys_exc'.format(key_base)
    key_unkwn_exc = '{0}.unkwn_exc'.format(key_base)

    requests = counters.get(key_request)
    timeouts = counters.get(key_timeout)
    sys_excs = counters.get(key_sys_exc)
    unkwn_exc = counters.get(key_unkwn_exc)

    # 只有当请求的数量大于某一个值才开始检测API的状态
    if requests > THRESHOLD_REQUEST:
        return ((timeouts / float(requests)) < THRESHOLD_TIMEOUT) and \
            ((sys_excs / float(requests)) < THRESHOLD_SYS_EXC) and \
            ((unkwn_exc / float(requests)) < THRESHOLD_UNKWN_EXC)
    return True
```

### 熔断算法
定义API有三种状态 `lock`, `unlock`, `recovery`

1，如果API的出错率高于某个阈值，API自动熔断, 状态为`lock`

2，如果API已经处于熔断状态，那么在`MIN_RECOVERY_TIME`时间内默认还是处于`lock`

3 如果API处于熔断状态且时间已经超过了`MIN_RECOVERY_TIME`, 而且判断此时API是健康的，则API状态变为`recovery`

3，如果API处于`recovery`状态，如果最新的一次API是`unlock`状态，API会以概率值恢复到状态，如果不是`unlock`，则直接转变为`lock`

4，如果API的`lock`状态持续时间大于`MAX_RECOVERY_TIME`,则直接返回到`unlock`

参考代码：
```
locks = defaultdict(dict)
# 使用服务名和函数名来确定唯一的API
key = '{0}.{1}'.format(service.name, func.func_name)

if key not in locks:
    locks[key]['locked_at'] = 0
    locks[key]['locked_status'] = MODE_UNLOCKED

locked_at = locks[key]['locked_at']
locked_status = locks[key]['locked_status']

# 判断此次API是否健康
result = None

if locked_status == MODE_UNLOCKED:
    if not health_ok_now:
        locks[key]['locked_at'] = time_now
        locks[key]['locked_status'] = MODE_LOCKED
        result = False
    else:
        result = True

elif locked_status == MODE_LOCKED:
     if time.time() - locked_at < MIN_RECOVERY_TIME or not health_ok_now:
        result = False

    locks[key]['locked_status'] = MODE_RECOVER
    result = True

elif locked_status == MODE_RECOVER:
    # 此时API已经是health状态，判断最新一次API请求的结果，如果请求是正常的，则有概率的恢复API，
    if api_latest_state.get(key, False):
    locked_span = time_now - locked_at
    # 如果锁住的时间过长，则直接恢复
    if locked_span >= MAX_RECOVERY_TIME:
        locks[key]['locked_at'] = 0
        locks[key]['locked_status'] = MODE_UNLOCKED
        result = True
        signals.after_api_health_unlocked.send(ctx)
    else:
        if random.random() < float(locked_span) / MAX_RECOVERY_TIME:
            result = True
        else:
            result = False

    else:
    # 最新的一次请求失败了，说明很有可能这个API又坏了，这时在判断是一下整体API的健康状态
    if not healt_ok_now:
       # 重新锁住
       locks[key]['locked_at'] = time.time()
       locks[key]['locked_status'] = MODE_LOCKED
```

### 统计机制
当目前位置，我们知道了然后判断一个API是否健康已经熔断的策略，现在需要关心的问题是，怎么去统计API的`key_timeout key_sys_exc, key_unkwn_exc`等指标的次数

目前我们采用的是使用`blinker`模块的`signal`, 大致流程如下：

```
# signal只罗列一部分，原理都一样的，类似一种回调机制
def register_signals():
    signals.after_api_called.connect(
    on_signal_after_api_called)
signals.after_api_called_ok.connect(
    on_signal_after_api_called_ok)
signals.after_api_called_sys_exc.connect(
    on_signal_after_api_called_sys_exc)

# 统计最后一次API访问的状态
api_latest_state = {}
def on_signal_after_api_called_sys_exc(ctx):
    metrics.incr('{0}.{1}.sys_exc'.format(service, func))
    # 标记状态，因为是sys_exc,所以访问的状态为False
    api_latest_state['{0}.{1}'.format(service,func)] = False


class service(object):
    # 注册相关信号量
    register_signals()

    # 运行的时候触发相关singal
    def run(self, dispatcher, func, args, logger):
        try:
            signals.after_api_called_ok.send(ctx)
         except TException as exc:
         if isinstance(exc, self.system_exc):
            signals.after_api_called_sys_exc.send(ctx)

        finally:
             signals.after_api_called.send(ctx)
```

收工。
