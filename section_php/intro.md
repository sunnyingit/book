## php 微服务化架构

目前，我们在使用swoole + thrift + laravel 实现微服务化， 使用swoole 作为TCP服务器，使用laravel的基础组件构建业务框架代码，便于编写业务， 微服务化之间的通信使用thrift 协议。

在不考虑服务治理，服务监控，配置中心化的问题，就只针对业务框架，有几点需要我们考虑：

- swoole如何与laravel结合使用, swoole需要注册回调函数去处理对应的事件，要求在项目启动过程中就必须向swoole注入对应的回调函数

- laravel的核心组件比如router, request, response, appliaction 都是基于HTTP协议编写的，但是我们的微服务化是基于thrift协议通信的，所以我们需要对laravel的核心组件进行改造，便于支持thrift协议

- thrift协议解析， 因为我们需要从thrift返回值里面抽象出request，response对象，所以我们不能简单的继承thrift生成的代码进行开发，我们需要解析thrift文件，动态去查找执行的类。

- swoole和原生的php一次请求销毁所有内存的不同在于swoole是常驻内存，这样laravel只需要初始化一次，可改善laravel的性能，但需要注意销毁对象不必要的对象

- 扩展thrift协议，支持request_id, seq_id, version等信息的传递。


## 重新打造一套微服务化框架

要解决以上几个问题，我们需要打造一套框架，能同时利用swoole的性能和laravel的组件，同时兼容thrift协议。

我们使用composer 利用了laravel的基础组件构建了一套自己的框架。 在这个过程中，阅读了大量的laravel基础组件的代码，受益良多。我在想，为什么觉得laravel很难使用

新手看了laravel的手册或者源码，依然觉得很困惑，为什么？是他们没有对laravel的组件有个整体认识，总感觉在盲人摸象。

这里的重点是 `数据模型`，比如容器`container`，那我们就要学习laravel是怎么抽象出容器这个数据模型的，摸清了这个`数据模型`后，使用起来会得心应手的活。

最重要的是学习laravel的设计思想，学laravel的命名，学laravel的代码规范， 学习laravel解决问题的思路


















