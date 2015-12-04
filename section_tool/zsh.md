

#### 简介

使用了zsh，再也不需要使用bash

[git主页](https://github.com/robbyrussell/oh-my-zsh#the-manual-way)

####  安装
好消息是Mac,linux自带zsh, 查看shells

```
cat /etc/shells
/bin/bash
/bin/zsh
```
查看正在使用的shell
```
echo $SEHLL
/bin/zsh
```
修改shell
```
chsh -s /bin/zsh
```
安装shell
```
brew install zsh
```
原生zsh过于难配置，需要配合[oh my shell](https://github.com/robbyrussell/oh-my-zsh) 使用，才能驾驭

安装oh my shell，执行下面命令之后，重启切换到zsh shell

```python
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```

#### 配置文件
```
~/.zhsrc
```

##### [自定义配置猛击](http://www.cnblogs.com/ma6174/archive/2012/05/08/2490921.html)


#### 使用

##### 更智能的补全 ，试着多按几次`<TAB>`
```
 sunlili@eleme ~ ssh 按下tab

 列出所有的ssh连接过的服务器
```

##### 按`d`，输入数字切入相应地目录
```
➜  upload-ohsame-com git:(master) d
0   ~/Desktop/workspace/upload-ohsame-com
1   ~/Desktop/workspace/upload-ohsame-com/v2
2   ~/Desktop/workspace
3   ~/Desktop
```

#####支持全局 alias 和后缀名 alias
```
alias cp='cp -i'
alias mv='mv -i'
alias rm='rm -i'
alias ls='ls -F --color=auto'
alias ll='ls -l'
```

##### 历史命令记忆
```
输入git之后，按下上下方向键，既可以搜索到所有使用过的 git xxx 命令,不喜欢方向键有木有，不要紧安装vi-mode插件，继续往下看
```

##### zsh 支持更加聪明的目录补全
 只需要输入每个路径的头字母然后 tab 一下： `cd /u/p/a/j<TAB>`

 #### 插件
 所有的插件都在```~/.oh-my-zsh/plugins```, [插件wiki地址](https://github.com/robbyrussell/oh-my-zsh/wiki/Plugins),我常用的插件如下

 `git`: 你必须已经安装了git，在git仓库中时，这个插件会显示目前文件所在branch

 `autojump`: j + 目录名

 第一次使用无效，使用这个插件之前，你必须安装了autojump软件
 mac
 ```brew install autojump
 ```
 linux:
 `wget https://github.com/downloads/joelthelion/autojump/autojump_v21.1.2.tar.gz`，

 当你使用cd切换目录的时候，autojump会记录你的cd操作，之后你是要j + 目录名就可以切换到相应的目录，不需要输入完整的目录路径


`web-search`: 使用bing, google搜索, 不需要在浏览器中输入了啦

`vi-mode`: 让zsh更加vi-like， 使用 `ESC` or `CTRL-[` 进入vi-like 模式,使用方法如下：

`ctrl-p` : Previous command in history
`ctrl-n` : Next command in history
`/` : Search backward in history
`n` : Repeat the last /

再也不需要按‘up’, 'down'方向键搜索命令历史了, 手不需要离开键盘了

