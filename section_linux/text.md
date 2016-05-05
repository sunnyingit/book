# awk

------
### 常用说明
1 单引号中的被大括号括着的就是awk的语句，注意，其只能被单引号包含

2 其中的$1..$n表示第几列。注：$0表示整个行
```
$ awk '{print $1, $4}' netstat.txt
```

### 过滤条件
其中的“==”为比较运算符。其他比较运算符：!=, >, <, >=, <=
```
 awk '$3==0 && $6=="LISTEN" ' netstat.txt
 awk ' $3>0 {print $0}' netstat.txt
 awk '$3==0 && $6=="LISTEN" || NR==1 ' netstat.txt
 awk '$3==0 && $6=="LISTEN" || NR==1 {printf "%-20s %-20s %s\n",$4,$5,$6}' netstat.txt
```

### 指定分隔符
```
awk  -F: '{print $1,$3,$6}' /etc/passwd
awk -F '[;:]' '{print $1,$3,$6}' /etc/passwd
```

### 指定输出分隔符
```
awk  -F: '{print $1,$3,$6}' OFS="\t" /etc/passwd
```

### 字符串匹配
第六列匹配包含FIN的字符串，如果要输出行号 使用NR==1
```
awk '$6 ~ /FIN/ || NR==1 {print NR,$4,$5,$6}' OFS="\t" netstat.txt

 # 匹配 FIN 或者TIME
awk '$6 ~ /FIN|TIME/ || NR==1 {print NR,$4,$5,$6}' OFS="\t" netstat.txt

 # 模式取反的例子
awk '$6 !~ /WAIT/ || NR==1 {print NR,$4,$5,$6}' OFS="\t" netstat.txt

awk '!/WAIT/' netstat.txt
```

### 花活
```
#从file文件中找出长度大于80的行
awk 'length>80' file

#按连接数查看客户端IP
netstat -ntu | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -nr
```


特殊字符说明

```
\ This suppresses the special meaning of a character when matching. For example, ‘\$’ matches the character ‘$’.

^ This matches the beginning of a string. ‘^@chapter’ matches ‘@chapter’ at the beginning of a string

$ This is similar to ‘^’, but it matches only at the end of a string. For example, ‘p$’ matches a record that ends with a ‘p’

. (period)  This matches any single character, including the newline character. For example, ‘.P’ matches any single character followed by a ‘P’ in a string

[^…]
This is a complemented bracket expression. The first character after the ‘[’ must be a ‘^’. It matches any characters except those in the square brackets. For example, ‘[^awk]’ matches any character that is not an ‘a’, ‘w’, or ‘k’

{n}
{n,}
{n,m}
One or two numbers inside braces denote an interval expression. If there is one number in the braces, the preceding regexp is repeated n times. If there are two numbers separated by a comma, the preceding regexp is repeated n to m times. If there is one number followed by a comma, then the preceding regexp is repeated at least n times:

wh{3}y
Matches ‘whhhy’, but not ‘why’ or ‘whhhhy’.

wh{3,5}y
Matches ‘whhhy’, ‘whhhhy’, or ‘whhhhhy’ only.
```

# sed

------

### 用s命令替换
把其中的my字符串替换成Hao Chen’s，下面的语句应该很好理解（s表示替换命令，/my/表示匹配my，/Hao Chen’s/表示把匹配替换成Hao Chen’s，/g 表示一行上的替换所有的匹配）

```
sed "s/my/Hao/g" pets.txt
```
注意：如果你要使用单引号，那么你没办法通过\’这样来转义，就有双引号就可以了，在双引号内可以用\”来转义
再注意：上面的sed并没有对文件的内容改变，只是把处理过后的内容输出，如果你要写回文件，你可以使用重定向

#### 使用i直接修改源文件
```
sed -i "/s/my/Hao/g" pets.txt
```

#### 添加新内容
在每一行最前面加点东西
```
sed -i "s/^/##/g" pets.txt
```
在每一行最后面加点东西
```
sed -i "s/$/----/g" pets.txt
```

#### 指定需要替换的内容
```
# 替换第三行的内容,
sed "3s/my/your/g" pets.txt

# 替换第三行到第六行的内容
sed "3, 6s/my/your/g" pets.txt

# 替换每一行的第一个s, 第一个s前面不指定行号，说明是每一行
# 最后一个'1'表示遇到的第一个's'
sed "s/s/S/1"

# 只替换每一行的第二个s
sed "s/s/S/2"

# 只替换第一行的第3个以后的s：
sed "s/s/S/3g"
```

### 多个匹配
第一个模式把第一行到第三行的my替换成your，第二个则把第3行以后的This替换成了That
```
 sed '1,3s/my/your/g; 3,$s/This/That/g' my.txt

 # 等价于
 sed -e '1,3s/my/your/g' -e '3,$s/This/That/g' my.txt
```

### a命令和i命令
a命令就是append， i命令就是insert，它们是用来添加行的
```
其中的1i表明，其要在第1行前插入一行（insert）
sed "1 i this is test" my.txt

其中的1a表明，其要在最后一行后追加一行（append）
 sed "$ a This is my monkey, my monkey's name is wukong" my.txt

注意其中的/fish/a，这意思是匹配到/fish/后就追加一行
sed "/fish/a This is my monkey, my monkey's name is wukong" my.txt
```

### d命令
删除匹配行
```
删除匹配到fish的行
sed '/fish/d' my.txt
删除第二行
sed '2d' my.txt

只保留前2行
sed "3, $d" my.txt
```

# grep

```
－c：只输出匹配行的计数。
－I：不区分大 小写(只适用于单字符)。
－h：查询多文件时不显示文件名。
－l：查询多文件时只输出包含匹配字符的文件名。
－n：显示匹配行及 行号。
－s：不显示不存在或无匹配文本的错误信息。
－v：显示不包含匹配文本的所有行。

正则规则
\： 忽略正则表达式中特殊字符的原有含义。
^：匹配正则表达式的开始行。
$: 匹配正则表达式的结束行。
\<：从匹配正则表达 式的行开始。
\>：到匹配正则表达式的行结束。
[ ]：单个字符，如[A]即A符合要求 。
[ - ]：范围，如[A-Z]，即A、B、C一直到Z都符合要求 。
. ：所有的单个字符。
* ：有字符，长度可以为0
```

### 实例
```
显示所有以d开头的文件中包含 test的行
$ grep ‘test’ d*

在多个文件中查找
$ grep ‘test’ aa.txt bb.txt cc.txt

# 注意\{\}需要转义，显示所有包含每个字符串至少有5个连续小写字符的字符串的行
$ grep ‘[a-z]\{5\}’ aa

# 匹配一个目录
grep -r 'a' /usr/src/*

```

#  sort
```
-r 逆序
```
#  uniq
去重
```
-c, –count 在每行文本前面输出重复次数
-d,只显示重复的行, 重复的行只显示一行
-D, 显示所有重复的行, 注意该选项与选项-d的区别
-i, 不区分大小写
uniq -c my.txt
```

