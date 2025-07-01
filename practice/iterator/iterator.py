"""
迭代器(如生成器、iter(list)的返回值):
    对象实现了'__iter__'和‘__next__’方法，并且'__iter__'方法返回对象本身(迭代器协议)

可迭代对象(如列表、字典):
    对象实现了'__iter__'方法，并且'__iter__'方法返回一个迭代器

故:
    迭代器(__iter__返回self, self本身就是迭代器, 满足条件)一定时可迭代对象，可迭代对象不一定是迭代器

for循环原理:
    for循环开始 -> 调用iterables(可迭代对象)的__iter__方法获取iterator(迭代器)  # 隐式处理
    -> 调用iterator(迭代器)的__next__方法获取下一个值
    -> 能够获取下一个值?
        YES -> 返回下一个值 -> 继续调用iterator(迭代器)的__next__方法获取下一个值
        NO -> 退出for循环

"""
from collections.abc import Iterator
'''
Iterator 抽象基类：
    * collections.abc.Iterator 已内置验证逻辑
    * 等价于手动检查：hasattr(obj, '__iter__') and hasattr(obj, '__next__')
'''


class MyIterator:
    def __init__(self, numbers: list):
        self.numbers = numbers
        self.current_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_index < len(self.numbers):
            current_index = self.current_index
            self.current_index += 1
            return self.numbers[current_index]
        else:
            raise StopIteration


class MyIterable:
    def __init__(self, numbers: list):
        self.numbers = numbers

    def __iter__(self):
        return MyIterator(self.numbers)


def main():
    my_iterable = MyIterable([1, 2, 3, 4, 5])
    my_iterator = iter(my_iterable)  # 等价于 my_iterator = my_iterable.__iter__(), 返回一个迭代器
    print(isinstance(my_iterator, Iterator))

    while True:
        try:
            next_test = next(my_iterator)  # 等价于 my_iterator.__next__(), 返回下一个值
            print(next_test)
        except StopIteration:
            break

    for number in my_iterable:  # 隐式调用my_iterable.__iter__(), 获取迭代器, 继续调用my_iterator.__next__()
        print(number)

    print(isinstance(my_iterable, Iterator) or isinstance([1, 2, 3], Iterator))  # 可迭代对象(如列表)不是迭代器


if __name__ == "__main__":
    main()
