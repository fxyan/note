"""
python 函数的一些坑:
	可变对象不可变对象
		a = 1
		def fun(a):
			a = 2
			print('函数a的值', a)
		fun(a)
		print(a)

		输出:
			函数a的值 2
			1

			b = []
			def fun1(b):
				b.append(0)
				print('函数列表b', b)
			fun1(b)
			print(b)

			输出:
				函数列表b [0]
				[0]

			c = [1, 2, 3]
			def fun1(c):
				print(c)
				c = [1, 4, 6, 8]
				c.append(0)
				# c = [1, 4, 6, 8]
				print('函数列表c', c)
			fun1(c)
			print(c)

			输出:
				[1, 2, 3]
				函数列表c [1, 4, 6, 8, 0]
				[1, 2, 3]

	我们可以看这个程序这里可以说明Python的参数传入的问题:
		在Python中所有的变量都可以被认为是内存地址的引用，
		在Python中string tuples,numbers是不可变对象 list dict set 是可变对象
	我们在使用函数的时候相当于是给外面引用的一个复制:
		对于可变对象我们在里面修改外面也会变化因为这里的引用已经复制了内存地址
		(这里如果你在函数内部对该值进行重新赋值，那么说明该可变的引用对象发生了改变就不会再更改外部的值了)
		但是对于不可变对象在内部的修改外部不会产生变化

	双下划线:
    __foo:这个有真正的意义:解析器用_classname__foo来代替这个名字,
	以区别和其他类相同的命名,它无法直接像公有成员一样随便访问,通过对象名._类名__xxx这样的方式可以访问.

写点高级技巧:
	generator:
		在python3中使用是没有问题的
			for i in range(100000)
		在python2中使用会发生一些麻烦所以一般会使用
			for i in xrange(100000)

		def my_range(n):
			i = 0
			while i != n:
				i += 1
				yield i

		r = my_range(1000)
		for i in r:
			print(i)

		yield: 在这里可以理解为系统中断也可以说是协程,在出现yield的时候就进行了中断，然后跳出循环，
				下次运行的时候我们是从上次中断的地方从新开始。
				假设for 10000000 是要先将10000000这个建立成一个数组然后再进行循环，
				但是使用生成器就不需要了 每次需要数据的时候再跳进去运行
"""
'''
	iterator:
		iter iter(obj) = obj.__iter__()
		next next(obj) = obj.__next__()
		一般来说只要是是有了__iter__和__next__这两个方法就可以说是实现了一个iterator

		(a)
			for i in range(10):
				pass

		(b)
			iter_obj = range(10)
			iter(iter_obj)

			while True:
				try:
					i = next(iter_obj)
				except StopIteration:
					break
'''
# class Pow2(object):
# 	def __init__(self, num):
# 		self.num = num
# 		self.n = 0
#
# 	def __iter__(self):
# 		self.n = 0
# 		return self
#
# 	def __next__(self):
# 		if self.n < self.num:
# 			self.n += 1
#             return 2 ** self.n
#         else:
#         raise StopIteration


'''
"""
	class methed, instance method, static method:
		instance method:
			实例对象: self就是实例对象的绑定
		static method:
			一个工具对象其实放在那里都是可以的但是这个为了严谨性所以放在使用到他的类中
		class method:
			和class绑定的一个方法
		类方法实例方法静态方法都可以被实例对象调用，区别是类方法传入的是类的名称
		实例:

'''
# class A(object):
#     def __init__(self, a):
#         self.a = a
#
#     def foo(self):
#         print('instance method')
#
#     @classmethod
#     def c_foo(cls):
#         print('class method')
#
#     @staticmethod
#     def s_foo():
#         print('static method')
#
# b = A(25)
# b.foo()
# b.c_foo()
# a.s_foo()
# A.c_foo()
# A.s_foo()
'''
鸭子类型:
    你这个东西叫的像鸭子 走的像鸭子 跑的像鸭子那么你就是鸭子
    在python中不回去管你是什么类型的，只会去看你是不是对应的方法和属性，如果有就可以使用没有就不行

函数重载:
    为什么python没有函数重载这个概念呢，因为函数重载有两个方面的原因
        1 可变参数类型
        2 可变参数个数
        在Python中可变参数类型，因为python接收任何类型的参数所以不同类型的参数传递过来可能代码相同无需重载
        在Python中可以接受任意个数的参数 用*args **kwargs
        所以不需要重载

	引用类型:
		深拷贝:
			在使用深拷贝中可以使用模块:
				from copy import deepcode
				l1 = []
				l2 = deepcode(l1)
				li.append(1)
				print(l2)

		浅拷贝:
			浅拷贝容易出现一些错误，比如
				l2 = [1, [1, 2], 2]
				如果你使用 l1 = l2[:]这样就不是深拷贝里面的列表还是会出现bug

		默认参数陷阱:
'''
# def foo(a=[]):
#     a.append(1)
#     print(a)
# foo()
# foo()
'''
			这里出现了一个默认参数陷阱，你第一次创建了a[]第二次就是引用，这样就会出现一些bug

	lambda:
		mul2 = lambda x：x * 2
		print(mul2(3))

		map filter reduce

		import functools
		import operator
		print(list(map(lambda x: x * 2, [1, 2, 3, 4])))
		print(list(filter(lambda x: x * 2, [1, 2, 3, 4])))
		print(functools.reduce(operator.add, [1, 2, 3, 4, 5], 5))

	closure:
		闭包引用问题
			def greeting(msg)
				def hello(msg, name)
				return hello
			h = greeting('welcome')
			h('akira')

		容易出现的陷阱:

			l = []
			for i in range(10):
			    def _():
			        print(i)
			    l.append(_)

			for f in l:
			    f()

			这样会产生闭包问题这里列表append的是一个函数并没有运行,这个时候我们下面
			for循环运行这个函数会让其中的每个_函数运行,这个时候运行函数时里面的i值就是
			9了,闭包引用一定要引用外部变量，如果直接在内部定义变量的话那么就不算是闭包了

			解决方法传入默认参数就行了(i=i)将变量拷贝到作用域中

	*args, **kwargs:
		args:
			tuple
		kwargs:
			dict


	magic method:
		missing method 消失的方法
		__ge

	list comprehension:

	dict comprehension:

	decorator:
		装饰器:
			我写了一个例子来看一下
'''

#
# def simple_wrapper(fn):
#     def _():
#         print(fn.__name__)
#         return fn
#     return _
#
#
# def fix_arg_wrapper(fn):
#     def _(x):
#         print(x)
#         return fn()
#     return _
#
#
# def all_args_wrapper(fn):
#     def _(*args, **kward):
#         print(*args, **kward)
#         return fn(*args, **kward)
#     return _
#
#
# @all_args_wrapper
# def foo(a, b, c, d, f=1):
#     pass
#
#
# foo(1, 2, 3, 4, f=1)
'''
				def simple_wrapper(fn):
					def _():
						print(fn.__name__)
						return fn
					return _

				def fix_arg_wrapper(fn):
					def _(x):
						print(x)
						return fn()
					return _

				def all_args_wrapper(fn):
					def _(*args, **kward):
						print(*args, **kward)
						return fn(*args, **kward)
					return _

				@simple_wrapper
				def foo()
					pass

				foo()

				一个装饰器就是写一段代码可以再使用装饰器的所有代码中进行使用，
				比如你想打log的话如果你想在一段代码中加就很简单，但是如果你想在一万段代码中加log就很困难。
				比如查看用户是不是登陆了，比如说在flask的装饰器
				如果你加上了log测试完成了，但是你上线的时候不会想出现log一个个删除更是崩溃，我们就可以使用装饰器这个方法，只需要在装饰器这个函数中将log注释就可以了。
				(延伸一下这个装饰器主要是使用了AOP的思想: 面向方向编程，吧程序做成了一个可拔插的东西当你想使用的时候就可以将程序插入，当不需要的时候就可以将程序拔出或者更改。)


	默认参数:

垃圾回收机制：
	python在每个对象中保存了一个计数器，这个计数器记录了当前对象的引用数目，当引用数目为0的时候，这个对象就会被自动回收。

储存机制:
	在python内部暂时储存并重复使用短字符串。所以会出现短字符串赋值的时候出现两个完全相同的情况。

赋值语句：
    这个很鬼畜啊
    a, *b = 'spam'
    输出： s ['p', 'a', 'm']
    这玩意是拓展序列解包 你可以从*kward 这个函数上使用它

    列表：
    在使用+号合并的时候会产生新的对象，而不会像原来一样在原有列表上进行修改。

    变量名：
        字母或者下划线 + 任意数目的字母 数字或者下划线

	for循环：
		for循环是支持两个数一起进行迭代的
		d = {'a' : 1,
			 'b' : 2,
			 'c' : 3,
			}

    函数
    嵌套函数的使用：
    两个函数在第一个函数赋值之后的时候就可以简单的将其 赋值给其余变量
    然后在进行赋值就可以给里面的函数赋值
        def knight():
            title = 'sir'
            action = (lambda x: title + ' ' + x)
            return action
        act = knight()
        act('robin')
        输出：'sir robin'
    匿名函数 lambda：
    默认参数也能够在这边使用
    使用方法 : f = lambda x, y, z: x + y + z
            print(f(2, 3, 4))
            输出： 9
    map：
        map(函数， 应用对象)
        这样的话处理匿名函数会变得比较方便
        counters = [1, 2, 3, 4]
        def inc(x):
            return x + 10
        list(map(inc, counters))
        输出：[11, 12, 13, 14]

        匿名函数版本
        counters = [1, 2, 3, 4]
        couns = [1, 2, 3, 5]
        list(map(lambda x: x + 10), counters))
        输出： [11, 12, 13, 14]
        list(map(lambda x, y: x + 10 + y), counters, couns))
        输出： [12, 14, 16, 19]
    在函数嵌套中使用lambda可以很方便的接收到上面函数传入的数据

    filter:
    如果序列中的元素返回值为真的时候就将其键入到结果的列表中
        list(filter((lambda x: x > 0), range(-5, 5)))
        输出：[1, 2, 3, 4]

    reduce:
    是一个模块函数了需要import一下
    from functools import reduce
    具体例子
    reduce((lanbda x, y: x + y), [1, 2, 3, 4])
    输出： 10
     reduce((lanbda x, y: x * y), [1, 2, 3, 4])
     输出：24

    总结：
        三个内置函数都是对待一个可迭代对象以及集合结果中的各项应用于另外一个函数。
        map 把每一项传递给函数并收集结果
        filter 收集那些函数返回一个 True值的项
        reduce 通过对一个累加器和后续向应用函数来计算一个单个的值。(而且不是内置函数需要导入模块才能够使用)


	模块：
	    import:
	        将会读取整个模块
	        第一次导入指定文件时的流程
	        1.找到模块文件
	        2.编译成位码
	        3.执行模块的代码来创建其所定义的对象
	        如果第二次运行的话就会跳过这些步骤
	        直接从内存提取已加载的模块
	        (python已经导入的模块保存在一个内置的sys.modules字典中
	        如果想看看已经导入了什么模块可以导入sys并且打印list(sys.modules.keys()) )
	        import module1
	        module1.printer("Hello world")
	    from:
	        from module1 import printer
	        printer("Hello world")
	        将获取模块特定的变量名
	        from *
	        可以获得模块顶层所有赋了值得变量名的拷贝
	        from module1 import *
	        可以获得所有变量名的使用

	    import 和 from :
	        其实是赋值语句
	        import 将整个模块对象赋值给一个变量名
	        from 将一个或多个变量名赋值给另一个模块中的同名的对象
	        注意：类似列表之类的在from之后如果被赋值的话那么就会发生改变

	    点号运算：
	        x指的是在当前作用域内搜索变量名x
	        x.y是指在当前范围内搜索x， 然后搜索对象x之中的属性y
	        x.y.z指的是寻找对象x之中的变量名y，然后再找对象x.y之中的z

	    as语句
	        import modulename as name
	        相当于
	        import modulename
	        name = modulename



# from functools import reduce
# print(reduce((lambda x, y: x * y), [1, 2, 3, 4]))
'''
# counters = [1, 2, 3, 4]
# couns = [1, 2, 3, 5]
# r = list(map(lambda x, y: x + y + 10, couns, counters))
# print(r)
