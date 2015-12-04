
#### RESTFUL设计笔记

> 每个URI是一种资源，客户端和服务端之间，传递资源的某种表现，客户端通过四个HTTP动词，对服务器端资源进行操作，GET用来获取资源，POST用来新建资源（也可以用于更新资源），PUT(PATCH)用来更新资源，DELETE用来删除资源。

#####理解资源
资源就是需要提供给客户端的信息载体，例如 order,  user, restaurant

##### 资源的操作
```
get /restaurants 获取餐馆列表信息
post /restaurants 创建餐馆信息
get /restaurants/{restaurant_id} 获取某个特定的餐馆信息
delete /restaurants/{restaurant_id} 删除某个餐馆
patch /restaurants/{restaurant_id} 部分修改餐馆的信息
```
##### 资源的关联操作
比如我需要获取我的订单信息，那么user资源和order资源之间就产生关联
```
get /user/{user_id}/orders  获取我的订单
get /user/{user_id}/orders/{order_id} 获取我的某个订单
post /user/{user_id}/orders/{order_id} 创建我的某个订单
patch /user/{user_id}/orders/{orders_id} 部分修改我的某个订单
```
获取订单与订单的评论
```
get /user/{user_id}/orders/{order_id}/comments/{comment_id} 获取我的订单的评论
post /user/{user_id}/orders/{order_id}/comments 创建一个评论
patch /user/{user_id}/orders/{orders_id}/comments/{comment_id}
```

如何去理解资源于资源之间的关联关系

比如用户和餐厅的关联关系，餐厅不属于任何一个用户，所以访问餐厅列表的URI不能设计为`/users/user_id/restaurants`,  但是如果访问用户对某个餐厅的评价，URI的设计应该是这样`/users/user_id/restaurants/{restauant_id}/comments`
所以，应该在具体的业务中，处理资源之间的关联关系。

再比如根据user_id 去创建一个购物车, URL设计为：`post /users/user_id/carts`，这个设计方案也不太合适，因为购物车不属于用户（在数据库模型中，并没有购物车和用户之间的对应关系），正确的做法`/carts` 把`user_id`当作参数传入。

##### 非CURD操作处理
比如说收藏，计数，交换，检测状态，在github中， 'star'这样设计：
```
put /gists/{gist_id}/star 加星操作
delete /gists/{gist_id}/star 取消加星
get /gitsts/{gist_id}/star 查看是否被star
```
设计原则就是把'star'看做一个子资源进行操作
```
get /users/count 获取用户的总数
get /search/rastaruant 搜索餐馆
post /transaction 把需要交换的内容作为参数传入
```
#####搜索
搜索相关的功能都应该通过参数实现(并且也很容易实现)。

过滤：为所有提供过滤功能的接口提供统一的参数。例如：你想限制get /tickets 的返回结果:只返回那些open状态的ticket–get /tickektsstate=open这里的state就是过滤参数。

排序：和过滤一样，一个好的排序参数应该能够描述排序规则，而不业务相关。复杂的排序规则应该通过组合实现

```
get /search/repositories
```
参数：

| Name      |    Type | Description  |
| :-------- | --------:| :--: |
| q  | string |  The search keywords, as well as any qualifiers.  |
| sort   |   string | The sort field. One of stars, forks, or updated. Default: results are sorted by best match  |
| order  |    string |The sort order if sort parameter is provided. One of asc or desc. Default: desc  |

具体q,  sort，order的设计，参考`https://developer.github.com/v3/search/`

#####请求样例：
`https://api.github.com/search/repositories?q=tetris+language:assembly&sort=stars&order=desc
`
####响应
这部分涉及到restful框架设计，一下是需要注意的几个点
#####字段过滤
比如请求'/restaurants/restaurant_id'获取餐馆信息，但目前的需求是只需要获取restauant_name，对字段进行过滤，可以减少网络传送的字节。做法是加入一个请求参数`www.test.com/?fields[]=id&fields[]=name`,php支持传入数组，如果不支持数组，可以这样`www.test.com/?fieldsid+name`

#####自动加载相关资源
到目前为止，一个URI请求，只会请求一种资源：请求餐馆列表，请求订单列表，请求评价等等，如果需要在一个请求中，请求一个餐馆及所有在这个餐馆里面下的订单。

目前的做法是在URL中加入`extras`字段，表示需要加载的额外的资源，如：`www.test.com/?extras[]=orders`
在服务器根据extras字段，去加载相应的资源。

这样延迟加载相关资源的做法，可以有效避免`N+1`的额外开销
#####响应格式
使用`json`作为响应格式，不要再考虑`xml`, 何时时候使用“envelope”，类似于下面：
```
{
  "data" : {
    "id" : 123,
    "name" : "John"
  }
}
```
把信息主体放到`data`中，这种做法我觉得没有任何必要，有两种情况是应该使用envelope的。如果API使用者确实无法访问`Response Header`里面的信息，或者API需要支持交叉域请求，否则应该是在`Response Header`中加入返回的HTTP状态码，在信息主体中加入响应的信息的主体内容。

使用`envelope`:
```
callback_function({
  status_code: 200,
  next_page: "https://..",
  response: {
    ... actual JSON response body ...
  }
})
```
#####错误信息返回
json格式的错误应该包含以下信息：一个有用的错误信息，一个唯一的错误码，以及任何可能的详细错误描述
```
{
  'message': '系统未知错误',  错误信息
  'name': 'SERVER_UNKNOWN_ERROR' 错误码
}
```
restful框架设计，错误码和错误信息应该是一一对应。
##### HTTP响应状态码
比如获取一个资源，资源存在在响应`204`,如果没有找到该资源则返回404，需要理解的是，当客户端请求一个资源，服务器返回404和客户端访问不存在的URL，服务器响应404是不一样的。

需要注意的是，检测项目是否加星`GET /gists/:id/star` 如果项目没有加星，那应该返回404, 因为`star`被查看一个子资源

Response if gist is starred
```
Status: 204 No Content
X-RateLimit-Limit: 5000
X-RateLimit-Remaining: 4999
```

```
Status: 404 Not Found
X-RateLimit-Limit: 5000
X-RateLimit-Remaining: 4999
```
HTTP状态码：
```
 200 ok  - 成功返回状态，对应，GET,PUT,PATCH,DELETE.
 201 created  - 成功创建。
 304 not modified   - HTTP缓存有效。
 400 bad request   - 请求格式错误。
 401 unauthorized   - 未授权。
 403 forbidden   - 鉴权成功，但是该用户没有权限。
 404 not found - 请求的资源不存在
 405 method not allowed - 该http方法不被允许。
 410 gone - 这个url对应的资源现在不可用。
 415 unsupported media type - 请求类型错误。
 422 unprocessable entity - 校验错误时用。
 429 too many request - 请求过多。
```
#####版本化
个人推荐在URL里面加入版本，github做法：
```
https://developer.github.com/v3/gists/#check-if-a-gist-is-starred
```
v3就是版本号

##### restful需要注意点
重写HTTP方法
有的客户端只能发出简单的GET 和POST请求。为了照顾他们，我们可以重写HTTP请求。这里没有什么标准，但是一个普遍的方式是接受X-HTTP-Method-Override请求头。
```
    public function getMethod()
    {
        if (null === $this->method) {
            $this->method = strtoupper($this->server->get('REQUEST_METHOD', 'GET'));

            if ('POST' === $this->method) {
                if ($method = $this->headers->get('X-HTTP-METHOD-OVERRIDE')) {
                    $this->method = strtoupper($method);
                } elseif (self::$httpMethodParameterOverride) {
                    $this->method = strtoupper($this->request->get('_method', $this->query->get('_method', 'POST')));
                }
            }
        }

        return $this->method;
    }
```
#####速度限制
为了避免请求泛滥，给API设置速度限制很重要。为此 RFC 6585 引入了HTTP状态码429（too many requests）。加入速度设置之后，应该提示用户，至于如何提示标准上没有说明，不过流行的方法是使用HTTP的返回头。
下面是几个必须的返回头（依照twitter的命名规则）：
X-Rate-Limit-Limit :当前时间段允许的并发请求数
X-Rate-Limit-Remaining:当前时间段保留的请求数。
X-Rate-Limit-Reset:当前时间段剩余秒数

默认使用pretty print格式，使用gzip

是蛇形命令（下划线和小写）还是驼峰命名？如果使用json那么最好的应该是遵守JAVASCRIPT的命名方法-也就是说骆驼命名法

参考文章：http://www.csdn.net/article/2013-06-13/2815744-RESTful-API
