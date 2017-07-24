#  ServiceProvider  服务提供者

## 为什么需要serviceProvider

`serviceProvider`可以分成两部分理解:

什么是`service`?

说白了 服务就是一个类，这个类可以提供一些方法完成某件事情， 在laravel中内置的服务有日志，异常，缓存，队列，数据库等, 我们可以**定义任意一个类作为一个服务**


什么是`provider`?

既然服务是一个类，就需要实例化这个类并把类注册到容器里面

provider就是实现这个过程的机制，在laravel中服务的概念很重要，其核心思想就是模块化，类与类之间实现解耦。


## serviceProvider 实现逻辑

容器里面讲到，可以通过singleton函数把一个类bind到容器中:

```php

use Illuminate\Support\ServiceProvider;

class ProfilerServiceProvider extends ServiceProvider
{
    protected $defer = true;

    # 定义一个register方法，这个方法执行后把Profiler绑定到容器中
    public function register()
    {
        $this->app->singleton('profiler', function ($app) {
            return new Profiler($app['curl']);
        });
    }

    public function provides()
    {
        return array('profiler');
    }
}

```

现在的问题是什么时候实例化`ProfilerServiceProvider` 并执行`register`方法

答案是: `container`容器初始化的时候，实例化类并调用register方法。
核心逻辑如下：

```php

class Container
{
    public function registerConfiguredProviders()
    {
        $providers = $this->config['app.providers'];

        foreach($providers as $provder) {

            $this->register($provider);
        }
    }

    public function register($provider, $options = [], $force = false)
    {
        # 如果已经注册了，则直接返回不需要重新注册
        if (($registered = $this->getProvider($provider)) && ! $force) {
            return $registered;
        }

        # 这里就是实例化serviceProvider，注意把this传递过去啦。
        if (! $provider instanceof ServiceProvider) {
            $provider = new $provider($this);
        }

        # 调用register方法，register方法实现了服务注册
        if (method_exists($provider, 'register')) {
            $provider->register();
        }


        # 标记服务已经注册啦，别在重新注册
        $this->markAsRegistered($provider);

        # 服务注册后，可以调用servicePorvider的boot函数做一些初始化工作
        if ($this->booted) {
            $this->bootProvider($provider);
        }
    }


}

```

到这里，服务注册的基本逻辑就完成了，上面的代码只是为了说明laravel的核心流程

但并不是laravel真正的代码，实际上，上面的流程 在`ProviderRepository`中实现, 代码太多我就不贴了。


## 服务注册的优化

并不是所有的服务，在laravel启动的时候都需要注册到容器里面，理想的做法是，当用到服务时候，再把服务注册到容器里面去，实现"延迟"注册，可以设当提升laravel的性能。

这样讲，就是需要`serviceProvider`有一个属性，去表示是不是“延迟注册”

```php
    # 使用$defer 表示是否是延迟注册
    protected $defer = false;

```

如果发现`serviceProvider` 是延迟绑定的话，就把这个类记录到容器的`deferredServices`数组里面。

怎么记录的呢，请查看`addDeferredServices` 方法。下面的代码显示了怎么实现**"用到再实例化"**的逻辑

```php

    # make一个服务的时候，就是用到这个服务
    public function make($abstract)
    {
        $abstract = $this->getAlias($abstract);

        # 如果这个服务是延迟绑定的，需要先register这个服务
        if (isset($this->deferredServices[$abstract])) {

            # 延迟注册这个服务
            $this->loadDeferredProvider($abstract);
        }

        return parent::make($abstract);
    }

    # 延迟注册
    protected function loadDeferredProvider($service)
    {
        $provider = $this->deferredServices[$service];

        if (!isset($this->loadedProviders[$provider])) {
            $this->registerDeferredProvider($provider, $service);
        }
    }

    public function registerDeferredProvider($provider, $service = null)
    {
        if ($service) {
            unset($this->deferredServices[$service]);
        }

        # 调用容器的register方法去注册这个服务
        $this->register($instance = new $provider($this));

        # 注意啦，如果laravel已经启动，服务的boot是不会执行的。
        if (!$this->booted && method_exists($instance, 'boot')) {
            $this->booting(function () use ($instance) {
                $instance->boot();
            });
        }
    }


```


在laravel中, 内置的`providers`都在`config/app.php`文件里面定义的。


## 服务注册再次优化

laravel就是优雅，就是考虑的全面，上面讲到每个serviceProvider都一个属性标示自己是否需要延迟绑定，对吧。


那就意味着，每次laravel启动的时候都需要判断这个服务是不是`defer`,很明显是很耗时的

其实serviceProvider只需要解析一次，怎么做到呢，laravel 使用了service.json文件缓存了serviceProviderd的解析结果。

```php
# 可以查看这个代码, 把解析的结果保存在了manifest中
public function writeManifest($manifest)
{
    if (! is_writable(dirname($this->manifestPath))) {
        throw new Exception('The bootstrap/cache directory must be present and writable.');
    }

    $this->files->put(
        $this->manifestPath, '<?php return '.var_export($manifest, true).';'
    );

    return array_merge(['when' => []], $manifest);
}

```

如果有一天，发现laravel的服务加载有问题了，有可能是因为缓存导致的，那就把`service.json`删除掉就好了。



## swoole 可以更优化

swoole可以常驻内存，这样laravel只需要启动的时候注册好服务，下次请求的时候就不需要在重新实例化啦，世界更美好！
