import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


class Scanner:
    def __init__(self):
        # 关键字
        self.keyword = {}
        # 运算符
        self.operator = {}
        # 界符
        self.delimiters = {}
        # 字母
        self.character = {}
        # 数字
        self.number = {}
        # 行
        self.lines = []
        # 词法分析表
        self.scanner_table = pd.DataFrame(
            columns=['line id','word','type','name']
        )

    def init(self):
        # 关键字
        self.keyword = {
            'int': 'integer',
            'main': 'main',
            'double': 'double',
            'return': 'return',
            'if': 'if',
            'else': 'else'
        }
        # 运算符
        self.operator = {
            '+': 'plus',
            '=': 'equal',
            '+=': 'plus or euqal',
            '-': 'minus',
            '<': 'less',
            '<=': 'less or equal',
            '==': 'judge'
        }
        # 界符
        self.delimiters = {
            ':': 'colon',
            ';': 'semicolon',
            '(': 'left parenthesis',
            ')': 'right parenthesis',
            '{': 'left curly braces',
            '}': 'right curly braces'
        }
        # 字母
        for x in range(ord('a'),ord('z')+1):
            self.character[chr(x)]=chr(x)

        # 数字
        for x in range(0,10):
            self.number[str(x)]=str(x)

    def getsym(self):
        line_id = 0
        for line in self.lines:
            line_id += 1
            id = 0
            length = len(line)

            while id < length:
                str = ''
                while id<length and (line[id] ==' ' or line[id] == '\n' or line[id]=='\r' or line[id]=='   '):
                    id += 1
                if id >= length:
                    break
                if line[id] in self.character:   # 是字母
                    while id<length and (line[id] in self.character or line[id] in self.number):
                        str += line[id]
                        id += 1
                    if str in self.keyword:
                        self.add_into_scanner_table(line_id,str,'keyword',self.keyword[str])
                    else:
                        self.add_into_scanner_table(line_id,str,'identifier',str)
                elif line[id] in self.number:  #  是数字
                    while id<length and (line[id] in self.number or line[id]=='.'):
                        str += line[id]
                        id += 1
                    if id < length:
                        if line[id] in self.character:
                            self.print_scanner_table()
                            print('\nerror at line {} , 错误类型为{}'.format(line_id,'变量命名错误'))
                            return
                    if str[-1] in self.number:
                        self.add_into_scanner_table(line_id,str,'number',str)
                    else:
                        print('读入数字时出现非法错误')
                        return
                elif line[id] in self.delimiters:  # 界符
                    str += line[id]
                    id += 1
                    self.add_into_scanner_table(line_id,str,'delimiters',self.delimiters[str])
                elif line[id] in self.operator:   # 运算符
                    if line[id] == '=':
                        while id < length and line[id] == '=':
                            str += line[id]
                            id += 1
                    else:
                        while id < length and (line[id] in self.operator):
                            str += line[id]
                            id += 1

                    if str in self.operator :
                        self.add_into_scanner_table(line_id,str,'operator',self.operator[str])
                    else:
                        print('读入运算符时出错')
                else:
                    str += line[id]
                    id += 1
                    self.add_into_scanner_table(line_id,str,'null',str)

    def add_into_scanner_table(self,line_id,word,type,name):
        self.scanner_table = self.scanner_table.append(
            {'line id': line_id, 'word': word, 'type': type,'name':name},
            ignore_index=True
        )

    def read_from_file(self, file_path):
        with open(file_path) as f:
            self.lines = f.readlines()

    def print_scanner_table(self):
        print()
        print(self.scanner_table)

def main():
    scanner = Scanner()
    scanner.init()
    scanner.read_from_file('./input.cpp')
    scanner.getsym()


if __name__ == '__main__':
    print('\n1602班11号，20167851，郑光聪\n')
    print('Language : Python3')
    print('Editor : Pycharm')
    print('Tools : pandas')
    main()
