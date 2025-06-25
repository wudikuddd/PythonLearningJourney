"""
装饰器 - 在不改变原有对象调用方式的情况下，给原有对象增加功能

原理：
    闭包 + 高阶函数(在python中 [函数] 是一等公民, 可以作为参数传递)

        - 闭包: 
            1. 发生在函数嵌套中
            2. 外层函数的返回值是内部函数，且返回的内部函数保存了外层函数的相关参数和变量(内部函数称为：闭包函数)
        eg:
            def external_func(xx: int):
            
                xx += 1

                def internal_func():
                    print(xx)
                    pass
            
                return internal_func

            运行:
            func1(1) -> <function func1.<locals>.internal_func at 0x101706520>  # 返回函数

            func1(1)() # 执行函数
                -> 2  # 打印内部存储变量xx的值
                -> None  # 函数返回值

语法糖 “@” 的奥义:

    @decorator
    def func():       -----相当于---->  func = decorator(func)
        pass         
    
    执行被装饰后的函数: func() 实际上执行的是: decorator(func)()
""" 
from functools import wraps 


# 装饰器函数实现
def simple_decorator(func):

    # @wrapper(func)  # wraps: 将传递给 `wraps（）` 的参数作为剩余参数传递给 `update_wrapper（）`。默认参数与 `update_wrapper（）` 的参数设置相同
    def wrapper(*args, **kwargs):
        
        # 额外功能
        print(f'wrapper is running')
        
        return func(*args, **kwargs)
    
    return wrapper


def func_test1(x, y):
    print("func_test1 is running")
    return f"{x} + {y} = {x + y}"

# 装饰函数
# 语法糖 -> @: 标识着这是一个装饰器
@simple_decorator
def func_test2(x, y):
    print("func_test2 is running")
    return f"{x} + {y} = {x + y}"


# 带参数的装饰器函数实现
def decorator_with_params(*deco_args, **deco_kwargs):
    def decorator(func):
        
        def wrapper(*args, **kwargs):
            
            # 使用参数
            print(f'decorator_with_params params: {str(*deco_args)}, {str(dict(**deco_kwargs))}')

            # 额外功能
            print(f'wrapper is running')
            
            return func(*args, **kwargs)
    
        return wrapper
    
    return decorator


# 装饰函数 - 使用带参数的装饰器
@decorator_with_params("zhangsan", age=3)
def func_test3(x, y):
    print("func_test3 is running")
    return f"{x} + {y} = {x + y}"


def main():
    result = simple_decorator(func_test1)(1, 2)  # 结合原理，看懂这一步很重要.  注意！！！-> 这里的func_test2实际上执行的是wrapper
    print(result)

    # @simple_decorator 可以理解为简化了:  func_test2 = simple_decorator(func_test2)
    result = func_test2(1, 2)  # 注意！！！-> 这里的func_test2实际上执行的是wrapper
    print(result)

    # @decorator_with_params(params) 可以理解为简化了:  func_test3 = decorator_with_params(params)(func_test3)
    result = func_test3(1, 2)
    print(result)

if __name__ == '__main__':
    main()