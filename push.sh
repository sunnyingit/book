#!/bin/bash

# 使用 gitbook init 初始化书籍目录
# 使用 gitbook serve 编译书籍， 然后就可以本地在本地访问gitbook

 git add -A
 git commit -m 'commit all update!'

 cp -r ~/workspace/book/_book /tmp

 cd ~/workspace/book

 git checkout gh-pages

 [ $? != 0 ] && echo "fuck dog, !! checkout gh-pages failed!!!" && exit

 cp -r /tmp/_book/* .

 ls -la

 git add -A  > /dev/null 2>&1

 [ $? != 0 ] && echo "fuck dog git add failed" && git checkout master && exit

 git commit -m 'push by shell'

 git push > /dev/null 2>&1

 [ $? != 0 ] && echo "fuck dog push sunny failed" && git checkout master && exit

 git checkout master

 echo "Done!!!!"

