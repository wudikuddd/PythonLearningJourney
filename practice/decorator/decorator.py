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
""" 
from functools import wraps 


# 1. 装饰器函数实现
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


# 语法糖 -> @: 标识着这是一个装饰器
@simple_decorator
def func_test2(x, y):
    print("func_test2 is running")
    return f"{x} + {y} = {x + y}"

def main():
    result = simple_decorator(func_test1)(1, 2)  # 结合原理，看懂这一步很重要.  注意！！！-> 这里的func_test2实际上执行的是wrapper
    print(result)

    print(f"\n{'-'*10} 分割线 {'-'*10}\n")

    # @simple_decorator 可以理解为简化了:  func_test2 = simple_decorator(func_test2)
    result = func_test2(1, 2)  # 注意！！！-> 这里的func_test2实际上执行的是wrapper
    print(result)


if __name__ == '__main__':
    main()