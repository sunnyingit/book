# 网络性能

### iptraf
测试两台主机之间的网络性能的一个办法就是在这两个系统之间互发数据并统计结果，看看吞吐量、延迟、速率如何, iptraf 用于查看本机网络的吞吐量，IO速率等参数
```
# install
sudo apt-get install iptarf
iptraf -d eth0
```
### ping
ping 使用ICMP协议，测试两个主机之间是否可以访问
```
ping [host|ip]
```

### telnet
，telnet因为采用明文传送报文，安全性不好，很多Linux服务器都不开放telnet服务，而改用更安全的ssh方式。

使用`ping`命令可以检测两台主机是否可以connection, `telnet`用来检测主机的某些端口是否可以访问

```
telnet host [port]
```

### netstat
netstat主要用于查看TCP/IP协议的相关数据，在实际业务中，例如服务要调用另一个服务器的服务，数据没有返回，可以使用netstat查看两个机器是否通信，端口是否被占有，TIME_WAIT的数量等
```
man netstat

 netstat {--statistics|-s} [--tcp|-t] [--udp|-u] [--udplite|-U] [--raw|-w] [delay]

  --wide , -W
       Do not truncate IP addresses by using output as wide as needed. This is optional for now to not break existing scripts.

   --numeric , -n
       Show numerical addresses instead of trying to determine symbolic host, port or user names.

   --numeric-hosts
       shows numerical host addresses but does not affect the resolution of port or user names.

   --numeric-ports
       shows numerical port numbers but does not affect the resolution of host or user names.

   --numeric-users
       shows numerical user IDs but does not affect the resolution of host or port names.
```
 常用组合
 ```
 netstat -tupl | grep 'mysql'
 netstat -a | grep '80'
 netstat -n | grep '423.11.11.55'

 ```
### tcpdump
dump traffic on a network, 更详细的输出网络状况, 在实际业务中，获取两台服务器之间的通信

```
可以指定ip,例如截获所有210.27.48.1 的主机收到的和发出的所有的数据包
tcpdump host 210.27.48.1

打印helios 与 hot 或者与 ace 之间通信的数据包
tcpdump host helios and \( hot or ace \)

截获主机210.27.48.1 和主机210.27.48.2 或210.27.48.3的通信
tcpdump host 210.27.48.1 and \ (210.27.48.2 or 210.27.48.3 \)

监视所有送到主机hostname的数据包
tcpdump -i eth0 dst host hostname

如果想要获取主机210.27.48.1接收或发出的telnet包，使用如下命令
tcpdump tcp port 23 and host 210.27.48.1

监视指定协议的数据包
tcpdump 'tcp[tcpflags] & (tcp-syn|tcp-fin) != 0 and not src and dst net localnet'
```

### tcpdump 与wireshark
```
tcpdump tcp -i eth1 -t -s 0 -c 100 and dst port ! 22 and src net 192.168.1.0/24 -w ./target.cap

(1)tcp: ip icmp arp rarp 和 tcp、udp、icmp这些选项等都要放到第一个参数的位置，用来过滤数据报的类型
(2)-i eth1 : 只抓经过接口eth1的包
(3)-t : 不显示时间戳
(4)-s 0 : 抓取数据包时默认抓取长度为68字节。加上-S 0 后可以抓到完整的数据包
(5)-c 100 : 只抓取100个数据包
(6)dst port ! 22 : 不抓取目标端口是22的数据包
(7)src net 192.168.1.0/24 : 数据包的源网络地址为192.168.1.0/24
(8)-w ./target.cap : 保存成cap文件，方便用ethereal(即wireshark)分析
```


[Linux tcpdump命令详解](http://www.cnblogs.com/ggjucheng/archive/2012/01/14/2322659.html)
[tcpdump 和 wireshark组合拳，揪出有问题的机器](http://www.bo56.com/tcpdump-%E5%92%8C-wireshark%E7%BB%84%E5%90%88%E6%8B%B3%EF%BC%8C%E6%8F%AA%E5%87%BA%E6%9C%89%E9%97%AE%E9%A2%98%E7%9A%84%E6%9C%BA%E5%99%A8/)

