### 撸撸TCP

### 预期目的
    普及和梳理socket的细节问题, tornado的核心流程梳理

### 1,基本TCP套接字编程
1. socket
    1. 使用socket(family, type, protocol) family AF_INET AF_INET6, SOCK_STREAM, SOCK_DGRAM
    2. bind 把一个一个本地协议地址赋予一个socket, 协议地址是(addr, port)的组合 ，如果没有指定port, 内核会随机分配一个

    3. listen, 把一个套接字变成监听套接字，在服务器的生命周期内都不能关闭这个套接字；连接队列(已完成，未完成)
        队列已满，TCP忽略这个分节, client会重传以期望不久的将来能够队列有足够的容量， 三次握手后，
        在调用accept之前，数据已经开始传输，传输数据的最大数据量为连接套接字的缓冲区大小
    4. accept, 返回一个已经连接的套接字
    5. connect (socketfd, addr, port) 必须传递服务器的端口号和ip地址
        1. client没有收到SYN的响应(ACK), 则会重传这个分节，若75s后还是没有收到ACK应答这返回ETIMEDOUT错误
        2. client收到的是RST应答，服务器没有运行，或者对应的端口错误(tcpdump可以模拟)
    6. close， 值得注意的是close也许不会立即触发4次握手，在多进程的TCP服务器中，父进程会关闭已经连接的套接字，只是把
    这个套接字的引用计数减1，第二点，调用close之后，这个套接字不能再被进程使用，也就是不能作为read或write的参数，但是TCP将会已经排队等待发送给对端的数据发送完了之后，才会发生正常的TCP终止序列
    7. getsockname 在没有绑定addr和port的client中，获取内核自动分配的本地ip和端口号。

    8. 一个简单的tcp服务器搭建

### 2, 内核与进程的套接字地址结构的传递
1. 内核与进程的套接字地址结构的传递都会传递引用
    1. 从进程到内核传递套接字：bind, connnect, sendto等
    2. 从内核到进程的传递套接字: accpet, recv, getsocketname等
2. socket读缓冲区和写缓冲区 (UDP没有缓冲区)
    应为有缓冲区大小的限制，字节流套接字的read或write输入或者输出的字节数可能比请求的数量少


### 3, TCP的状态
[参考文章](http://coolshell.cn/articles/1484.html)

1. 基础概念
    1. SYN(Synchronize Sequence numbers)： 用来解决网络乱序问题
        1. SYN超时处理
        2. SYN队列(/proc/sys/net/ipv4/tcp_syn_*) tcp_max_syn_backlog 增加SYN的队列的连接数，tcp_abort_on_overflow 不处理SYN
        3.ISN (Inital Sequence Number) 初始化的SYN的值，目前SYN的值 = ISN + len(segment),一个ISN的周期大约是4.55个小时
    2. ACK(acknowledgment, number): 用来确认已经接受到的包，解决掉包问题
        1. ACK只能确认送到的最大的连续的包
        2. 重传机制：
            Fast Retransmit：仅仅重传超时的包(节省流量)，
            Selective Acknowledgment： ACK对端已经接受到的包 (/proc/sys/net/ipv4/tcp_sack), 在发送端就可以根据回传的SACK来知道哪些数据到了，哪些没有到
    3. WINDOW, 滑动窗口，用于控制流量
        这个字段是接收端告诉发送端自己还有多少缓冲区可以接收数据。于是发送端就可以根据这个接收端的处理能力来发送数据，而不会导致接收端处理不过来.

        超时时间设定：TCP引入了RTT——Round Trip Time，也就是一个数据包从发出去到回来的时间。这样发送端就大约知道需要多少的时间，从而可以方便地设置Timeout——RTO（Retransmission TimeOut），以让我们的重传机制更高效。 听起来似乎很简单，好像就是在发送端发包时记下t0，然后接收端再把这个ack回来时再记一个t1，于是RTT = t1 – t0。没那么简单，这只是一个采样，不能代表普遍情况

        RTT的采样，是否包括重传的时间

        缓存区满了处理，ack的时候window的大小是0，这个时候，发送端将不会发送数据。如果服务器端缓冲区又有空间了，怎么通知客户端呢，TCP使用了Zero Window Probe技术，缩写为ZWP，也就是说，发送端在窗口变成0后，会发ZWP的包给接收方，让接收方来ack他的Window尺寸，一般这个值会设置成3次，第次大约30-60秒
        如果3次过后还是0的话，有的TCP实现就会发RST把链接断了。

        如果你的网络包可以塞满MTU，那么你可以用满整个带宽，如果不能，那么你就会浪费带宽
        MTU: (Maximum Transmission Unit)
        MSS: (Max Segment Size) 最大的传输数据
        如果window变得特别小了，那么每次传输只会使用到一部分mtu的空间

    4. FLAG， 包的的类型，我们常见的有RST， FIN
        FIN：触发四次握手的时候发送此信号
        RST: 1 客户端请求一个服务器端口没有打开的服务，
             2 服务端接受SYN超时，会向对端发送一个RST,表示拒绝向你服务，服务器socket配置了SO_RCVTIMEO
             3 客户端在服务端已经关闭掉socket之后，仍然在发送数据。这时服务端会产生RST


2. 三次握手和四次握手(tcpdump 查看三次握手)

3. time_wait的状态，reuseaddr的配置 (netstat -an | grep 8888)
    1. 服务器将重新发送最后的一个FIN，对端必须维护状态信息，以允许它发送最后的ACK
    2. 我们会在相同的端口创建新的连接，TCP的必须保证新老的数据不会串，TCP将不会给处于TIME_WAIT状态的TCP发起新的化身，TIME_WAIT的时间是MSL的2倍，MSL 是Maximum Segment Lifetime英文的缩写，“报文最大生存时间”
4. tcp状态转移图

### 5, 阻塞式I/O和非阻塞式I/O
[I/O模型](http://www.jianshu.com/p/55eb83d60ab1)
1. I/O模型， 阻塞和非阻塞 术语：同步：导致请求进程阻塞，知道I/O完成，异步：不导致阻塞
2. 什么时候会发生阻塞
3. 如何解决阻塞

### 6, I/O复用：select/epoll
1. I/O模型之I/O复用：内核一旦发现一个或多个I/O条件就绪(可读，可写或者异常)就通知用户进程的能力
2. select的机制和限制
    `select(int maxfdp1,*readset,*writeset,*exceptset, timeout)`
    1. 注册可读，可写，异常的相关套接字
    2. timeout取值: None: 一直阻塞知道数据准备好，0: 不阻塞，立即返回，相当于轮询， >0: 阻塞的时间，当超过阻塞的时间还没有数据准备好则返回为空的集合
    3. `maxfdp1 = sockfd + 1` select在内核中是轮询的，内核遍历所有注册的fd，查看是否有准备好的fd， 套接字是从0开始的，所有maxfd  = max(socket) + 1，这也是select的限制(轮询和描述符数量限制)
    4. 如何给这三个集合指定多个描述符并返回准备好的描述符
    5. 什么是数据准备好，(可读：缓冲区数据大于低水位，接受到FIN的TCP连接，accpet, 异常， 可写: 缓冲区大于发送缓冲区的低水位， connect, 有错误处理，异常条件)
    6，多个客户端的处理

    ```
    SO_RCVBUF: 接受缓冲区的大小 (int)
    SO_SNDBUF: 发送缓冲区的大小 (int)
    SO_RCVLOWAT: 接受缓冲区的低水位大小 (int=1)
    SO_SNDLOWAT: 发送缓冲区的低水位 (int=2048)
    ```



3. epoll的水平触发和边沿触发
    1. 没有描述符数量的限制
    2. 事件触发机制不需要轮询
    3. 内存管理方式更高效(不需要复制fd)
    4. 给套接字注册相关的事件(可读，可写，异常)
    5. LT(level triggered) 是默认/缺省的工作方式，同时支持 block和no_block socket。这种工作方式下，内核会通知你一个fd是否就绪，然后才可以对这个就绪的fd进行I/O操作。就算你没有任何操作，系统还是会继续提示fd已经就绪，不过这种工作方式出错会比较小，传统的select/poll就是这种工作方式的代表。

    ET(edge-triggered) 是高速工作方式，仅支持no_block socket，这种工作方式下，当fd从未就绪变为就绪时，内核会通知fd已经就绪，并且内核认为你知道该fd已经就绪，不会再次通知了，除非因为某些操作导致fd就绪状态发生变化。如果一直不对这个fd进行I/O操作，导致fd变为未就绪时，内核同样不会发送更多的通知，因为only once。所以这种方式下，出错率比较高，需要增加一些检测程序。

    LT可以理解为水平触发，只要有数据可以读，不管怎样都会通知。而ET为边缘触发，只有状态发生变化时才会通知，可以理解为电平变化。

    epoll事件：
    ```
    POLLIN: 可读普通或者优先优先级
    POLLRDNROM: 普通优先级
    POLLRNDAND: 优先级
    POLLPRI: 高优先级

    POLLOUT: 普通数据可写
    POLLERR: 发送错误
    ```

    所以，在边缘触发模式下，必须每次都处理已经准备好的fd
4. tornado的事件触发机制：一个微型tcpserver的构建
