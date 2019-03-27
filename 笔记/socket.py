import selectors
"""
IP分组标记DF
如果没设置DF表示可以分组，在发送数据报的时候如果链路不允许这么大的数据发送那么就将是数据分隔成一个个小的包进行标记发送
然后在收到地址上重新组合成一个新的数据报
如果设置了说明不允许分组，传送失败的时候会丢弃数据报然后尝试将数据报分割成较小的数据再次发送。
如果是一个数据报UDP的操作系统可能不会进行标记DF分组这样所有的数据都会发送到对面
但是如果是一个TCP的长数据流那么操作系统就会DF分组方便操作系统确定每一个数据包的大小方便畅通的进行发送数据，
防止在传输的时候一直分割数据报降低效率
多路复用
    在两台主机之间的连接，把不同的程序的数据打上不同的标签，来进行传输防止数据无法识别
可靠传输
    保证传输的数据是完整的，如果有顺序错误那么就会将整个包重组正确顺序，有数据丢失就重传，删除多余数据


用户空间与内核空间
    虚拟储存器一般有两个空间，一个是用户空间，一个是内核空间，内核空间是操作系统自己使用的空间，权限很高能干很多事情，
    不希望用户空间也和它搅在一起，所以Linux一般将虚拟空间中位置较高的1G分配给内核空间，剩下的分配给用户空间

I/O访问
    首先操作系统会把数据加载到操作系统的内核缓冲区中，然后再从内核缓冲区加载到应用程序的内存空间
    进行数据拷贝对cpu的运行开销十分的大

水平触发:
    如果文件描述符可以非阻塞的执行I/O系统调用，此时认为已经准备就绪
    在使用水平触发的时候随时都可以进行关于文件描述符的查询，这个时候并不需要进行尽可能多的I/O(可以选择执行，甚至不执行I/O)
    select()和poll()只支持水平触发 epoll()支持水平触发
边缘触发:
    如果文件描述符从上次检测的状态以来有了新的I/O活动，此时需触发通知
    因为是边缘触发的情况，所以尽可能的在某一个时刻对程序进行尽可能多的I/O，因为这里不对程序进行足够的I/O
    在下次有新的I/O状态的时候才会再次通知，在这之前可能没接受到足够的数据造成数据丢失程序阻塞之类的
    每一个边缘触发的程序都应该设定为非阻塞的不然一直for io的话可能最后没有I/O操作的时候程序就会因为没有数据而进行等待阻塞，
    非阻塞的情况执行到没有I/O的时候就会返回一个错误码。
    信号驱动I/O只支持边缘触发 epoll()同样支持边缘触发
I/O模型
    阻塞I/O
        首先程序进行的时候，recv数据，首先cpu等待接受数据，再将数据复制到用户内存中(操作系统内核缓冲区)，然后返回结果。
        在其中等待数据的阶段整个程序会暂时阻塞，当数据被返回之后就可以继续执行，这种情况cpu可以在程序被阻塞的时候去干别的事
        提高利用率
    非阻塞I/O
        并不会阻塞，而是一次一次的询问操作系统我的数据好了吗，没好就返回一个error的信号，然后再次询问，一旦数据已经接收完成
        就马上复制到用户内存中,返回数据

    python中的select:
        在调用的时候会先将这三个指针初始化，因为这里只储存结果值，先将指针初始化，然后把响应的文件描述符绑定过去
        select会一直阻塞直到有文件描述符达到了就绪状态
        就绪状态的时候就返回数据了，底层已经帮你完成了数据的整理
        def select(rlist, wlist, xlist, timeout=None):
            rlist 读指针
            wlist 写指针
            xlist 错误信息指针
            timeout 阻塞时间，设定为NULL的时候将会一直阻塞，直到其中一个操作符达到就绪，或者例程中断，timeout时间过期
        返回值 -1的时候说明有错误，或者三个参数中有违法的，0的时候说明调用文件操作符的时候超时了，所有描述符清空，
            正整数是众多连接中文件描述符达到就绪的个数(上面三个)。
            
    poll
        fd 指定文件描述符的个数
        event 
        revents
        一般都是调用掩码
            POLLIN  可读
            POLLOUT 可写
            POLLERR 错误
            POLLHUP 出现挂断
            POLLRDNORM 等同于POLLIN
            POLLWRNORM  等同于POLLOUT
            POLLWRBAND  优先级数据写入
            POLLPRI 可读取高优先数据
        timeout 
            -1处于一直阻塞的状态，直到有文件描述符就绪
            0  只检查一次
            大于0 最多阻塞timeout时间，直到有文件描述符就绪
        返回值
            -1 内部报错
            0 在调用之前就已经超时
            正整数 说明有多个值就绪了
            
    poll 与 select的区别 如果在返回值中有一个文件描述符出现多次，select会重复计数，poll不会
    其实内部的poll与select都是调用的相同内核返回一系列的掩码，只不过调用select的时候被包装一下
        POLLIN POLLRDNORM POLLERR POLLHUP POLLRDBAND r
        POLLOUT POLLWRNORM POLLERR POLLWRBAND w
        POLLPRI except
        掩码包装
    性能区别
        select是1024定长数组，poll是用户自定义长度数组
        当需要检查的文件描述符范围很小的时候
        有大量文件需要被描述的时候，而且分布十分密集
        以上两种情况性能差距十分小
        
        当被检查的文件十分少，却又十分分散在非常大的序列中，poll的优势就会很明显
        可以从输入的参数来了解原因select传递文件描述符集合，和范围nfds(比要检查的最大号+1)
        这样的话必须从头查到尾，而poll就不需要了只需要制定对应的文件描述符，内核会自动检查
        (当然在新的2.6系统中已经被大大优化了)
    问题
        每次使用select和poll都要挨个检查所有指定范围的数据，开始检查之后需要将数据发送给内核然后拷贝到内核缓冲区之后再返回
        数据，每次这样重复的拷贝会占据大量的时间
    
    epoll
        一般epoll使用水平触发，也可以使用边缘触发，但是一定要配合非阻塞的文件描述符
        select和poll支持水平触发，epoll支持边缘触发和水平触发
        
        三个部分
            epoll_create()创建一个epoll实例返回代表该实例的文件描述符
            epoll_ctl()操作同epoll实例相关联的兴趣列表，通过这个api可以增添文件描述符，删除文件描述符，修改文件描述符
            epoll_wait 返回就绪列表中的成员          
        timeout
            -1 一直阻塞直到有信号发生
            0 执行一次非阻塞的行为检查有没有文件就绪
            正整数 将阻塞正整数时间
    区别 
        每次进行select和poll的时候都需要把规定的文件描述符拷贝到内核空间其中
        select是一个定长数组每次传输的时候都要初始化一次文件描述符，先将三个文件描述符初始化，然后将指定的文件描述符绑定进去
        而poll是一个链表所以可以一直增长。 之后操作系统进行检查将就需的文件进行标记，然后返回给你全部数据，
        你再从全部数据进行检查看看那些有就绪的标记，就处理那些文件。
        epoll就不需要，三个步骤在内核空间建立一个数据结构，用ctl进行内核空间的描述符添加删除等操作，
        wait之后操作系统返回就绪的数据
        为了防止使用边缘触发的情况下可能出现的程序饿死情况(一个程序有很多I/O导致其余程序很久之后才能运行)，
        可以使用轮转的方式操作一段时间就轮转一下，或者当出现这种情况的时候就将timeout设定为很小或者0，这样就可以快速处理程序
    
            


"""


print(1 << 1)