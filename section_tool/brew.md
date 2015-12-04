# Brew

------
Mac下得程序安装工具，类似于yum, apt-get工具  [官网](http://brew.sh/index_zh-cn.html)


#### 1 安装
打开终端，执行如下命令:

```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
#### 2 安装目录
```
Homebrew 会将套件安装到独立目录，并将文件软链接至 /usr/local $ cd /usr/local
$ find Cellar
Cellar/wget/1.16.1
Cellar/wget/1.16.1/bin/wget
Cellar/wget/1.16.1/share/man/man1/wget.1

$ ls -l bin
bin/wget -> ../Cellar/wget/1.16.1/bin/wget
```

#### 3 常用命令(以php为例)

```php
brew doctor 自检
brew update                        # 更新brew可安装包，建议每次执行一下
brew search php55                  # 搜索php5.5 查看php可使用的扩展有哪些
brew tap                           # 查看安装源
brew tap josegonzalez/php          # 添加一个新安装源
brew install php55                 # 安装php5.5
brew remove  php55                 # 卸载php5.5
brew upgrade php55                 # 升级php5.5
brew pin     php55                 # 禁止php5.5升级
brew unpin   php55                 # 去掉升级限制
brew options php55                 # 查看php5.5安装选项
brew info    php55                 # 查看php5.5相关信息
brew home    php55                 # 访问php5.5官方网站
brew cleanup php55                 # 删除旧版本

```

#### 4 定制brew上面没有的软件
首先找到待安装软件的源码下载地址
`http:/ /foo.com/bar-1.0.tgz`

建立自己的formula
`brew create http://foo.com/bar-1.0.tgz`

编辑formula，上一步建立成功后，Homebrew会自动打开新建的formula进行编辑，也可用如下命令打开formula进行编辑。
`brew edit bar`
Homebrew自动建立的formula已经包含了基本的configure和make install命令，对于大部分软件，不需要进行修改，退出编辑即可。

输入以下命令安装自定义的软件包
`brew install bar`

#### 5 安装软件开机自启动
使用brew 安装的软件会有一个文件
```
/usr/local/Cellar/nginx/1.6.2/homebrew.mxcl.nginx.plist
```
使用`launchctl`命令load这个文件之后，nginx就会开机自启,命令：
`launchctl load ~/Library/LaunchAgents/homebrew.mxcl.mysql.plist
`
下篇将会讲`launchctl`

#### 6 使用brew services

launchctl 使用还是太麻烦了，如果有个程序能自动设置开机自启动就好了，于是有了`brew services`

[官网](https://robots.thoughtbot.com/starting-and-stopping-background-services-with-homebrew)

安装 brew services
`brew tap homebrew/services
`

使用
```
brew services start/stop/restart/list/
```
Let’s say we uninstalled MySQL and Homebrew didn’t remove the plist for some reason (it usually removes it for you). There’s a command for you:
```
$ brew services cleanup
Removing unused plist /Users/gabe/Library/LaunchAgents/homebrew.mxcl.mysql.plist
```

#### 然后 `brew-cask`?

使用brew-cash 安装浏览器
```
$ brew install caskroom/cask/brew-cask
$ brew cask install google-chrome
```
