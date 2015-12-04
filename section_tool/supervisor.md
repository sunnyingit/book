# supervisor
[文章转载于烂笔头](http://dhq.me/mac-supervisor-install)

supervisor 是一个类 unix 操作系统下的进程监控管理工具，比如安装了redis-server，就可以使用supervisor管理redis-server

#### 安装

Supervisor 是由 Python 写成，可用 Python 的包安装管理工具pip直接安装：
`sudo pip install supervisor
`
#### 配置
Supervisor 服务启动的时候默认会在一下这几个目录位置查找配置文件 supervisord.conf。supervisor 也提供参数 "-c" 来指定配置文件的目录路径
`$CWD/supervisord.conf
$CWD/etc/supervisord.conf
/etc/supervisord.conf
`

在终端输入 "echo_supervisord_conf" 命令可查看 Supervisor 的默认配置的内容。

生成一份默认的配置文件
`echo_supervisord_conf > /etc/supervisord.conf
`
这里有选择的设置了一些配置，基本够用，配置如下：
```
[unix_http_server]
file=/var/run//supervisor.sock   ; (the path to the socket file)
chmod=0700                       ; sockef file mode (default 0700)

[supervisord]
logfile=/tmp/supervisord.log ; (main log file;default $CWD/supervisord.log)
pidfile=/var/run/supervisord.pid ; (supervisord pidfile;default supervisord.pid)
childlogdir=/var/log/supervisor            ; ('AUTO' child log dir, default $TEMP)

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix:///var/run//supervisor.sock ; use a unix:// URL  for a unix socket

[include]
files = /etc/supervisor/conf.d/*.ini
```

/etc/supervisor/conf.d/mux.ugc.ini的配置如下
```
[program:web.mux.ugc] ;进程名
command=thrift-mux run /workspace/ele/mux-ugc ;执行命令
autostart=true ;自启动
autorestart=unexpected
startsecs=3
startretries=3
stopsignal=TERM
stopwaitsecs=5
user=www-data   ; 特别注意此用户权限问
stopasgroup=true
killasgroup=true
stdout_logfile=/tmp/mux.web.ugc.stdout.log ; 程序运行日志
stderr_logfile=/tmp/mux.web.ugc.stderr.log ; 程序错误日志
```
#### 启动
`supervisord -c /etc/supervisord.conf`

#### 开机自启动
```php
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
    </dict>
    <key>Label</key>
    <string>dengjoe.supervisord</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/supervisord</string>
        <string>-n</string>
        <string>-c</string>
        <string>/etc/supervisord.conf</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```
启动 Supervisor 服务：
`launchctl load ~/Library/LaunchAgents/dengjoe.supervisord.plist`
supervisorctl 是 Supervisor 自带的后台进程控制工具，下面是该命令的一些用法：

使用supervisorctl：
`supervisorctl start/restart/status/stop/update program`

重新load 所有的supervisor服务
`sudo supervisorctl reload`
