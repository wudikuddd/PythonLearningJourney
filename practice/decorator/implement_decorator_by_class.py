"""
用类实现装饰器 - 类装饰器依赖__call__方法, 让实例像方法一样被调用
"""
import functools


# 方式一
class Decorator1:

    def __init__(self, *args, **kwargs):
        self.str_params = f'Decorator1 init params: {str(*args)}, {str(dict(**kwargs))}'
    
    def __call__(self, func):

        @functools.wraps(func)
        def warapper(*args, **kwargs):

            # 使用参数
            print(self.str_params)

            # 额外功能
            print(f'Decorator1 __call__ is running')

            return func(*args, **kwargs)
        
        return warapper
    

# 方式二
class Decorator2:

    def __init__(self, func):
        self.func = func
    
    def __call__(self, *args, **kwargs):

        # 额外功能
        print(f'Decorator2 __call__ is running')

        return self.func(*args, **kwargs)


# 使用方式一装饰
@Decorator1("zhangsan", age=3)  # func_test = Decorator1("zhangsan", age=3)(func_test)(x, y)
# 使用方式二装饰
@Decorator2  # func_test = Decorator1(func_test)(x, y)
def func_test(x, y):
    print("func_test1 is running")
    return f"{x} + {y} = {x + y}"


def main():
    result = func_test(1, 2)
    print(result)


if __name__ == '__main__':
    main()
