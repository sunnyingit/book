# Facade (门面)

## 为什么要使用Facade

Facade 提供一个更简洁的方式去访问【在容器注册的对象】的方法。

那"更简洁"的方式是什么呢，是一种静态访问的方式。




```php
# 使用make 去访问注册日志对象的info方法
$container->make('log')->info('message')

# 使用arrayaccess的方式
$container["log"]->info('message')

# 使用Facade访问Logger对象的info方法, 这样就不需要在使用容器了。
Log::info('message');
```

记住了，这就是Facade的本质, 使用静态方式访问一个对象的方法，尽管这个方法不是静态方法。

当然还有一个更大的好处，我会在文章的最后指出来。


## 怎么实现静态访问一个对象的任意方法

抛开Laravel Facade.如果我们自己设计一个"Facade"我们应该怎么做呢.

设想一下，逻辑可能是这样:

访问一个类的静态方法method，但是这个静态方法不存在，于是可能访问到某一个魔术方法，在这个魔术方式呢，实例化了某一个真正的类，通过这个类去访问method。

这样就是实现了最基本的Facade方式。

事实上laravel 也是这样做的。这个魔术方法就是__callStatic().

核心代码如下：

```php
use Illuminate\Support\Facades\Facade;

# laravel中所以的Facade都继承了Facade对象
class LogFacade extends Facade
{
    protected static function getFacadeAccessor()
    {
        return 'log';
    }
}

abstract class Facade
{
    # 这就是所说的静态方法
    public static function __callStatic($method, $args)
    {
        # 获取到一个新的对象, 这就是我们要的实际上要访问的对象
        $instance = static::getFacadeRoot();

        if (! $instance) {
            throw new RuntimeException('A facade root has not been set.');
        }

        # 访问到这个对象的方法
        return $instance->$method(...$args);
    }
}

```

于是我们就可以这样访问对象:

```php

LogFacade::info('message')
```

但是注意啦，`LogFacade::info('message')` 和上文提到了`Log::info('message')` 不一样呀， 怎么使用实现【访问一个"Log"对象，实际上是访问的"LogFacade"对象】呢, 答案是 `class_alias()`:

```php
class_alias('Log', 'LogFacade');
```

自此，我们基本了解了Facade的实现机制啦，但还有最后一个疑问:

【访问Log对象，怎么就可以访问到在容器里面注册的log对象的】?


## 如何从Log::info 到 $container['log']->info

再回到__staticMethod方法中，有一个方法`getFacadeRoot`, 这个方法就是用来【获取一个真正的对象]

```php

        public static function getFacadeRoot()
        {
            # getFacadeAccessor 就是获取对象在container注册的下标
            return static::resolveFacadeInstance(static::getFacadeAccessor());
        }

       protected static function resolveFacadeInstance($name)
    {
        if (is_object($name)) {
            return $name;
        }

        if (isset(static::$resolvedInstance[$name])) {
            return static::$resolvedInstance[$name];
        }

        # 核心在这里：$app对象就是container哟，这里就是通过container arrayAccess的方式获取一个注册的对象
        return static::$resolvedInstance[$name] = static::$app[$name];
    }
 ```

容器所有问题基本解答完毕，`static::$app`这个属性是什么使用初始化的呢，实在laravel启动的时候调用了
```php
Facade::setFacadeApplication($this);

public static function setFacadeApplication($app)
{
    static::$app = $app;
}

```


那现在剩下最后一个问题 【什么容器还有什么好处】，答案是【便于单测】


## 容器如何便于单测

比如有下面一段代码
```php
class Event
{
    public function fire($eventName)
    {
        # 这里使用了日志对象记录fire的事件，但是测试fire方法的时候，因为某些原因不能使用log对象，必须mock使用的log对象
        Log::info("event");
    }
}
```

Facace提供了getMockableClass 可以mock一个对象

```php
public function testFire()
{
    # 创建一个mock对象
    Event::shouldReceive('info')->once()->with('event');

}
```

到目前为止了，Facade已经全部讲完了，了解Facade的原理，除了Laravel自定义的Facade以外，也可以给自己定义的类去实现Facade的访问方式。

你应该知道怎么做了吧
