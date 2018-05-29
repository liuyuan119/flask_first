def addHaha(func):
    print('-----------------addHaha--------------')         # 2（没有调用主函数时）
    def addFun():
        return func() + "Haha"                                      # 3进入4    # 5 结束
    return addFun


def addWorld(func):
    print('-----------------addWorld--------------')  # 1（没有调用主函数时）
    def addFun():
        return func() + "world"                                     # 4 完成回到3
    return addFun


@addHaha
@addWorld
def main():
    print('-------------------printHello------------')
    return 'hello'


print(main())
