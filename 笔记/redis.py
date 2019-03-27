"""
redis:
    在 usr/local/bin中
    ubuntu@VM-0-17-ubuntu:/usr/local/bin$ redis-server /home/ubuntu/myredis/redis.conf
    ubuntu@VM-0-17-ubuntu:/usr/local/bin$ redis-cli -p 6379

    redis 已经不是ACID了
    C 强一致性  数据不变提交什么是什么
    A 可用性    必须能用不会崩溃
    P 分区容错性
    在CAP的理论上一般是不会满足三个的，一般都是满足两个
    CA 单点集群 满足一致性可用性的系统 一般在可扩展性不太强    一般是我们传统的关系型数据库
    CP 满足一致性 分区容错性的系统一般性能上不太强
    AP 满足可用性 分区容错性的系统一般对 一致性要求不高  Nosql一般对分区容错性的要求是必须的

    redis  支持数据的持久化 可以将在内存中的数据保存在磁盘中等待下次重启后重新使用
            支持备份  除了k v键值对以外还包含了各种数据结构

    redis 是单进程处理
        通过epoll函数封装，redis的效率主要是看主进程的效率
        默认redis的配置是有16个数据库的这个情况下 使用select 数字可以切换到对应的数据库

    常用操作
        get key
        select 切换数据库
        dbsize 查看当前数据库的key的数量
        flushdb  清空当前库
        flushall 删除所有库
        exists key  判断某个key是否存在
        ttl key  查看key是否过期 -1表示永不过期  -2 表示已经过期  当一个数据已经过期的时候就将数据从数据库中移除
        type key 查看key是什么类型
        expire key 给key设置过期时间
        move key db 移动到对应库

    当出现key值相同的数据的时候会覆盖数据库原有的值

    平常我们总是将redis称为字典型的数据库,但是其实不是这样的redis其实内置了五种数据结构。
    其实这里也和我们平常进行编程相似选择不同的数据结构进行不同操作。
    string
        set/get/del/append(追加字符串在key的值后面  相当于字符串拼接)/strlen(返回长度)
        incr key(加1)/decr(减1)/incrby key val(这个直接在对应的val上加上你输入的值)
        decrby key val(这个直接在对应的val上减去你输入的值)
        上面这些命令要val是数字的时候才能用
        getrange key start end (有点类似字符串切片返回start到end的string值)
        setrange key 数字 值(将字符串从对应数字下标的位置开始插入值，如果内部对应下标的地方有值则直接覆盖如果只有5个字母
        插入位置却是10那么中间的空位补占位符\x00)
        setex key 秒 val  创建时直接设置过期时间
        setnx key val  这个设定值主要是内部没有这个key的时候用来设定值如果内部有的话这个语句无效
        mset key val key val key val key val 用来一次性设置多个键值对
        mget key key key  用来一次性查找多个键值对
        msetnx  key val key val  用来一次性设置多个未存在的键值对，如果其中有一个键值对存在那么整条语句失效
        set (key)hello (value)world
        get hello
            (返回) world
    list   底层实际上是链表
        lpush list-key item  进出顺序  进 1 2 3 4 5  （0 -1）5 4 3 2 1
        rpush list-key item           进 1 2 3 4 5   （0 -1）1 2 3 4 5
        (integer)1
        rpush list-key item1
        (integer)2
        lindex list-key 下标  查看该下标元素
        "item"
        lpop list-key 左删除
        rpop list-key 右删除
        llen list-key 查看长度
        lrem list-key 个数 val  删除固定个数的val 如果删除数量超过列表中存在的值就直接删完
        ltrim key start end   将原列表的值截出来然后重新赋值给原列表  如果长度超过原列表那么直接将原列表重新赋值
        rpoplpush list-key1 list-key2  将第一个列表rpop 第二个列表将这个值lpush
        lset list-key index val  将目标列表对应的值进行修改
        linsert key before/after 值1 值2   将值2插入到值1的前或者后
    set
        sadd key val val  可以添加值到set中可以同时添加多个值
        smembers key 展示对应key的val
        sismember  key val  判断对应的key中是否有对应的val
        scard  key  获取集合中的元素个数
        srem key val  删除对应的val
        srandmember key 整数  从对应的key中随机出几个数 如果超出元素总个数那么就弹出所有的元素、
        spop key 整数 随机弹出整数个值
        smove key1 key2 val  将key1中的val移动到key2
        sdiff key1 key2 差集
        sinter key1 key2 交集
        sunion key1 key2 并集
    hash
        在哈希中kv键值对不变但是内部的 v 也是一个键值对
        hset hash-key  key val  新增单个哈希
        hget hash-key  key      查找单个哈希中的一个值
        hmset  hash-key  key val  key val  key val  可以同时增加单个哈希中的多个值
        hmget  hash-key  key  key  key   可以同时查找单个哈希中的多个值
        hgetall  hasn-key  无需key 直接列出所有哈希的 key val
        hdel  hash-key key   删除哈希中的单个哈希值
        hlen  hash-key  查看对应哈希中有多少个键值对
        hexists  hash-key key  查看对应的哈希中有有没有这个key
        hkeys hash-key  查看对应的哈希中所有的keys
        hvals hash-key  查看对应的哈希中所有的val
        hincrby hash-key key 整数  将对应的key中的数加上整数 如果没有key的话创建一个新的key val的值为整数
                                    如果对应的key的值不是整数的时候报错(是浮点数也会报错)
        hincrbyfloat  hash-key  key 浮点数  将对应的key中的数加上浮点数 如果没有就创建
        hsetnx hash-key key val  如果hash-key中没有这里的key的时候创建一个新的kv 如果有那么就什么也不做
    zset  有序集合
        在set的基础上增加了score值 zset k1 score1 v1 score2 v2 score3 v3
        zadd k1 score1 v1 score2 v2 score3 v3  创建
        zrange 0 -1 (withscores)   显示所有的 v1 v2之类的  如果加上括号里面的就显示包含score的zset的所有值
        zrangebyscore key 开始数值  结束数值   显示开始数值到结束数值之间的val 特殊使用方法(60 (90 大于60 小于90
                                                60 90 大于等于60小于等于90   limit 2 2 从下标2开始截取两个
        zrem key 某个score下面对应的val  删除这个元素包括前面的score
        zcard key  得到对应key的数量(一个score val 算是一个值)
        zcount key score区间 得到对应score区间的值的数量
        zrank key val  获取下标值
        zscore key val 获取对应的分数
        zrevrange key  获得逆序的range

    flushdb删除所有数据

    数据库我们使用简单的数字来进行标记这里使用 select 1 可以切换到不同的数据库。
    select 0 切换回默认数据库。

    set users:leto "{name: leto, planet: dune, likes: [spice]}"
    存储数据
    get users:leto
    读取数据

    查询:
        对于这种Redis关键字是一切,只能通过关键字来寻找值,不能通过值来找关键字。在Redis中
        是不会管值是什么的因为Redis不需要理解或者读取它
    变更情况:
        默认情况下，如果1000个或更多的关键字已变更，Redis会每隔60秒存储数据库；
        而如果9个或更少的关键字已变更，Redis会每隔15分钟存储数据库。
        Redis的数据默认是存储在储存器中的。
    Redis:
        Redis有五个数据结构,我们通过不同的命令来对操作数据库,比如set是将值存在字符串的数据结构中
        hset是将值存储到散列表中

    strlen <key>能用来获取一个关键字对应值的长度；
    getrange <key> <start> <end>将返回指定范围内的关键字对应值；
    append <key> <value>会将value附加到已存在的关键字对应值中（如果该关键字并不存在，则会创建一个新的关键字-值对）
    字符串数据结构被常用来缓存数据

    散列:
        hset users:goku powerlevel 9000
        设置一个散列值
        hget users:goku powerlevel
        读取它
        hmset users:goku race saiyan age 737
        同时设置多个key-value
        hmget users:goku race powerlevel
        同时读取多个key-value
        hgetall users:goku
        读取所有数据
        hkeys users:goku
        读取所有key
        hdel users:goku age
        删除数据

        当你想通过不同的键值来获取查询相同的值的话这对于空间十分不友好,因为要储存两次,而且对于数据管理也十分不友好,
        这里我们可以使用散列数据结构来更改他
        set users:9001 "{id: 9001, email: leto@dune.gov, ...}"
        hset users:lookup:email leto@dune.gov 9001

    列表:
    集合:
        集合数据结构常常被用来存储只能唯一存在的值，
        并提供了许多的基于集合的操作，例如并集。集合数据结构没有对值进行排序，
        但是其提供了高效的基于值的操作。

    分类集合:
        相比于普通集合提供了排序标记
    redis是单线运行的但是我们可以开启多个客户端进程所以还是会出现常见的并发问题

redis  配置文件
redis 持久化
    rdb  redis database
        在指定的时间间隔内将内存中的数据写入到磁盘中
        它恢复时是将文件直接读取到内存中

        redis 单独创建一个进程(fork)来进行数据的持久化，会先将数据写入到一个临时文件中待持久化过程都结束了在用这个临时文件替换
        上次持久化好的文件整个过程中主进程不进行IO操作来保证性能  缺点是最后一次的持久化的数据可能会丢失，可能在持久化没有
        完成的时候断电这样的话最后一的数据就会丢失  在后台会偷偷地保存数据，而且在下一次打开的时候读取对应的数据进内存
        在shutdown的时候会直接生成新的临时文件进行替换所以可能会出现数据丢失  flushall和save都可以更新db文件
        save 其余操作全部阻塞先进行备份
        bgsave  异步备份 可以执行其余操作
        flushall 会生成空的备份文件 是无意义的
        将备份文件 dump.rdb移动到安装目录就可以使用备份
        适合大规模的数据恢复
        对数据的完整性和一致性要求不高的情况
        劣势
            如果意外被down掉的话会丢失最后一次的修改
            要开一个额外的新进程要用两倍的空间

        fork  创建一个与当前进程完全相同的进程，新进程的所有数据都和原来的进程相同，这个新进程作为原来进程的子进程

        三种保存策略
            15分钟有1个修改   就会触发 保存到磁盘
            5分钟有10个修改   就会触发 保存到磁盘
            60秒钟有10000个修改  就会触发 保存到磁盘
    aof  append only file
        通过日志的方式来记录下redis的所有操作，不包括读操作，这个时候每次从新启动redis的时候都读取这个文件按照上面的操作
        一步一步恢复整个redis(这个文件只许增加不许修改)
        如果该文件出现错误的话可以使用 redis-check-aof --fix 文件进行处理恢复成正常的没有语法错误的文件

    以上两种
        持久化的方式是不可以共存的 当两个文件同时存在的时候，以aof为主，默认使用aof来重新将数据读取到内存中，
        如果修改了aof文件 使内部出现错误的话可能会导致redis无法连接

        rdb可以在固定的时间间隔来对你的数据进行一次持久化，而aof是记录你的每条命令
        如果你只做缓存的话就不需要持久化的策略
        建议使用方法是同时开启两种策略 虽然开启两种策略是无法共存的redis会使用aof来恢复数据库，但是rdb可以明确的记录下
        你数据库的内容更加适合当做备份使用
redis事务
    一次性执行多个命令的集合  会按照顺序执行所有的命令不会加塞
    一个队列中顺序的一次性的排他性的执行一系列命令
    命令
        DISCARD  取消事务放弃事物内部的所有命令
        EXEC     执行事务块中的所有命令
        MULTI    标记一个事务块的开始
        UNWATCH  取消WATCH对key的监视
        WATCH    监视一个或者多个key如果这些key在执行命令之前被其他命令改动那么事务将会被打断
悲观锁乐观锁
    悲观锁每次拿数据的时候都会悲观的认为数据会被修改每次拿数据的时候都上锁直到数据修改结束之后再释放
    乐观锁每次拿数据的时候都乐观的认为别人不会修改自己的数据，这种锁使用版本号控制，每次提交的时候都会判断这个数据有没有被更新
    提交版本必须大于当前记录的版本
redis的发布订阅
    进程间的一种通信方式
redis主从复制
    SLAVEOF IP 端口号
    主机数据更新后根据配置和策略自动同步到备机  master/slaver  master 以读为主 slave以写为主
    作用
        读写分离  容灾恢复
    配从库不配主库 从库只能读 只要主库添加从库 从库就能会能够得到主机的所有的资源，主机如果挂了从机是无法成为主机的，
    只能等待主机重启 如果从机挂了重启的话如果在配置文件中没有配置那么会自动成为主机

    可以将一个从机当做一个主机给下一个从机复制数据，这样可以减少对于主机的压力。从机依旧是从机
    SLAVEOF IP 端口号

    SLAVEOF no one 反客为主  在主机挂掉的时候可以选择一个从机使用这个语句 将从机变成主机
                            其余从机可以选择 SLAVEOF IP 端口号 从新选择主机

    哨兵模式
        在自定义的myredis中新建sentinel.conf文件
        在这个文件中 插入一行 sentinel monitor 主库名 ip 端口 票数  结果是谁的票数大于这个谁会成为新的主机
        开启哨兵  在redis文件夹中使用 redis-sentinel   sentinel.conf的绝对路径     哨兵开启

"""