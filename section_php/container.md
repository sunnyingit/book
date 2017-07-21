# 容器

## 为什么需要容器

容器主要是为了实现**控制反转**。 什么是控制反转呢，简单来说，把操控的对象的调用权交给容器，通过容器来实现对象的管理。下面的例子，Cache对象不用操作Redis对象，由Container对象负责Redis对象的生成。

可是为什么要控制反转呢，主要是为了减少**类的耦合**， 这样Cache对象不需要依赖Redis对象， 如果有一天不使用Redis作为缓存，那也不需要改Cache的代码。

```php

# 不反转的例子 Cache类依赖Redis
class Cache {
    public function __construct()
    {
        $this->store = new Redis();
    }
}

# 反转使用容器, 由容器实例化对应的类，把控制权给了容器
class Cache {
    public function __construct(Container $container)
    {
        $this->$container = $container;

        $this->store = $this->container->make('cache');
    }
}
```

可为什么`make('cache')` 可以得到Redis的实例化对象呢，那是因为我们之前已经先向容器里面**绑定**Redis对象，伪代码：

```php

$container->bind('cache', function($container) {
    return new Redis($container);
});
```


这里，我们可以把container理解成储存东西的器具，就像使用存钱罐一样使用它，先往存钱罐里面存钱，你可以储存硬币，纸币，在需要的时候再把它拿出来，使用步骤可以总结为2点:

- **先往容器里绑定东西**

- **再向容器拿绑定过的东西**

记住了，这两句话就是容器最核心的本质, 牢记于心。

## 可以往容器里面bind什么类型的东西

现在有三个问题

1. 怎么绑定呢

通过`abstract => value`方式赋值绑定， 然后通过abstract 去查找绑定的value.

2. 可以支持绑定哪些类型

简单来说，value主要有如下几种常用类型:

- array instances, 实例化后的对象 instance

- array bindings,  匿名函数  binding

- array methodBindings, 绑定一个method


3. 有哪些函数可以实现绑定

- instance

- bind

- bindMethod

- bindIf

- singleton


```php
class Container {

    # 判定一个实例化的对象
    public function instance($abstract, $instance)
    {
        $this->instances[$abstract] = $instance;
    }

    # 绑定一个匿名函数，如果$concrete传入的是一个类名，容器会自动构建一个匿名函数，这个函数执行后返回类实例化对象
    public function bind($abstract, $concrete, $shared = false)
    {
        # 加入shared是为了判断生成的对象是不是单例的。
        $this->bindings[$abstract] = compact('concrete', 'shared');
    }

    # 绑定一个对象方法
    public function bindMethod($method, $callback)
    {
        $this->methodbindings[$method] = $callback;
    }

    # 只在没有绑定的情况下绑定
    public function bindIf($abstract, $concrete = null, $shared = false)
    {
        if (! $this->bound($abstract)) {
            $this->bind($abstract, $concrete, $shared);
        }
    }

    #  共享绑定，生成的对象是单例的
    public function singleton($abstract, $concrete = null)
    {
        $this->bind($abstract, $concrete, true);
    }


}
```


## bind之后怎么取东西
现在有一个问题

1. bind完了之后，我们就需要通过abstract从容器里面取数据对吧，那怎么去取呢

laravel提供了`resolve`方法，其核心的思路是这样的：

1，首先判断instances中是否有abstract, 有的话，直接返回。没有接着往下看。

2，其次，判断bindings里面有没有abstract，有的话拿到注册的匿名函数， 并执行匿名函数。

3，最后 注意啦，第三步很重要，前两步都没有找到的话，那laravel会把abstract当作一个类名，然后通过**反射** 构建这个类名的实例化对象。

**所以不需要事先绑定一个类， 通过Make函数可以直接实例化类** 当然需要可自动加载这个类。

伪代码：

```php
# resolve 是支持传递参数的
protected function resolve($abstract, $parameters = [])
{
   # 先查找instances
   if (isset($this->instances[$abstract]) && ! $needsContextualBuild) {
        return $this->instances[$abstract];
    }

    # 把参数保存起来
    $this->with[] = $parameters;

    # 在查找bindings
    if (isset($this->bindings[$abstract])) {
        $concrete = $this->bindings[$abstract]['concrete'];
    }

    # 如果在bindings找到了一个匿名函数，则直接执行这个函数
    if ($concrete instanceof Closure) {
        return $concrete($this, end($this->with));
    }

    # 然后反射abstarct
    $reflector = new ReflectionClass($abstract);

    # 标记已经resolved过了
    $this->resolved[$abstract] = true;

    # 把参数吐出来
    array_pop($this->with);

    return $reflector->newInstanceArgs($instances);
}
```

laravel 提供了'make' 方法去获取bind的内容

```php

    # 注意 make 是不能传递参数的
    public function make($abstract)
    {
        return $this->resolve($abstract);
    }

```

还有一个问题，怎么触发bind的methodBindings类型呢, 通过callMethodBinding就可以啦，代码如下:


```php

public function callMethodBinding($method, $instance)
{
    # 调用过程中，需要传递一个类的实例和container, 由调用方式可知这个方法可访问intance，可以操作管理intance
    # 如果你需要一个方法管理一个类可以使用这个方法
    return call_user_func($this->methodBindings[$method], $instance, $this);
}

```

### 更简洁的访问放方式

到目前为了，容器的基本架构已经很明显啦，大家都可以随心所欲的去bind和make了，
但是还没有完，每次取一个东西都要make一下太麻烦了，于是laravel实现了arrayAccess的机制

请看伪代码：


```php
# 实现了ArrayAccess啦
class Container implements ArrayAccess, ContainerContract
{
    public function offsetGet($key)
    {
        return $this->make($key);
    }

    public function offsetSet($key, $value)
    {
        $this->bind($key, $value instanceof Closure ? $value : function () use ($value) {
            return $value;
        });
    }
}

# 于是我们存和取姿势可以这样:
存一个东西，$container['cache'] = new Redis();
取一个东西，$redis = $container['cache']

存一个东西： $container['key'] = value
取一个东西： $value = $container['key']
```

使用心得:

> 一般在使用过程中，使用bind，instance, singleton去绑定value，使用arrayacces的方式去获取绑定的value。通过make去自动构建一个类的实例.

## 还可以什么特性用的比较多

还有很多哦，接着玩下看

### callbacks 回调函数

在开始resolve, revolve之后，重新rebound这些时刻可以触发回调函数，回调函数有全局的，也可以是某一个abstract的特定的回调函数

```php

    # 重新bind的时候触发的函数
    protected $reboundCallbacks = [];

    protected $globalResolvingCallbacks = [];

    protected $globalAfterResolvingCallbacks = [];

    protected $resolvingCallbacks = [];

    protected $afterResolvingCallbacks = [];

````


自行查看查看对应的代码

### aliases 别名

```php

    public function alias($abstract, $alias)
    {
        $this->aliases[$alias] = $abstract;

        # 看这里，可以给一个abstract 设置多个别名哦
        $this->abstractAliases[$abstract][] = $alias;
    }

```

别名逻辑很简单，可是为什么要有别名的呢, 只是为了做一个精简的abstract么，我觉得不是，这个应该和契约编程有关系

```php

# 使用别名之后，如果其他类需要使用到Dispatcher，那么都统一通过DispatcherContract::class 拿，这样大家都遵从DispatcherContract定义的契约
$this->app->alias(
    Dispatcher::class, DispatcherContract::class
);

$this->app->alias(
    Dispatcher::class, QueueingDispatcherContract::class
);

```


### extend: 修改容器里面已经bind的abstract的value

这个函数类似于python的装饰器，可以修饰instance对象，第二个参数是一个匿名函数，
匿名函数的第一个参数是需要修饰的instance对象，第二个参数是container

```php

    public function extend($abstract, Closure $closure)
    {
        $abstract = $this->getAlias($abstract);

        if (isset($this->instances[$abstract])) {
            $this->instances[$abstract] = $closure($this->instances[$abstract], $this);

            $this->rebound($abstract);
        } else {
            $this->extenders[$abstract][] = $closure;

            if ($this->resolved($abstract)) {
                $this->rebound($abstract);
            }
        }
    }

```


### 容器最复杂是保存类的上下文

简单来说，是make 反射一个类的时候，如果这个类的构造参数之一是一个其他类的实例化对象，那必须得先实例化其他的类，这个就很复杂啦，幸好用的不多，有兴趣可以自行阅读。



好🌶，该说的基本上说完了，现在你会使用容器了吗，bind and make !









