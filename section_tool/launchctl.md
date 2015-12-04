
# launchctl
launchctl 管理OS X的启动脚本，控制启动计算机时需要开启的服务。也可以设置定时执行特定任务的脚本，就像Linux crontab一样, 通过加装*.plist文件执行相应命令

#### **使用**
开机时自动启动mysql服务器：
`$ sudo launchctl load -w /System/Library/LaunchDaemons/homebrew.mxcl.mysql.plist`

`launchctl list` 显示当前的启动脚本。

`sudo launchctl unload [path/to/script]` 停止正在运行的启动脚本，再加上 -w 选项即可去除开机启动。

Launchd脚本存储在以下位置, 默认需要自己创建个人的LaunchAgents目录
```
~/Library/LaunchAgents
/Library/LaunchAgents
/Library/LaunchDaemons
/System/Library/LaunchAgents
/System/Library/LaunchDaemons
```

`mkdir -p ~/Library/LaunchAgents
`

#### brew和launchctl配置使用
通过brew安装的软件，通常都会有一个*.plist文件,所以通过launchctl可以使brew安装的软件开机自启动


#### MAC常用命令
`pbcopy` 和 `pbpaste`

这两个工具可以打通命令行和剪贴板。当然用鼠标操作复制粘贴也可以——但这两个工具的真正威力，发挥在将其用作Unix工具的时候。意思就是说：可以将这两个工具用作管道、IO重定向以及和其他命令的整合。例如：
`$ ls ~ | pbcopy`
可以将主目录的文件列表复制到剪贴板。
也可以把任意文件的内容读入剪贴板：

`$ pbcopy < blogpost.txt`
做点更疯狂的尝试：获取最新Google纪念徽标（doodle）的URL并复制到剪贴板：

`$ pbpaste >> tasklist.txt`

[Mac 命令大全](http://ss64.com/osx/)
