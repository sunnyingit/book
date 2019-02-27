
文章参考[卢钧轶(cenalulu)](http://cenalulu.github.io/linux/tmux/)

#### **简介**
Tmux是一个服务器，他是它提供了一个窗体组随时存储和恢复的功能窗口被关闭没有关系，只要Tmux server没有被kill, 就能很快的恢复， 比如你在远程服务器上面开了很多窗口，由于ssh超时导致再次连接远程服务器的时候，窗口全部被关闭了，不爽！

在远程服务器上面开启tmux就好了，tmux会保存你打开的窗口！

#####  **安装**
```
brew install tmux
apt-get install tmux
```

#### **tmux解释**
我们先来理解下tmux的几个元素。tmux的主要元素分为三层：

`Session` 一组窗口的集合，通常用来概括同一个任务。session可以有自己的名字便于任务之间的切换。

`Window` 单个可见窗口。Windows有自己的编号，也可以认为和ITerm2中的Tab类似。

`Pane` 窗格，被划分成小块的窗口，类似于iterm 分屏。


![file-list](http://ww2.sinaimg.cn/mw690/6941baebjw1et4uosbtuhj21kw0qvqf1.jpg)

#### **使用流程**
`session` 我一般会两个session `tmux new -s r(remote)` 这个session会处理远程服务器 `tmux new -s w(workspace)` 处理本地的服务器

`window` 编辑`xxz`目录开一个窗口，处理`xxxx`业务又开一个窗口，原则就是，你需要同时处理多少业务就开多少窗口，我最多开启5个，多了不好管理

`Pane` 在使用监控的时候最好分屏处理，一个屏发起请求，一个屏监控日志，还有一个屏幕实时修改代码调试，爽！

#### **快捷键**

Prefix-Command前置操作：所有下面介绍的快捷键，都必须以前置操作开始。tmux默认的前置操作是CTRL+b。例如，我们想要新建一个窗体，就需要先在键盘上摁下CTRL+b，松开后再摁下n键。

下面使用prefix代表 CTRL+b
#### session
输入`tmux` 会自动创建一个session
1  `tmux new -s session_name` 创建session
2  `tmux ls` 列出所有的session
3  `prefix d(deattach)`离开session， session还会在后台运行
4  `prefix $` 重命名session, 或者 `prefix : new-session`
5  `tmux attach -t session_name` 链接一个后台运行的session

#### window
  `prefix c`（create）创建一个窗口
  `prefix 数字` 切换窗口
  `prefix q` 查询窗口
  `prefix &` 关闭窗口


####Panne
`prefix %` 水平切分窗口
`prefix “`  垂直切分
`prefix 方向键` 选择panne
`prefix z` 暂时把一个窗口放大
`prefix o` 切换到下一个panne
`prefix !` 删除一个pannecd

####命令行
`prefix : 命令` 在终端中执行tmux的命令，例如 prefix: attach-session -t s 使用tab可以补全命令


#### **tmux原生还是不好用**

首先，Ctrl+b 太难按了，手没有这么长，而且不支持任何鼠标行文，使用大神的配置 [请猛击](https://github.com/gpakosz/.tmux)

大神文档中说明如何复制，粘贴，选择pane, 安装后可以查看如何copy, 切换pane，配置在：
```
~/.tmux.conf
```

#### 大神还是没有支持鼠标
```
vim ~/.tmux.conf.local
# 使用鼠标复制的时候按住alt键
set -g mode-mouse on
# 开启鼠标选择pane
set -g mouse-select-pane on
# 开启鼠标调整pane大小
set -g mouse-resize-pane on
# 鼠标选择窗口
set -g mouse-select-window on
```
