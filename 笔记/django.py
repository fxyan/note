"""
关于django的一些知识
django处理url的机制:
    假如请求想转入/blog/
    首先在setting文件中找到ROOT_URLCONF = 'xxxxxx'
    这行标记了你的根url的地址，然后从这个文件中寻找你所需要的url
    其中可能会有include之类的就在向下寻找，直到找到你所需要的路由函数
    找到后路由函数通过render返回一个HttpResponse，Django再进行处理将路由函数返回的
    response显示在web页面上
Django Django.contrib:
    这个是Django的标准库
Django request:
    简单的函数:
        request.path	除域名以外的请求路径，以正斜杠开头	"/hello/"
        request.get_host()	主机名（比如，通常所说的域名）	"127.0.0.1:8000" "www.example.com"
        request.get_full_path()	请求路径，可能包含查询字符串	"/hello/?print=true"
        request.is_secure()	如果通过HTTPS访问，则此方法返回True， 否则返回False	True 或者 False
    HTTP的头信息都包含在了request.META中了
"""