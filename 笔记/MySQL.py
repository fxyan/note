"""
MySQL的索引
    一般都是两种实现，哈希表和B+树
    哈希表
        正常寻找数据不使用索引的话都是一行一行的去找十分慢使用索引就像是使用哈希表一样快捷，
        哈希表将你建立索引的值为key，实际地址为value来进行查找。
    B+树索引:
        每个节点的大小都是页的倍数(一页就是磁盘I/O一次能读取的数量)
        为什么使用B+树而不使用B树呢，因为B树在每个节点都会储存数据，这样的话每个节点存储的key就变少了，树的高度增加了
        总体来说磁盘的I/O也就变多了，而且B树因为每个节点都储存数据导致没有B+树这样的链表来串连数据，所以在获取一大块数据的
        时候也显得没有B+树效率高
        而B+树只有在叶子结点才会储存数据
    MylSAM:
        索引和数据是分开的两个文件
        从索引中找到数据地址，再去找到数据
        辅助索引和主索引几乎没什么区别
    innodb:
        使用主键索引，辅助索引返回的是主键值，再返回到主索引去查找数据
        数据也挂在叶子结点下面，不和索引分开
    索引优化
        最左前缀优化:
            因为有的时候你建立索引是按照多行来建立的，索引表也是多行的
                        学科 时间 姓名
            可以使用三列一起来进行索引数据(因为MySQL索引优化器这三列顺序和建立索引的顺序不同也是没问题的)

            如果你只有 学科 姓名 这两列的时候索引，只能按照学科来匹配，因为不知道中间的时间是什么，可以选择建立一个辅助索引
            只包含 学科 姓名

            也可以使用填坑办法，如果 时间 这一列数据比较少的情况下可以用
            学科 AND 时间 IN (XXX, XXX, XXX, XXX) AND 姓名
            这种方式来进行索引(不过如果说时间的列实在太多那性能可能提升不大了)

            查询时没有索引的第一列，无法使用索引

            如果你是用LIKE '%xx'的时候如果 % 不在开头可以使用到索引，如果在开头无法确定你搜索的第一个字符是什么，
            自然也没办法使用索引

            范围查询 学科 < xx 这种情况可以使用到索引，但是范围列后面的无法使用索引 必须最左前缀
            注意 BETWEEN 在MySQL中属于多值精确匹配所以后面的列依然可以使用索引

            某些列包含函数或者表达式这些列不能使用索引
        回表，select 学科 from 如果学科就在索引中就不需要返回原始的表进行搜索了，这样也可以提高效率(尽量少用select *)
        索引选择性 如果一列中的重复率太高不适合建索引可以使用 distinct(xx) / count(*) 来查看百分比，百分比太低就是浪费时间

"""

# 基操
"""
字符串和日期用''括起来
表名  列名  关键字不区分大小写
但是关键字习惯的使用大写

创建表的时候一般使用的四个基础类型
    INTEGER(integer)
        整数
    DATE
        日期
    CHAR(长度)
        字符串，但是这里字符串创建的时候会给一个长度，如果没达到长度的话会给一个空格填充字符串
    VARCHAR(长度)
        可变长度的字符串，如果输入的东西没达到长度的话也不会增加空格进行填充

    约束创建数据的时候也会有一些约束在的比如
        NOT NULL
        PRIMARY KEY (product_id)设置主键
语句
    CREATE DATABASE (数据库名称)
    CREATE TABLE 表名(详细的每个列)
    DROP TABLE 表名
    ALTER TABLE 表名 ADD COLUMN 列的定义
    ALTER TABLE 表名 DROP COLUMN 列名
    INSERT INTO 表名 VALUES (数据)
as 设置别名
    设置别名的时候可以使用中文但必须遵循下面的格式
        "你想指定的中文别名或者整数"
    还可以直接使用计算式算出数值来AS
DISTINCT
    去掉一列中的所有重复行，NULL也被视为重复行只显示一个

WHERE
    紧跟在FROM后面
    条件表达式用来过滤数据
    先经过条件表达式得到行的备选结果，然后再从select的列数据中进行选择
    WHERE sale_price - purchase_price >= 500
    总之也能用这种东西很方便
    不能使用聚合函数


运算表达式和比较运算符
    + - * / 和正常使用没有区别也可以用括号进行
    四则运算如果有NULL全部是NULL
    < <= > >= <>(不等于也可以用 !=)

逻辑运算符:
    NOT,正常用法，可以使用在WHERE里面
    对于NULL这种特殊类型，不支持使用比较运算符的，可以使用人性化的方法比如 IS NULL  或者  IS NOT NULL
    AND
    OR
    使用方法和变成上面是一样的，但是有一个规则，AND优先级要大于OR
    A AND B OR C
    实际上是
    (A AND B) OR C
    所以想要使用的时候加上()来进行使用
    在SQL中除了真和假还会出现不确定的情况，对NULL进行逻辑运算就会出现这种情况，尽量不要出现NULL,比如加上NOT NULL的约束

字符串排序
    字符串并不会像整数一样进行排序，而是像字典一样
    '1'  '2'  '222' '3' '11'
    排序之后是
    '1' '11' '2' '222' '3'
    进行大小比较的时候也是按照这个来排序

聚合函数
    可以在函数内部使用DISTINCT
    对于聚合函数在接收列名当做参数的时候就已经将NULL排除在外了所以可以进行计算。
    COUNT:在聚合函数中独有的COUNT(*)其余聚合函数不能(*)，他返回所有的行数。COUNT(列名)就不同，
            比如说你有两行是NULL 那么就返回总行数-2。
    MIN
    MAX
        原则上适用于所有类型
    SUM
    AVG
        一般适用于数值类型
    只有SELECT HAVING ORDER BY子句中可以使用聚合函数

其余函数
    ABS(0)
    MOD()
    ROUND()
    LENGTH()
    LOWER()
    REPLACE()
    SUBSTRING()
    UPPER()
    CURRENT_DATE()
    CURRENT_TIME(0)
    CURRENT_TIMESTAMP













    SELECT id, user_id, score, term
    FROM ?
    COURSE = '数学' AND (SELECT user_id
                                FROM p2
                                WHERE COURSE = '语文' AND score > 90 and p1.term = p2.term)


   WHERE COURSE = '语文' AND score > 90 AND()













    LIKE 是一种模糊查询的方法用来查询匹配字符串
        LIKE 'DDD%'/'%DDD%'/'%DDD' 就是已经知道了三个字母是DDD 希望能够得到所有和这个匹配的数据 前中后都可以
        使用 __ 也是模糊查询的方法但是确定了有几个字符的长度不像上面可以是无线长度的
分组 GROUP BY
    四个注意(聚合函数和GROUP BY)
        必须写在SELECT 子句中
        WHERE无法使用聚合函数
        GROUP BY 出来的数据是无序的
        GROUP BY 无法使用SELECT的别名
    使用GROUP BY 函数的经典错误:
        在SELECT 中多写了GROUP BY中没有的行
        这样会导致数据按照GROUP BY进行了分组之后多余的行和进行的分组不是一一对应的关系导致数据出错
        列子
            SELECT price，name
            GROUP BY price;
            你分组之后 价格为2800元的有玩具和显卡,你分组只有一行不知道怎么应对两个值

        GROUP BY中使用了SELECT AS的别名
            错误原因:因为在数据库执行语句的时候顺序是GROUP BY 在前的所以这样写无法识别
            虽然在MySQL里面没有报错，但是还是不应该使用

        GROUP BY 语句的数据得出来的是随机的，你再次运行顺序不一样，想要排序从SELECT里面排序

    分组处理将表中的数据按照你的SELECT进行分组，也会将NULL进行分组
    写在FROM 后面
    如果有WHERE 写在WHERE后面
    有GROUP BY的时候的语句执行顺序
    FROM -> WHERE -> GROUP BY -> SELECT

HAVING
    写在GROUP BY 后面
    不能使用别名
    用于给分组进行筛选，类似于WHERE
    使用的三要素
        常数
        聚合函数
        GROUP BY 指定的列
    书写顺序
        SELECT -> FROM -> WHERE -> ORDER BY -> HAVING
    HAVING是对组进行操作
    WHERE是对行进行操作
    有的时候对两个值进行不同的操作可以得到同样的结果，推荐使用WHERE，因为在使用聚合函数的时候内部会对行进行排序，
    这样的话行越少排序的负担越少，执行的也就越快。如果使用HAVING是在排序结束之后再进行分组，不能减轻排序的负担
    另外一个原因是使用WHERE可以对对应的列创建索引，大幅度提升速度。

ORDER BY
    一般写在末尾
    默认是ASC升序 指定DESC是降序
    指定一个排序键可以就这一列排序，但是当这一列出现数值相同的行的时候那几行就会随机排列，所以可以选择多个排序键来进行排序
    如果有NULL的时候，一般会汇集在末尾或者开头
    ORDER BY可以使用别名,原因就是内部的语句执行顺序
    可以使用SELECT中不存在的列和聚合函数
    书写顺序
        SELECT -> FROM -> WHERE -> GROUP BY -> HAVING -> ORDER BY
    执行顺序
        FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY

INSERT:
    对于NULL也是一视同仁 直接插入就行了，注意是否会有NOT NULL约束
    设定默认值的时候DEFAULT 可以选择直接给该列赋值DEFAULT 或者直接不给这个列赋值，这样的话就是使用了默认值
    插入数据
        INSERT INTO 表名 (列名 列名...) VALUES (数据)
        在插入的数据正好是全部列的数据的时候也可以省略列名，但是使用了列名的时候，数据和列名不能够不一致
    多行INSERT
        INSERT INTO 表名 (列名) VALUES (数据)，(数据)，(数据)这样可以省略INSERT INTO 只一行就插入多行数据。

DELETE:
    可以使用DROP TABLE 表名 来删除表
    使用DELETE 来删除数据，因为DELETE删除的是行，所以没办法指定列名或者 *
        DELETE FROM 表名
    使用WHERE来进行选择性删除
    TRUNCATE
        也是一种删除的办法，但是这个是不可控的删除整个表的数据，所以运行的时候会快一点。使用的时候要谨慎

UPDATE:
    UPDATE 表名
    SET 列名 = 表达式
    WHERE 条件
    合并多条UPDATE语句
        UPDATE 表名
        SET 列名 = 新的值，列名 = 新的值....
        WHERE 条件

事务
    事务都是用 事务开始语句和事务结束语句包起来的
        START TRANSACTION;
            事务
        COMMIT/ROLLBACK;
    在MySQL中一般都是自动提交事务的，写的一般语句都默认是已经被一个事务包裹，如果在自动提交的状态下DELETE了数据，那么
    就无法回滚了，必须要自己写一个ROLLBACK这样的事务才能回滚。

数据库事务的四种特性
    原子性:
        事务的操作，要么全部执行，要么全部不执行，不能出现只执行一半的操作
    一致性:
        对于事物的操作要符合数据库的约束，如果出现了不符合约束的情况就把他回滚
    隔离性:
        对于一个事务而言，在他没有执行完之前对于其余的事务是透明的，别人无法干扰你的操作
    持久性:
        就是当事务提交或者回滚之后，能够保证数据可以持久的被保存住，一般都是在硬盘中记录日志来进行数据的持久化，
        当发生故障的时候通过日志来进行数据的恢复

视图
    视图就是将SELECT语句进行储存形成一个新的表，而且这个表会自动随着数据更新而更新，
        CREATE VIEW productsum (type, count)
        AS
        SELECT product_type, COUNT(*)
        FROM product
        GROUP BY product_type
        这样就形成了一张视图保存的是上面SELECT语句进行搜索的结果，有了这张视图在你想要搜索同样的结果的时候就不需要
        再次输入SELECT了
    删除DROP VIEW
    子查询
        其实就是就是一次性的视图了
        使用方法也很简单
        SELECT type, count
        FROM (
            SELECT product_type, COUNT(*)
            FROM  product
            GROUP BY product_type
            ) AS productsum
        效果是一样的， 作为被嵌套的查询子查询是先被执行的，除了这种简单的用法还有很多实际的用法，比如在WHERE语句中
        是无法使用聚合函数的如果想要销售价格大于平均价格的数据     WHERE price > (SELECT AVG(price) FROM product)
        这样可以实现功能，
        子查询只能返回一行

        你想得到每个类型中销售价格大于平均价格的商品，使用下面的关联子查询。
        SELECT product_type, product_name, sale_price
        FROM product AS P1
        WHERE sale_price > (SELECT AVG(sale_price)
							FROM product AS P2
							WHERE P1.product_type = P2.product_type
							)
	    关联子查询的详细使用
	    这种标量子查询可以返回一个多行的数据





启动等核心操作:
    mysql -u 用户名 -p; 启动
    CREATE DATABASE 库名; 创建数据库
    USE 库名; 选择数据库使用(这里一般返回Database changed表示成功)
    创建用户:
        CREATE USER 'username'@'host' IDENTIFIED BY 'password';
        'username':用户名
        'host':指定用户可以在那里登录本地可以使用localhost
        'password': 密码
    重命名:
        RENAME USER 'username'@'host' TO 'username'@'host';(本地用户改为localhost)
    删除用户:
         DROP USER 'username'@'host';
    授权用户:
        GRANT privileges ON databasename.tablename TO 'username'@'host'
        privileges: 权限如果想要所有的权限的话使用ALL
        databasename: 数据库名
        tablename: 表名
    更改用户密码:
        SET PASSWORD FOR 'username'@'host' = PASSWORD('newpassword');
        当前用户
        SET PASSWORD = PASSWORD("newpassword");

    show操作:
        show databases; 显示所有可用数据库
        show tables; 显示数据库里的表
        show columns from 表名; 显示表的具体数据(describe(形容描绘) 表名 也可以当做快捷使用)
        show status; 显示服务器状态信息
        show grants; 显示授予用户的安全权限
        show errors/warnings; 显示服务器错误或者警告

操作数据库语句:
    操作语句的顺序:
        SELECT
        FROM
        WHERE
        GROUP BY
        HAIVING
        ORDER BY
        LIMIT

    select:
        select 列名 from 表名, 检索多个列的话要在列中间加逗号, 检索表中所有列的话 * 就行了
        select distinct 列名 from 表名, 可以只返回不同值的列,
        这个不能部分使用会作用到后面所有列(但是如果有一个表的数值重复的少那么就会显示相同的行数)

    limit 限制语句:
        (位于order by之后)
        select 列名 form 表名 limit 数字(开始查找的行数 2 之后需要查找的行数 3 )找出来的就是 3 4 5行
        返回数字的行数也可以使用括号里的行数查找法
        检索出来的第一行是0行所以(1, 1)是第2行 行号是1
        表名也可以写得十分完整

    order 排序语句:
        按字母顺序排列
            select 列名 from 表名 order by 列名

        多行排序是和多行select是一样的

        order by是后面的行按照第一行来进行排序
            order by name, price
            先排序name,然后price按照排序的name再排序。
            如果name的值全部唯一那么price就不用再排序了

        默认是升序排序desc是降序排序可以转换
            select 列名 from 表名 order by 列名 desc
            只对单列有效,多列要加多个desc

    WHERE 过滤条件:
        (位于order by之前)
        SELECT 列名 from 表名 where 列名=xxx(xxx为我们检索的过滤条件值)
        where有很多指定方式 = < > !=等等    <>含义是不相等
        between(在指定的两个值之间):语法
            between 3 and 5
        在这里有些不同NULL的列在匹配过滤和不匹配过滤的时候不返回他们,所以在检测数据的时候
        要确定NULL的值有没有返回
        AND OR 就和普通编程使用的一样增加过滤条件:
            WHERE (vend_id = 1002 OR vend_id = 1003) AND prod_price >= 10;
        优先级可以使用()分隔
        IN:
            HWERE vend_id  IN (1001, 1002)
        NOT 普通使用方法:
            HWERE vend_id  NOT IN (1001, 1002)
        LIKE通配符一种搜索模式:
            %:
                WHERE prod_name LIKE 'jet%';
                这样可以搜索jet开头的所有数据
                WHERE prod_name LIKE '%anvil%'
                anvil 这样就无法匹配
                可以两边都加%
                WHERE prod_name LIKE 's%t'
                也行
                空格会干扰通配符,NULL不会被返回
                (这里注意一下不同的MySQL会有不同的设置,有的时候会区分大小写)
            _:
                这里的_和%的效果是一样的就是_只能匹配一个字符 不像%可以匹配0个字符
                _十分死板。
                WHERE prod_name LIKE '_ ton anvil'
            通配符注意点:
                尽量不要过度使用通配符,因为通配符搜索是很慢的
                在使用通配符的时候尽量不要放在搜索的开始,因为这样是最慢的

    计算字段:
        Concat:
            拼接不同的列产生不同的结果,比如同时返回两个列的结果
            SELECT Concat(name, '(', country,')')
            返回效果:
                jet (USA)
        去左右空格:
            去右空格RTrim(左空格LTrim, Trim去两边空格):
                SELECT Concat(RTrim(name), '(', RTrim(country), ')')
        创建别名:
            SELECT Concat(RTrim(name), '(', RTrim(country), ')') AS title
            可以将查询出来的数据建成一个列方便使用和注释
        使用运算符:
            +-*/四种运算符都可以使用
            SELECT prod_id, quantity * price AS expanded_price
            返回的列表中expanded_price是计算字段 quantity 和 price的乘积

    函数:
        RTrim(): 去掉右空格
        LTrim(): 去掉左空格
        Trim(): 去掉两边空格
        Left(str, length): 从str字段从左截取length位
        Right(str, length): 从str字段从右截取length位
        Upper(): 全部大写
        Lower(): 全部小写
        Abs(): 绝对值

    日期:
        日期格式请遵循
            xxxx-yy-mm
        Data():返回日期
        Time():返回时间
        Year():返回 年
        Month():返回 月

    聚合函数:
        COUNT(): 返回某列的行数
            如果返回指定的列那么忽略NULL *例外返回所有值
        AVG(): 返回某列的平均值
            通过WHERE 语句也可以返回特定一行或者几行的平均值
        SUM(): 返回某列值的总和
        MAX(): 返回某列的最大值
        MIN(): 返回某列的最小值
            忽略NULL
        获取不同的值:
            DISTINCT
            在上面进行聚合的时候默认参数其实是ALL的代表所有参数
            但是可以指定DISTINCT 表示只选用不同的值
            案例:
                SELECT SUM(DISTINCT price)
                FROM product;

    分组:
        (在WHERE之后, ORDER BY之前)
        GROUP BY:
            SELECT vend_id,COUNT(*) AS num_prods
            FROM products
            GROUP BY vend_id;
            这样会导致COUNT不会对整个列进行计算,而是针对vend_id进行了分组计算,对每一个
            vend_id都进行了一次计算返回结果类似
            vend_id | num_prods
            1001    |         3
        HAVING:
            简而言之:
                WHERE是在分组前进行过滤筛选可以进行分组的数据
                HAVING是在分组后进行筛选
            HAVING其实就是和WHERE是一样的效果,但是不同的是前者是过滤分组后者过滤行。例子:
            SELECT vend_id,COUNT(*) AS num_prods
            FROM products
            GROUP BY vend_id
            HAVING COUNT(*) >= 2;

    子查询:
        可以使用
            SELECT vend_id,COUNT(*) AS num_prods
            FROM products
            GROUP BY vend_id
        来当做查找条件
        (嗯 就这样)
        可以使用自联结来代替的

    联结表:
            这样就是联结了两个表的同一行来进行查找 找vend_id的行来对应两个表。
        可以同时联结多个表。
            SELECT vend_name, prod_name, prod_price
            FROM vendors, products
            WHERE vendors.vend_id = products.vend_id
            ORDER BY vend_name, prod_name;

        使用 INNER JOIN 是更加规范的联结方式,而且可以可能会影响性能
            SELECT vend_name, prod_name, prod_price
            FROM vendors INNER JOIN products
            ON vendors.vend_id = products.vend_id

        左右联结:
            左联结以左表为基本匹配右表,如果左表有的行而右表没有对应的行就返回NULL来对应
                LEFT OUTER JOIN
            右联结和上面相同
                RIGHT OUTER JOIN

    组合查询:
        UNION:
                SELECT vend_id, prod_id, prod_price
                FROM products
                WHERE prod_price <= 5
                UNION
                SELECT vend_id, prod_id, prod_price
                FROM products
                WHERE vend_id IN (1001, 1002);
            在两个SELECT中间夹杂着UNION 这样可以组合查询,
            (使用条件上下两组SELECT 必须具有相同的列、表达式和聚合函数)
            UNION 默认是不返回重复行的,可以使用UNION ALL来返回所有的行
            在查询结束之后使用ORDER BY 只需要一行。

    数据处理:
        插入:
            INSERT
            INSERT INTO tab_student (表名)
                (Name, StuID, Rank)
            VALUES
                ('Alice', '01', 2)(值);
        删除:
            DELETE(一定要注意不然会删除整个表的):
                DELETE FROM customers
                WHERE cust_id = 10006;
                这样删除行,如果想删除列的话直接UPDATE NULL就行了
                这里是删除表的行而不是整个表

                如果想从表中删除所有行，不要使用DELETE。 可使用TRUNCATE TABLE语句
        更新:
            UPDATE:
                UPDATE customers
                SET cust_email = 'xxxx@qq.mail'
                WHERE cust_id = 10005;
                SET 指定新的值,这里要注意我们必须使用cust_id不然的话很有可能更改到错误的数据
                也可以同时更新两行,只需要一个SET
                UPDATE customers
                SET cust_email = 'xxxx@qq.mail',
                    cust_name = 'wang'
                WHERE cust_id = 10005;
                删除值可以直接更新数据成NULL就行

    创建表:
        CREATE TABLE:
            CREAT TABLE 表名(数据库内容)

            CREATE TABLE users (
                id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                username	TEXT NOT NULL UNIQUE,
                password	TEXT NOT NULL,
                email	TEXT
            )
            在创建表的时候可以设置NULL 和 NOT NULL
            NULL 允许这个值为空
            NOT NULL 不允许这个值为空
            AUTO_INCREMENT告诉MySQL，本列每当增加一行时自动增量。
            每次 执行一个INSERT操作时，MySQL自动对该列增量
            DEFAULT设定默认值
        DROP TABLE 表名:删除表
        RENAME TABLE 旧表名 TO 新表名


    删除表:
        DROP TABLE 表名

    重命名表:
        RENAME TABLE 旧表名 TO 新表名

    DELIMITER // 告诉命令行我们使用//代替;来结束语句在使用结束之后可以改回DELIMITER ;
"""

# 概念
"""
数据库索引
    B树
    
    选取B+树的原因
    尽量减少磁盘I/O。为了达到这个目的，磁盘往往不是严格按需读取，而是每次都会预读，
    即使只需要一个字节，磁盘也会从这个位置开始，顺序向后读取一定长度的数据放入内存。
    当一个数据被用到时，其附近的数据也通常会马上被使用。
    程序运行期间所需要的数据通常比较集中。
    
    可知检索一次最多需要访问h个节点。数据库系统的设计者巧妙利用了磁盘预读原理，
    将一个节点的大小设为等于一个页，这样每个节点只需要一次I/O就可以完全载入。
    每次新建节点时，直接申请一个页的空间，这样就保证一个节点物理上也存储在一个页里，
    加之计算机存储分配都是按页对齐的，就实现了一个node只需一次I/O。
    B-Tree中一次检索最多需要h-1次I/O（根节点常驻内存），渐进复杂度为O(h)=O(logdN)。
    一般实际应用中，出度d是非常大的数字，通常超过100，因此h非常小（通常不超过3）。
"""