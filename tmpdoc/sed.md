####sed 使用用法总结

##### s 替换命令

 把xg-替换为sed-

sed "s/xg\-/sed\-/g" sed.log 

 上面的命令不会修改sed.log 可以使用 sed "s/xg\-/sed\-/g" sed.log > sed.log 获取  sed -i "s/xg\-/sed\-/g" sed.log  

 建议使用双引号，如果需要匹配双引号，可以使用"\"转义，但不能对单引号转义
 g 表示global 全局替换，如果只替换每一行的第1个 'xg-', 只想替换 1-2行 
sed "1,2s/xg\-/sed\-/1" sed.log

 如果想替换第三行到最后一行
sed '1,$s/xg\-/Rend-/g' sed.log

可以使用&来当做被匹配的变量，然后可以在基本左右加点东西

sed 's/sed/[&]/g' sed.log

 在每行的前面加点内容
sed 's/^/start/g' sed.log

 在每行的结尾加点内容
sed "s/$/end/g" sed.log

 如果我们需要一次替换多个模式，可参看下面的示例：（第一个模式把第一行到第三行的my替换成your，第二个则把第3行以后的This替换成了That）

sed -e '1,3s/my/your/g' -e '3,$s/This/That/g' sed.log
sed '1,3s/my/your/g; 3,$s/This/That/g' sed.log

 圆括号括起来的正则表达式所匹配的字符串会可以当成变量来使用，sed中使用的是\1,\2, 例如把xg 替换为（xg）

sed 's/\(xg\)/\(\1\)/g' sed.log


##### d 删除命令

删除带有“fish”的行
$ sed '/fish/d' my.txt
This is my cat, my cat's name is betty
This is my dog, my dog's name is frank
This is my goat, my goat's name is adam
 
删除第二行 
$ sed '2d' my.txt
This is my cat, my cat's name is betty
This is my fish, my fish's name is george
This is my goat, my goat's name is adam
 
只保留第一行
$ sed '2,$d' my.txt
This is my cat, my cat's name is betty


##### c 替换匹配行
直接替换第二行
$ sed "2 c This is my monkey, my monkey's name is wukong" my.txt
This is my cat, my cat's name is betty
This is my monkey, my monkey's name is wukong
This is my fish, my fish's name is george
This is my goat, my goat's name is adam
 
替换带有fish的行
$ sed "/fish/c This is my monkey, my monkey's name is wukong" my.txt
This is my cat, my cat's name is betty
This is my dog, my dog's name is frank
This is my monkey, my monkey's name is wukong
This is my goat, my goat's name is adam


#### a命令和i命令
a命令就是append， i命令就是insert，它们是用来添加行的。如：

# 其中的1i表明，其要在第1行前插入一行（insert）
$ sed "1 i This is my monkey, my monkey's name is wukong" my.txt
This is my monkey, my monkey's name is wukong
This is my cat, my cat's name is betty
This is my dog, my dog's name is frank
This is my fish, my fish's name is george
This is my goat, my goat's name is adam
 
# 其中的1a表明，其要在最后一行后追加一行（append）
$ sed "$ a This is my monkey, my monkey's name is wukong" my.txt
This is my cat, my cat's name is betty
This is my monkey, my monkey's name is wukong
This is my dog, my dog's name is frank
This is my fish, my fish's name is george
This is my goat, my goat's name is adam
我们可以运用匹配来添加文本：

# 注意其中的/fish/a，这意思是匹配到/fish/后就追加一行
$ sed "/fish/a This is my monkey, my monkey's name is wukong" my.txt
This is my cat, my cat's name is betty
This is my dog, my dog's name is frank
This is my fish, my fish's name is george
This is my monkey, my monkey's name is wukong
This is my goat, my goat's name is ad