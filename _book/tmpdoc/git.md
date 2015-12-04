#### git使用梳理

#### 目录

0. [配置](#doc-0)
1. [工作区，暂存区，git仓库](#doc-1)
2. [本地仓库和远程仓库](#doc-2)
3. [本地分支管理](#doc-3)
4.  [远程分支管理](#doc-4)
5. [git常用命令](#doc-5)
6. [git工作模式](#doc-6)

<h5 id="doc-0">配置</h5>
etc/gitconfig: 适用于所有的用户
~/.gitconfig: 适用于当前用户
.git/config:适用于当前项目

使用git管理项目，无法查看到代码的提交者，一般是git没有配置用户名和邮箱
```
git config --global user.name "sunny"   
git config --global user.email "sunliwodewy@163.com"
git config --global core.atuocrlf=true  解决在windows和linux的换行格式化问题
git config --global push.default=current
```

<h5 id="doc-0">工作区，暂存区，git仓库</h5>
明明在一个目录中创建了一个文件，后来在此目录中去无法找到,这种问题就是没有理解工作区，暂存区和git仓库的联系。

一个git仓库只有一个工作区，在工作区里面创建，修改文件后，需要使用git add 提交到暂存区，使用git commit 命令把暂存区的内容提交到git 仓库。

无法找到创建的文件的问题，一般是由多分支导致的，当git切换不同的分支，工作区的内容就会变成切换后的分支内容，如果仅在A分支创建a文件,当
切换到B分支的时候，就找不到a文件了

文件2种状态：
```
1 Changes not staged for commit  没有储存到暂存区
2 Changes to be committed    已经储存到暂存区，么有提交到git仓库
```
<h5 id="doc-0">本地仓库和远程仓库</h5>
git管理的代码要推送到远程仓库中(github), 需要把本地git和远程git关联起来。代码的推送是基于git分支的，也就是说，本地仓库和远程仓库关联之后，就可以把本地分支的内容推送远程分支上。

如何关联本地分支和远程分支
```
git clone git@github.com:用户名/仓库名 clone后会自动在本地创建一个master分支，并关联远程仓库origin/master分支

git push -u origin master 推送本地的当前分支到远程仓库origin的master分支上，即把当前分支和远程分支关联起来

git checkout -b [分支名] [远程仓库] / [分支名]
```
需要理解本地分支可以关联不同的远程分支，关联之后，本地分支就可以跟踪远程分支。

远程仓库的操作
```
git remote -v                    # 查看远程服务器地址和仓库名称
git remote show origin           # 查看远程服务器仓库状态
git remote add origin git@github:robbin/robbin_site.git         # 添加远程仓库地址
git remote set-url origin git@github.com:robbin/robbin_site.git # 设置远程仓库地址(用于修改远程仓库地址)
git remote rm <repository>       # 删除本地的远程仓库
```
