'''
@author: ZGC
@license: (C) Copyright 2013-2018, Node Supply Chain Manager Corporation Limited.
@contact: zgc_troy@163.com
@github:  https://github.com/ZGCTroy
@file: test.py
@time: 2018/10/11 19:51
@desc:
'''



# with open("./fuzz_bitmap","rb+") as f:
#     data = f.read()
#     print(data)
#     print(len(data))
#     print(type(data))


# with open("./fuzz_bitmap","rb+") as f:
#     for i in f.read():
#         print(i)


# with open("./fuzz_bitmap","rb+") as f:
#     data = f.read(1)
#     print(data)
#     print(ord(data))
#     print(len(data))
#     print(type(data))
import pandas as pd
with open("./fuzz_bitmap","rb+") as f:
    data = []
    for i in f.read():
        data.append(i)
    print(data.count(254))
    # data = pd.DataFrame(data=data)
    # print(data)
    # print(data.info())
    # print(data.describe())
