"""
redis:
    平常我们总是将redis称为字典型的数据库,但是其实不是这样的redis其实内置了五种数据结构。
    其实这里也和我们平常进行编程相似选择不同的数据结构进行不同操作。
    string
        set (key)hello (value)world
        get hello
            (返回) world
    list
        rpush list-key item
        (integer)1
        rpush list-key item1
        (integer)2
        lindex list-key 1
        "item"
    set
    hash
    zset


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
"""