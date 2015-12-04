#!/bin/bash

 cp -r ~/workspace/gitbook/_book /tmp 

 cd ~/workspace/gitbook

 git checkout gh-pages
 
 [ $? != 0 ] && echo "fuck dog checkout gh-pages failed" && exit

 cp -r /tmp/_book/* .

 git add -A  > /dev/null 2>&1
 
 [ $? != 0 ] && echo "fuck dog git add failed" && git checkout master && exit

 git commit -m 'push by shell'
 
 git push sunny > /dev/null 2>&1

 [ $? != 0 ] && echo "fuck dog push sunny failed" && git checkout master && exit

 git checkout master

 echo "Done!!!!"

