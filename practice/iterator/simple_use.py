"""
小内存处理大数据
"""
import os
import tracemalloc  # python内置模块(可以跟踪程序的内存使用情况)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
# log文件路径
DEMO_FILE_PATH = os.path.join(DIR_PATH, 'db.log_')


def process_line(line):
    """
    处理单行内容
    :param line:
    :return:
    """
    # print(line)
    pass


class MyIterator:
    def __init__(self, file_path: str):
        self.file = open(file_path, 'r')

    def __iter__(self):
        return self

    def __next__(self):
        line = self.file.readline()
        while line:
            if "INSERT INTO" in line:  # 找到包含INSERT INTO的行
                return line
            line = self.file.readline()
        self.file.close()
        raise StopIteration


def main():
    tracemalloc.start()  # 开始追踪内存分配

    # # 1.常见处理文件方式
    # with open(DEMO_FILE_PATH, 'r') as f:
    #     lines = f.readlines()  # 返回的是包含所有行的列表. 在处理大文件时，应避免使用
    #
    # for line in lines:
    #     process_line(line)
    #
    # # 2.使用迭代器方式
    # with open(DEMO_FILE_PATH, 'r') as f:
    #     for line in f:  # 逐行读取（迭代器）. 补充一个知识点: 文件对象本身就是迭代器
    #         process_line(line)

    # 3. 自定义迭代器
    for line in MyIterator(DEMO_FILE_PATH):
        process_line(line)

    current, peak = tracemalloc.get_traced_memory()  # 获取当前内存 和 start到当前的峰值内存
    print(f'当前内存: {current / 1024 / 1024}MB, 峰值: {peak / 1024 / 1024}MB')
    tracemalloc.stop()


if __name__ == '__main__':
    main()
