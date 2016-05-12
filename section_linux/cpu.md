# CPU性能监控

[转载神文](http://www.vpsee.com/2009/11/linux-system-performance-monitoring-cpu/)

### CPU性能理解
要理解CPU的性能，就必须理解CPU做了哪些事情

工作时间：CPU就是一个执行者，他维护着一个可运行队列，每时每刻都会有进程(线程)在上面运行，进程的运行时间就是CPU的工作时间

中断时间(Interrupt Number)：CPU需要知道什么时间运行什么进程，这需要CPU和进程调度器协商沟通，进程调度器管理CPU, 告诉CPU到底运行哪个进程，这花费的时间就是中断时间， 同时，正常情况下，线程要么在睡眠状态（blocked 正在等待 IO，调用sleep函数可以让进程睡眠，让出cpu）要么在可运行状态

中断优先级(硬件中断>内核中断>用户中断)

上下文切换时间(context switch)：A进程运行时间已经到了，现在CPU需要切换到B进程，这个时间就是上下文切换时间

利用率：
us (user cpu time)：用户进程占用CPU花费时间的百分比
sy(system cpu time)：内核, 中断占用CPU花费时间百分比

CPU的性能指标：利用率，上下文切换次数，中断测试，运行队列来监控cpu性能

### vmstat
vmstat 是个查看系统整体性能的小工具，小巧、即使在很 heavy 的情况下也运行良好，并且可以用时间间隔采集得到连续的性能数据
```
2: 表示每隔2s
[li.sun@d114-app-06 ~]$ vmstat 2
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 0  0      0 16963800   3440 8607132    0    0     5     8    8    4  2  0 98  0  0
 0  0      0 16964188   3440 8607132    0    0     0     4 2601 2123  0  0 100  0  0
 0  0      0 16964372   3440 8607132    0    0     0     2 3695 3146  1  0 99  0  0

 r (running): 可运行的队列
 b (blocked): 阻塞的进程数，过多说明系统IO速度有问题
 in (interrupt number): 中断的次数，中的次数越多说明cpu不停的需要请求资源
 cs(contenxt switch): 上下文切换的次数 上下文过多，说明进程数量过多
 us(user cpu time): 用户进程的cpu利用率
 sy(system cpu time): 内核进程的cpu利用率
 wa(io wait): 当可运行的进程因为等待io而处于blokced状态，这个时间所占的比例
 id(idle): cpu完全空闲的时间的比例
```

### 具体实例分析
系统的某个时间段，cpu的利用率很高，排查cpu时间到底花在哪里了
```
$ vmstat 1
procs -----------memory---------- ---swap-- -----io---- --system-- -----cpu------
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 4  0    140 2915476 341288 3951700  0    0     0     0 1057  523 19 81  0  0  0
 4  0    140 2915724 341296 3951700  0    0     0     0 1048  546 19 81  0  0  0
 4  0    140 2915848 341296 3951700  0    0     0     0 1044  514 18 82  0  0  0
 4  0    140 2915848 341296 3951700  0    0     0    24 1044  564 20 80  0  0  0
 4  0    140 2915848 341296 3951700  0    0     0     0 1060  546 18 82  0  0  0
```
interrupts（in）非常高，context switch（cs）比较低，说明这个 CPU 一直在不停的请求资源；
system time（sy）一直保持在 80％ 以上，而且上下文切换较低（cs），说明某个进程可能一直霸占着 CPU（不断请求资源）；
run queue（r）刚好在4个

```
vmstat 1
procs -----------memory---------- ---swap-- -----io---- --system-- -----cpu------
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
14  0    140 2904316 341912 3952308  0    0     0   460 1106 9593 36 64  1  0  0
17  0    140 2903492 341912 3951780  0    0     0     0 1037 9614 35 65  1  0  0
20  0    140 2902016 341912 3952000  0    0     0     0 1046 9739 35 64  1  0  0
17  0    140 2903904 341912 3951888  0    0     0    76 1044 9879 37 63  0  0  0
16  0    140 2904580 341912 3952108  0    0     0     0 1055 9808 34 65  1  0  0
```
上面的数据可以看出几点：

context switch（cs）比 interrupts（in）要高得多，说明内核不得不来回切换进程；
进一步观察发现 system time（sy）很高而 user time（us）很低，而且加上高频度的上下文切换（cs），说明正在运行的应用程序调用了大量的系统调用（system call）；
run queue（r）在14个线程以上，按照这个测试机器的硬件配置（四核），应该保持在12个以内

### mpstat

mpstat 和 vmstat 类似，不同的是 mpstat 可以输出多个处理器的数据，下面的输出显示 CPU1 和 CPU2 基本上没有派上用场，系统有足够的能力处理更多的任务。

```
Linux 3.10.0-123.el7.x86_64 (d114-app-06)   05/12/2016  _x86_64_    (24 CPU)

02:55:54 PM  CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle
02:55:54 PM  all    2.10    0.04    0.19    0.01    0.00    0.02    0.00    0.00    0.00   97.63
02:55:54 PM    0    3.67    0.04    0.37    0.01    0.00    0.06    0.00    0.00    0.00   95.85

%user      在internal时间段里，用户态的CPU时间(%)，不包含nice值为负进程  (usr/total)*100
%nice      在internal时间段里，nice值为负进程的CPU时间(%)   (nice/total)*100
%sys       在internal时间段里，内核时间(%)       (system/total)*100
%iowait    在internal时间段里，硬盘IO等待时间(%) (iowait/total)*100
%irq       在internal时间段里，硬中断时间(%)     (irq/total)*100
%soft      在internal时间段里，软中断时间(%)     (softirq/total)*100
%idle      在internal时间段里，CPU除去等待磁盘IO操作外的因为任何原因而空闲的时间闲置时间(%) (idle/total)*100

```

### ps
如果发现某个进程特别占有cpu，查看某个进程的cpu利用情况
```
li.sun@xg-ppe-web:~$ ps aux | grep hhvm
www-data  4113  0.3  2.9 1033992 238096 ?      Ssl  14:32   0:06 /usr/bin/hhvm --config /etc/hhvm/php.ini

USER: 执行进程的用户
PID: 进程ID
%CPU: CPU的利用率
%MEMER: 内存的使用率
VSZ: 虚拟内存的使用情况(kb)
RSS: 该 process 占用的固定的内存量 (Kbytes)
TTY ：该 process 是在那个终端机上面运作
STAT：该程序目前的状态，主要的状态有
    R ：该程序目前正在运作，或者是可被运作
    S ：该程序目前正在睡眠当中 (可说是 idle 状态)，但可被某些讯号 (signal) 唤醒。
    T ：该程序目前正在侦测或者是停止了
    Z ：该程序应该已经终止，但是其父程序却无法正常的终止他，造成 zombie (疆尸) 程序的状态
START：该 process 被触发启动的时间
TIME ：该 process 实际使用 CPU 运作的时间
COMMAND：该程序的实际指令
```
