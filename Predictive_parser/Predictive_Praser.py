'''
@author: ZGC
@license: (C) Copyright 2013-2018, Node Supply Chain Manager Corporation Limited.
@contact: zgc_troy@163.com
@github:  https://github.com/ZGCTroy
@file: Predictive_Praser.py
@time: 2018/10/11 17:29
@desc:
'''

from Grammar import Grammar
import pandas as pd
import numpy as np


class Predictive_Parser:
    def __init__(self, grammar=Grammar()):
        self.grammar = grammar
        self.First = {}
        self.Follow = {}
        self.Select = {}
        self.Table = pd.DataFrame()
        self.terminals = []

    def get_first(self, str):
        """
        计算str的First集
        :param str: 要计算First集的字符串
        :return: First(str),type=set()
        """
        if str in self.First.keys():
            return self.First[str]
        First = set()
        for i in str:
            if i == '@':
                First.add(i)
                return First

            if i in self.grammar.terminals:
                First.add(i)
                break

            if i not in self.grammar.nonterminals:
                print('sb', i)
                break

            NextFirst = set()
            for j in self.grammar.P[i]:
                NextFirst = NextFirst | self.get_first(j)

            First = (First - {'@'}) | NextFirst
            if '@' not in NextFirst:
                break
        self.First[str] = First
        return First

    def get_follow(self, VN):
        """
        计算非终结符VN的Follow集
        :param VN: 非终结符
        :return: Follow(VN),type=set()
        """
        if VN not in self.Follow:
            self.Follow[VN] = set()
        else:
            return self.Follow[VN] - {'@'}

        if VN in self.grammar.start_symbols:
            self.Follow[VN].add('#')

        for nonterminal in self.grammar.nonterminals:
            for str in self.grammar.P[nonterminal]:
                VNpos = str.find(VN)

                if VNpos != -1:
                    if VNpos == len(str) - 1:
                        self.Follow[VN] |= self.get_follow(nonterminal)
                    else:
                        nextstr = str[VNpos + 1::]
                        NextFirst = self.get_first(nextstr)
                        self.Follow[VN] |= NextFirst
                        if '@' in NextFirst:
                            self.Follow[VN] |= self.get_follow(nonterminal)

        return self.Follow[VN] - {'@'}

    def get_select(self, left, right):
        """
        计算规则P的Select集合
        :param left: 规则P的左部
        :param right: 规则P的右部
        :return: Select(left->right),type=set()
        """
        if left in self.Select:
            if right in self.Select[left]:
                return self.Select[left][right]
            else:
                self.Select[left][right] = set()
        else:
            self.Select[left] = {}

        RightFirst = self.get_first(right)

        if '@' in RightFirst:
            self.Select[left][right] = (RightFirst - {'@'}) | self.get_follow(left)
        else:
            self.Select[left][right] = RightFirst

        return self.Select[left][right]

    def judgeLL1(self):
        """
            判断文法G是否为LL(1)文法
        """
        print('First集如下:')
        for nonterminal in self.grammar.nonterminals:
            print(
                'First({}) = {}'.format(
                    nonterminal, self.get_first(nonterminal)
                )
            )
        print('\nFollow集如下:')
        for nonterminal in self.grammar.nonterminals:
            print(
                'Follow({}) = {}'.format(
                    nonterminal, self.get_follow(nonterminal)
                )
            )

        print('\nSelect集如下:')
        for nonterminal in self.grammar.P:
            for right in self.grammar.P[nonterminal]:
                print('Select({}->{}) = {}'.format(nonterminal, right, self.get_select(nonterminal, right)))
        print()

    def cal_table(self):
        """
            构造文法G的预测分析表Table
        """
        self.terminals = self.grammar.terminals
        self.terminals.append('@')
        self.terminals.sort()
        table = []

        for nonterminal in self.grammar.nonterminals:
            row = {}
            for terminal in self.terminals:
                row[terminal] = ""
                for right in self.Select[nonterminal]:
                    if terminal in self.Select[nonterminal][right]:
                        row[terminal] = nonterminal + '->' + right
                        break
            table.append(row)

        table = pd.DataFrame(data=table, index=self.grammar.nonterminals, columns=self.terminals)
        self.Table = table
        print('预测分析表如下：\n')
        print(self.Table)
        print()
        print()

    def judge(self, str):
        """
        判断输入串的分析过程
        :param str: 要代入预测分析器进行语法分析预测的字符串
        :return:
        """
        curstack = ['#']
        curstack.extend(self.grammar.start_symbols)
        leftstack = list(str)
        data = []
        while len(curstack):
            row = {'curstack': ''.join(curstack), 'curchar': leftstack[0], 'leftstack': ''.join(leftstack), 'P': ''}
            if curstack[-1] == leftstack[0]:
                curstack.pop(-1)
                leftstack.pop(0)
            else:
                str = self.Table[leftstack[0]][curstack[-1]]
                if (curstack[-1] not in self.grammar.nonterminals) or str=="":
                    data.append(row)
                    data = pd.DataFrame(data=data, columns=['curstack', 'curchar', 'leftstack', 'P'])
                    print('匹配过程如下：\n')
                    print(data)
                    print('\n匹配失败')
                    return
                curstack.pop(-1)
                row['P']=str
                str = str.split('->')[1]
                if str != '@':
                    str = list(str)
                    str.reverse()
                    curstack.extend(str)

            data.append(row)

        data = pd.DataFrame(data=data,columns=['curstack','curchar','leftstack','P'])
        print(data)
        print('匹配成功')


def main():
    # TODO 1 : 从文件读入文法,要求此文法不包含左递归
    G = Grammar()
    G.read_from_file("./data5.3_origin.txt")

    # TODO 2 : 构建语法分析预测器,导入文法，并打印文法
    predictive_parser = Predictive_Parser(grammar=G)
    predictive_parser.grammar.print_grammar()

    # TODO 3 ： 分别求出First、Follow、Select集，并判断文法是否属于LL1文法
    predictive_parser.judgeLL1()

    # TODO 4 ： 构建语法分析预测表并打印
    predictive_parser.cal_table()
    # TODO 5 ： 输入字符串进行语法分析预测
    predictive_parser.judge('(a,a)#')


if __name__ == '__main__':
    main()

