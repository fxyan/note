"""
系统配置
程序安装
PATH
命令
参数
权限
用户
用户组
gcc linux下的一个编译程序 是c程序的编译工具

linux系统级别
    0   关机
    1   单用户 [找回丢失密码]
    2   多用户状态没有网络服务
    3   多用户状态有网络服务
    4   系统未使用保留给用户
    5   图形界面
    6   系统重启
    系统的运行级别配置文件
        /etc/inittab
    切换到指定运行级别的指令
        init[0,1,2,3,4,5,6]从中选择一个


linux的文件目录结构
    linux是一个树状的目录层次最上层目录是 /    在linux中一切皆文件
    bin 常用的指令 例如cp之类的
    dev 将硬件映射成文件 cpu之类的
    etc 存放配置文件比如mysql什么的配置文件
    home 家用户 当你创建一个用户的时候就会产生一个对应的文件
    lib  静态库系统开机所需要的动态链接库 类似windows下面的DLL文件
    media 识别光驱u盘之类的媒体文件  识别一些设备
    opt 安装的软件会放在这里
    proc 内核的东西
    root root用户的文件
    sbin 高权限的用户使用的东西
    selinux linux下面的负责安全的目录
    usr 用户安装的文件什么的
    user/local 额外安装软件的安装目录
    var  不断扩展的东西都在这里 还有日志文件


vim文本编辑器
    h 向左移动
    j 向下移动
    k 向上移动
    l 向右移动
    o 在光标下插入一行
    x 删除光标下的符号
    dd 删除一行  5dd删除当前行开始的5行  使用方法类似嘛数字开头dd
    yy 复制一行 5yy拷贝当前行开始的下面5行 按p复制
    查找 /关键词 就能够找到对应的关键词(如果关键词有多个那么找到最顶端的词)  如果这个不是你想要的话按 n 可以找到该文档的下一个
        对应词
    显示行号/不显示行号: set nu 让文件显示行号   :set nonu 让文件不显示行号
    跳转到文件最后一行和第一行  输入G跳转到最后一行  输入gg跳转到第一行
    撤销输入  u 就可以
    让光标到达对应行号  在正常模式下 输入行号(数字)然后按shift+g跳转
    i 进入更改状态
    :w 写入磁盘
    :w! 当文件为只读的时候强制写入磁盘(能不能写入还是看你的权限)
    :q 离开
    :q! 强制离开不保存
    :wq 写入后离开
    :wq! 强制写入后离开

文本浏览器 less
    less的使用方法 less 文件名
    这样可以查看 j 上 k 下 q 退出
    --chop-long-lines  这种情况在水平的框较小的情况下行会乱，可以开启这个调整行
    / 加一些你要搜索的值可以只显示你要搜索的值

常用操作
.代表当前目录
..代表父目录

pwd
    print working dir
    显示现在所处的目录

ls
    不带参数就显示当前目录下的所有文件
    程序可以加参数
    -l 显示详细信息
    -h 人性化显示文件尺寸
    -a 显示所有文件， 以 . 开头的文件是隐藏文件
    -t 按照时间排序
    -r 反转排序
    还可以带一个目录当参数，这样就会显示这个目录
下面两个是等价的
ls -l -h
ls -lh

cd
    cd Desktop
    改变当前目录
    . 代表当前目录
    .. 代表上级目录
    cd 不带参数就回到默认的家目录
    每个用户都有一个家目录，默认在 /home/用户名
    root 用户的家目录是 /root

cp
    cp  /home/hello.txt /home/bbb  将hello.txt复制到bbb的目录下
    -v 添加正在做什么的的解释
    复制出一个文件，用法如下
    cp a.txt b.txt
    复制 a.txt 并把新文件取名为 b.txt
    复制目录要加上 -r 参数
    -r 递归复制整个文件夹
    cp -r a b
    当你覆盖一个目录的时候会有提示你要不要覆盖，这个时候如果你的目录中有多级目录的话，每覆盖一个重复的嵌套的文件系统都会
    提示你是否要覆盖，可以在命令前面增加一个 \ 来进行强制覆盖

mkdir [-mp] 目录名称
    创建一个目录
    -p 可以一次性创建多层目录
    -m 配置目录权限
    mkdir -p a/b/c
rmdir [-p] 目录名称
    只能用来删除一个空目录
    -p 递归删除目录
rm
    这个命令直接删除东西，很危险，一般不要用
    删除文件或者目录
    -f 强制删除不提示
    -r 用来删除目录递归删除目录
mv
    移动文件或者文件夹
    也可以用来改名
    mv a.txt b.txt
    mv b.txt ../
    mv b.txt ../gua.txt
    可以用 mv xx /tmp 的方式来将文件放入临时文件夹
    （/tmp是操作系统提供的临时文件夹，重启会删除里面的所有文件）
cat
    显示文件内容
    加上-n可以显示行号  通过 | more 可以使用分屏 按空格看下一屏
tac
    反过来显示文件内容
nl
    显示内容并附带行号
more less head tail
    more 可以分屏分批看文件内容  内置快捷键  空格向下翻页  回车向下翻一行  q表示离开more  =输出当前行号
            :f输出当前行号和文件名   crtl + b 返回上一屏
    less 比 more 更高级，可以前后退看文件   pageup  pagedown  空格是向下翻动下一页
                    /字串 向下搜索字串的功能  n: 向下查找 N: 向上查找
                    ？字串 向上搜索字串的功能 n: 向下查找 N: 向上查找
                    这里的大小写的n 就是查找一个字符串之后输入用来寻找到下一个或者上一个对应的字符串
    head 可以显示文件的前 10 行
    tail 可以显示文件的后 10 行
    head 和 tail 有一个 -n 参数
    head -n 20 a.gua
touch [-acdmt] 文件名称
    创建空文件
    -a 更新文件最后被的访问时间
    -c 更新文件权限等最后被修改的时间
    -m 更新文件被修改的最后时间
    touch a.gua
    如果 a.gua 存在就更新修改时间
    如果 a.gua 不存在就创建文件
echo
    echo $PATH 输出当前环境变量的路径
head
    head 文件名
    head -n x 文件名  x的值为一个数字代表你想看的行数
tail
    tail 文件名 ，默认显示文件的后10行
    tail -n x 和上面一样
    tail -f  实时追踪文档的更新  经常使用

ln
    生成一个软连接  相当于windows的快捷方式
    ln -s 原文件或目录 软连接名  这样生成了一个快捷方式 输入你的软连接名称直接跳转到对应的文件目录

时间日期类
    date                显示当前时间
    date + %Y           显示当前年份
    date + %m           显示当前月份
    date + %d           显示当前日期
    date  %H %M %S        时 分 秒  这几个日期的子母是固定的记住就行
    date "+%Y %m %d  %H %M %S"
    date -s   用来设置系统时间

    cal 日历  显示当前日历

压缩和解压缩
    gzip 文件名     压缩文件  将文件进行压缩之后不会保留原文件
    gunzip 文件名   解压文件  将文件解压缩之后不会保留原文件

    zip         压缩文件   -r 递归压缩压缩整个目录
        zip [选项] xx.zip  要压缩的内容
    unzip       解压文件  -d目录 表示要将文件解压到的位置
        unzip [选项] xx.zip

    tar 打包指令可以通过参数来进行解压和压缩
        tar [选项一般打包的话直接组合拳 -zcvf 解压的话直接-zxvf] xxx.tar.gz  要进行压缩或者解压的文件
        -c  产生.tar打包文件
        -v  显示详细信息
        -f  指定压缩后的文件名
        -x  解包.tar文件
        -z  打包同时压缩

目录分布



用户管理
    添加用户
        useradd [选项] 用户名
        当你没有指定新用户的组的时候，就会创建一个新的和新用户同名的组将新用户放进去
        useradd -d 指定目录
        useradd -g 用户组 用户名 将新的用户指定到你想要的组中
    给用户指定密码
        passwd   用户名
    删除用户
        userdel 用户名   这种是普通删除法单单删除对应的用户不删除家目录的分组文件夹
        userdel -r 用户名  会删除对应home文件夹的用户所在的分组目录
        在删除用户时尽量保存家目录
    修改用户组
        usermod -g 用户组 用户名
    查询用户信息
        id 用户名  如果没有对应的用户会返回无此用户
    切换用户
        su - 用户名
        返回原先用户 exit
        高切低不需要密码  低切高需要密码
    如何找回root密码
        进入单用户模式修改root密码  因为进入单用户模式root不需要密码就可以登录
用户组
    类似一个角色对有共性的多个用户进行统一的管理
    新增组
        groupadd 组名
    删除组
        groupdel 组名

权限操作
sudo
    用管理员帐户执行程序
    比如安装程序或者修改一些系统配置都需要管理员权限
su
    switch user， 切换用户
    su gua
    su root

文件权限    文件类型 用户 用户组 文件大小  修改日期     文件名
-rw-rw-r--  1       gua gua     10      11/09 20:28 b.gua
drwxrwxr-x  2       gua gua     4096    11/09 20:28 tmp
文件类型    是否可读  是否可写  是否可执行
d           r       w           x
-           r       w           x
文件类型 d 目录 - 普通文件  l 软连接  c 字符设备  b 块文件 硬盘
三组 rwx 分表代表 所属用户|同组用户|其他用户
rwx 可以用数字表示为 421
上面的三个权限对于文件和目录有不同的意义
       文件  r  可读
             w  可修改，但是不一定可以删除，如果想删除的话要有对该文件所在的目录有写权限才能删除
             x  可执行
       目录
            r  可读
            w  可修改 目录内部删除 创建 重命名
            x  可进入该目录
于是乎
r-- 就是 4
rw- 就是 6
rwx 就是 7
r-x 就是 5

chown
    改变文件的用户  加个-R可以递归的将目录中所有文件全部改变 下面全部有效
    chown gua:用户组 c.gua  同时改变组和用户
    chown gua:gua c.gua
chmod [-ugoa]
    改变文件权限
    u 拥有者
    g 所属群组
    o 其他人
    a 所有人
    chmod 666 root.gua
    chmod +x root.gua
    chmod a+x root.gua
    chmod -x tmp
chgrp
    修改文件所在的组
    chgrp 组名文件名

信息查找
file
    显示文件的类型（不是百分之百准确）
uname
    显示操作系统的名字或者其他信息
    uname -r
    uname -a
which
    which pwd
    显示 pwd 的具体路径
whereis
    whereis ls
    显示更全面的信息
whoami

find
    -name 文件名
    -user 使用者
    -size 大小
    find /home(查找范围) -name hello.txt(查找对象)

locate
    快速定位文件位置，因为这个命令使用了内部自带的数据库进行查找所以速度会相当快
    但是缺点是要求定期维护内部的数据库  在第一次使用的时候先输入 updatedb创建数据库
    loacte 文件名  会显示文件的位置

奇怪符号
~   家目录快捷方式
>   覆盖式重定向
>>  追加重定向
|   管道, 将前一个命令的结果输出传递给后面的命令处理
``  获取命令执行的结果
&   后台执行
    python3 server.py &
    可以用 fg 命令把一个在后台的程序拉到前台来
    可以用 Ctrl-z 来把一个前台的程序放到后台去挂起
()  开新的子进程shell执行(不用掌握这一条, 因为几乎没人用)


history
    查看历史命令
grep
    查找
    -n  显示匹配行及行号
    -i  忽略字母大小写
    xxx | grep -ni yes   查找xxx中有没有yes有的话显示行号
这两个一般配合使用
    history | grep touch

任务调度
    crontab  -e 编辑   -r 删除  -l查询
ps
    查看进程, 一般用下面的用法
    -a  显示终端的所有信息
    -u  以用户格式显示终端所有信息
    -x  现实后台进程运行的参数
    -e  显示所有进程
    -f  全格式
    ps ax
ps ax | grep python
    查看带 python 字符串的进程

kill 和 killall 杀进程
    用 ps ax 找到进程id (pid)
    kill [pid]
    kill -9 [pid]
    kill -15 [pid]
    killall 是用进程名字来杀进程  将所有重复进程全部关闭

后台前台
fg
jobs

快捷键
C-z 挂起到后台
C-c 中断程序



reboot
    重启
shutdown
    关机
    可以用参数指定时间
    shutdown -h now 现在关机
    shutdown -h 1   一分钟后关机
    shutdown -r now 立刻重启
halt
    关机
sync 将内存中的数据同步到磁盘上 在关机或者重启之前使用保存数据
logout  注销用户



====

# ssh-key 的概念和使用
#
# 1. 生成 ssh id_rsa.pub
ssh-keygen

# 2. 普通用户把 public key 添加到~/.ssh/authorised_keys
##  root用户把 public key 添加到 /root/.ssh/authorised_keys
cat id_dsa.pub >> ~/.ssh/authorized_keys

# 3. 重启 ssh
service ssh restart


软件安装
====
apt-get install 软件名
比如下面
apt-get install python3


====

# 安装防火墙 和 防火墙的基本套路配置
# 防火墙的作用(redis安全漏洞)
apt-get install ufw
ufw allow 22
ufw allow 80
ufw allow 443
ufw allow 3000
ufw allow 8089
ufw default deny incoming
ufw default allow outgoing
ufw status verbose
ufw enable
"""
# shell
"""


"""
