"""
缓存

缓存特征
    命中率:
        当数据在缓存中被请求到的时候成为缓存命中，请求到的越多命中率越高，
        同理利用率也越高
    最大空间:
        因为缓存是在内存中的所以说不可能会很大，当缓存数据达到一定的数量的时候就需要
        淘汰部分数据来存放新的数据
    淘汰策略:
        LRU:最近最久未使用策略，优先淘汰最久未使用的数据。这样可以缓存热点数据
            增加缓存命中率。
        FIFO:先进先出
缓存位置:
    浏览器缓存:
        浏览器缓存主要是缓存网页的静态文件js 图片 HTML等
    反向代理:
        存储在反向代理中
    ISP:
        存储在网络供应商中的缓存
    本地缓存:
        存储在服务器本地内存
    分布式缓存:
        Redis
    数据库缓存:
        MySQL有自己的缓存机制
    CDN:
        利用更靠近的服务器来给用户更快的消息体验
缓存穿透:
    当用户访问一个不存在的数据时，请求会穿过缓存到达数据库
    解决方案:
        对这类请求进行过滤
        对不存在的数据缓存一个空数据
缓存雪崩:
    缓存大面积失效(过期)
    缓存服务器宕机
    数据没有加载到缓存中
    导致大量的请求到达数据库导致数据库崩溃
    解决方案:
        通过对用户的观察进行合理的缓存时间防止大面积过期
        使用分布式缓存，缓存数据库宕机只是一个节点挂了其余的还是可以继续工作，
        缓存预热，避免系统刚运行一会缓存中没有足够的数据
缓存一致性:
    当数据更新的时候同时要求缓存也能更新
    解决方案:
        数据更新的时候同时更新缓存
        在请求缓存的时候去查询是不是最新的数据，如果不是就去更新
数据分布:
    哈希分布:
        按照哈希值下标进行分布
        缺点就是节点超过一开始的设定值的时候从新分布会导致大量数据迁移
    顺序分布:
        按顺序分布
        保证数据顺序一致
        能精准的把握每台服务器的数据量
"""