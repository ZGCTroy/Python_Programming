'''
@author: ZGC
@license: (C) Copyright 2013-2018, Node Supply Chain Manager Corporation Limited.
@contact: zgc_troy@163.com
@github:  https://github.com/ZGCTroy
@file: main.py
@time: 2018/10/11 17:29
@desc:
'''


from Grammar import Grammar
from Predictive_Parser import *
import os
import sys

def main():
    application_path = ""
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)
    filepath = os.path.join(application_path,'input.txt')

    # TODO 1 : 从文件读入文法,要求此文法不包含左递归
    G = Grammar()
    G.read_from_file(filepath)

    # TODO 2 : 构建语法分析预测器,导入文法，并打印文法
    predictive_parser = Predictive_Parser(grammar=G)
    predictive_parser.grammar.print_grammar()

    # TODO 3 ： 分别求出First、Follow、Select集，并判断文法是否属于LL1文法
    predictive_parser.judgeLL1()

    # TODO 4 ： 构建语法分析预测表并打印
    predictive_parser.cal_table()
    # TODO 5 ： 输入字符串进行语法分析预测
    predictive_parser.judge('eadeaa#')
    predictive_parser.judge('edeaebd#')
    predictive_parser.judge('edeaeaadabacae#')
if __name__ == '__main__':
    main()