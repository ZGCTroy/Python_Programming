"""
FileName    : main.py
Author      : 郑光聪,20167851,160211
Institution : School of computer and communication engineering, Northeastern University at Qinhuangdao
Version     : 0.1
Date        : 2018-09-19
Description : transer NFA to DFA
"""
from DFA import *
from NFA import *







def main():
    # TODO 1 : 输入NFA
    N = NFA()
    N.read_from_file(filepath="./data4.9_origin.txt")

    # TODO 2 : 输出NFA
    N.print()

    # TODO 2 : 确定化NFA为DFA
    D = N.determine()

    # TODO 3 : 输出DFA
    D.print()

if __name__=='__main__':
    main()
