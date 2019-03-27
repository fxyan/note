def cache_fib(fucn):
    cache = {}
    print(cache)
    def momo(*args):
        # print(args)
        if args not in cache:
            print('args', args)
            print(fucn(*args))
            cache[args] = fucn(*args)
            print(cache, 'cache')
        return cache[args]
    return momo

@cache_fib
def fib(n):
    if n <= 1:
        return 1
    return fib(n-1) + fib(n-2)

def multipliers():
    return [lambda x: i * x for i in range(4)]


print([m(0) for m in multipliers()])

def multipliers():
    def mm(x):
        for i in range(4):
            c = i * x
        return c
    return mm
list = [[]] * 5
print(id(list[0]), id(list[1]))