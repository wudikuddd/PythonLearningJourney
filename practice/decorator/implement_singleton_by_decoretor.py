"""
装饰器实现单例模式
"""

def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper


@singleton
class TestClasx:
    pass


def main():
    test_clasx1 = TestClasx()
    test_clasx2 = TestClasx()
    test_clasx3 = TestClasx()

    print(f"{test_clasx1}\n{test_clasx2}\n{test_clasx3}")


if __name__ == '__main__':
    main()