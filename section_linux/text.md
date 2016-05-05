# awk 配置

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

### 正则表达式字符说明

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

(…)
Parentheses are used for grouping in regular expressions, as in arithmetic. They can be used to concatenate regular expressions containing the alternation operator, ‘|’. For example, ‘@(samp|code)\{[^}]+\}’ matches both ‘@code{foo}’ and ‘@samp{bar}’. (These are Texinfo formatting control sequences. The ‘+’ is explained further on in this list.)

*
This symbol means that the preceding regular expression should be repeated as many times as necessary to find a match. For example, ‘ph*’ applies the ‘*’ symbol to the preceding ‘h’ and looks for matches of one ‘p’ followed by any number of ‘h’s. This also matches just ‘p’ if no ‘h’s are present.

There are two subtle points to understand about how ‘*’ works. First, the ‘*’ applies only to the single preceding regular expression component (e.g., in ‘ph*’, it applies just to the ‘h’). To cause ‘*’ to apply to a larger subexpression, use parentheses: ‘(ph)*’ matches ‘ph’, ‘phph’, ‘phphph’, and so on.

Second, ‘*’ finds as many repetitions as possible. If the text to be matched is ‘phhhhhhhhhhhhhhooey’, ‘ph*’ matches all of the ‘h’s.

+
This symbol is similar to ‘*’, except that the preceding expression must be matched at least once. This means that ‘wh+y’ would match ‘why’ and ‘whhy’, but not ‘wy’, whereas ‘wh*y’ would match all three.

?
This symbol is similar to ‘*’, except that the preceding expression can be matched either once or not at all. For example, ‘fe?d’ matches ‘fed’ and ‘fd’, but nothing else.
```



