# 扫描登陆

## 目录:

1. [流程解析](#doc-1)
2. [数据库设计](#doc-2)
3. [API设计](#doc-3)

<h3 id="doc-1">流程解析</h3>


1. 用户请求二维码登陆的页面，服务器生成一个唯一标识uuid，可以使用base64加密，状态为未绑定

2. 在APP登陆的情况下，使用APP扫描二维码获取到uuid, 并提示确认登陆

3. APP点击确认登陆，把之前已经登陆的用户信息, uuid, timestamp，提交到服务器

4. 服务器绑定用户和uuid的信息, 并标示uuid的状态为已绑定

5. 网页每隔5s，轮询向服务器询问uuid是否绑定了user信息，请求参数：uuid, timestamp, rand_id

6. 服务器验证uuid是否过期，uuid过期则提示用户重新刷新，获取新的uuid, 如果uuid没有过期，且APP还没有扫描，则返回httpcode 408, 如果uuid绑定了用户，则通过uid, timestamp, rand_id 加密生成一个access_token 并把access_token返回给网页

7. 网页通过access_token, 获取用户信息

###### 为什么要使用access_token，而不直接使用uuid?
因为uuid在未登录的时候，已经暴露出去，试想一下，如果A用户打开了登陆网页，并记下来uuid, 然后通知B来扫描登陆，
如果用uuid来获取用户的话，A用户就可以获取到B用户的信息


<h3 id="doc-2">数据库设计</h3>

`二维码表 qr`

###### 字段描述
| 名字 | 类型 | 详细描述 |
| ----- | ----- | -------- |
| id | INT | auto |
| uuid | STRING | 唯一标识 |
| status | TINYINT | 1 未绑定， 2已绑定， 3 已过期 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 修改时间 |

`用户 user`

###### 字段描述
| 名字 | 类型 | 详细描述 |
| ----- | ----- | -------- |
| uuid | STRING | 唯一标识 |
| access_token| STRING | 获取用户的信息的凭证 |
| expired_at| TIMESTAMP | access_token 过期时间|


<h3 id="doc-3">API设计</h3>


`APP扫描授权 POST /login/qrcode/auth`

###### 参数描述
| 名字 | 类型 | 详细描述 |
| ----- | ----- | -------- |
| uuid | STRING | uuid |

###### 响应
`204`


`判断是否授权 POST /login/qrcode`

###### 参数描述
| 名字 | 类型 | 详细描述 |
| ----- | ----- | -------- |
| uuid | STRING | uuid |
| timestamp | STRING | 当前时间戳 |
| rand_id | STRING | 随机字符串, 可选 |

###### 响应描述
| 名字 | 类型 | 详细描述 |
| ----- | ----- | -------- |
| access_token | STRING | access_token，用于获取用户信息 |
| expired_at | STRING | access_token的过期时间 |

###### 响应
```
{
    'access_token': 'token',
    'expired_at': 1313131312,
}
```


`通过access_token 获取用户信息 GET /user`

###### 参数描述
| 名字 | 类型 | 详细描述 |
| ----- | ----- | -------- |
| uuid | STRING | uuid |
| access_token | STRING | 当前时间戳 |


###### 响应
用户信息










