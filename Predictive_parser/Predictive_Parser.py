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
        if left in self.Select:
            if right in self.Select[left]:
                return self.Select[left][right]
            else:
                self.Select[left][right] = set()
        else:
            self.Select[left] = {}

        RightFirst = self.get_first(right)

        if '@' in RightFirst:
            self.Select[left][right] = RightFirst | self.get_follow(left)
        else:
            self.Select[left][right] = RightFirst

        return self.Select[left][right]

    def judgeLL1(self):
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



def main():
    # TODO 1 : 从文件读入文法,要求此文法不包含左递归
    G = Grammar()
    G.read_from_file("./datain3.txt")

    # TODO 2 : 构建语法分析预测器,导入文法，并打印文法
    predictive_parser = Predictive_Parser(grammar=G)
    predictive_parser.grammar.print_grammar()

    # TODO 3 ： 分别求出First、Follow、Select集，并判断文法是否属于LL1文法
    predictive_parser.judgeLL1()

    # TODO 4 ： 构建语法分析预测表并打印
    predictive_parser.cal_table()

    # TODO 5 ： 输入字符串进行语法分析预测


if __name__ == '__main__':
    main()
