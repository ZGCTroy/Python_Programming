from Grammar import Grammar
import pandas as pd
import numpy as np

class OperatorPrecedenceAnalysis:
    def __init__(self,grammar=Grammar()):
        self.Grammar = grammar
        self.operator_table = pd.DataFrame(
            data="",
            index=self.Grammar.terminals,
            columns=self.Grammar.terminals
        )
        self.FIRSTVT = pd.DataFrame(
            data=0,
            index=self.Grammar.nonterminals,
            columns=self.Grammar.terminals
        )
        self.LASTVT = pd.DataFrame(
            data=0,
            index=self.Grammar.nonterminals,
            columns=self.Grammar.terminals
        )

    def print_operator_table(self):
        cols = ['+','*','u','i','(',')','#']
        self.operator_table = self.operator_table.ix[:,cols]
        self.operator_table = self.operator_table.ix[cols, :]

        print('FIRSTVT表如下： ')
        print(self.FIRSTVT,'\n')
        print('LASTVT表如下： ')
        print(self.LASTVT,'\n')
        print('算符优先表如下： ')
        print(self.operator_table, '\n')

    def get_firstvt(self):
        # init,若有产生式A->a或A->Ba,则a属于FIRSTVT(A)
        curstack = []
        for left in self.Grammar.P:
            for right in self.Grammar.P[left]:
                if right[0] in self.Grammar.terminals:
                    if self.FIRSTVT[right[0]][left] == 0:
                        self.FIRSTVT[right[0]][left] =1
                        curstack.append((left,right[0]))
                else:
                    if len(right)>1 and right[1] in self.Grammar.terminals:
                        if self.FIRSTVT[right[1]][left] == 0:
                            self.FIRSTVT[right[1]][left] =1
                            curstack.append((left,right[1]))

        # 如果a属于FIRSTVT(B),并且A->B...,则a也属于FIRSTVT(A)
        while len(curstack):
            (B,a) = curstack.pop()
            for A in self.Grammar.P:
                for right in self.Grammar.P[A]:
                    if right[0] == B :
                        if self.FIRSTVT[a][A] == 0:
                            self.FIRSTVT[a][A] = 1
                            curstack.append((A,a))

    def get_lastvt(self):
        # init,若有产生式A->a或A->Ba,则a属于FIRSTVT(A)
        curstack = []
        for left in self.Grammar.P:
            for right in self.Grammar.P[left]:
                if right[-1] in self.Grammar.terminals:
                    if self.LASTVT[right[-1]][left] == 0:
                        self.LASTVT[right[-1]][left] =1
                        curstack.append((left,right[-1]))
                else:
                    if len(right)>1 and right[-2] in self.Grammar.terminals:
                        if self.LASTVT[right[-2]][left] == 0:
                            self.LASTVT[right[-2]][left] =1
                            curstack.append((left,right[-2]))

        # 如果a属于FIRSTVT(B),并且A->B...,则a也属于FIRSTVT(A)
        while len(curstack):
            (B,a) = curstack.pop()
            for A in self.Grammar.P:
                for right in self.Grammar.P[A]:
                    if right[-1] == B :
                        if self.LASTVT[a][A] == 0:
                            self.LASTVT[a][A] = 1
                            curstack.append((A,a))

    def get_operator_table(self):
        # TODO 1 : 求 = 关系
        for left in self.Grammar.P:
            for right in self.Grammar.P[left]:
                for i in range(len(right)-1):
                    if right[i] in self.Grammar.terminals and right[i+1] in self.Grammar.terminals:
                        self.operator_table[right[i+1]][right[i]]="="
                for i in range(1,len(right)-1):
                    if right[i] in self.Grammar.nonterminals:
                        if right[i-1] in self.Grammar.terminals and right[i+1] in self.Grammar.terminals:
                            self.operator_table[right[i + 1]][right[i-1]] = "="

        # TODO 2 : 求FIRSTVT与LASTVT集
        self.get_firstvt()
        self.get_lastvt()

        # TODO 3 : 求 < 关系
        # 有表达式A->...aB...时，对每一b属于FIRSTVT(B),有a<b
        for A in self.Grammar.P:
            for right in self.Grammar.P[A]:
                for i in range(len(right)-1):
                    a = right[i]
                    B = right[i+1]
                    if a in self.Grammar.terminals and B in self.Grammar.nonterminals:
                        row = self.FIRSTVT.loc[B]
                        for b,v in zip(row.index,row):
                            if v == 1:
                                self.operator_table[b][a] = '<'

        # TODO 4 : 求 > 关系
        # 有表达式A->...Bb...时，对每一a属于LASTVT(B),有a>b
        for A in self.Grammar.P:
            for right in self.Grammar.P[A]:
                for i in range(len(right)-1):
                    B = right[i]
                    b = right[i+1]
                    if b in self.Grammar.terminals and B in self.Grammar.nonterminals:
                        row = self.LASTVT.loc[B]
                        for a,v in zip(row.index,row):
                            if v == 1:
                                self.operator_table[b][a] = '>'

    def judge(self, str):
        """
        判断输入串的分析过程
        :param str: 要代入预测分析器进行语法分析预测的字符串
        :return:
        """
        curstack = ['#']
        leftstack = list(str)
        data = []
        step = 0
        while len(curstack):
            step += 1
            topchar =''
            for i in reversed(curstack):
                if i in self.Grammar.terminals:
                    topchar = i
                    break
            relationship = self.operator_table[leftstack[0]][topchar]
            row = {
                '步骤': step,
                '栈':''.join(curstack),
                '优先关系': relationship,
                '当前输入符号': leftstack[0],
                '剩余输入串': '',
                '移进或归约': ''
            }
            if relationship == '<':
                curstack.append(leftstack[0])
                leftstack.pop(0)
                row['移进或归约'] = '移进'
                row['剩余输入串'] = ''.join(leftstack)
            elif relationship == '>' :
                leftpos = len(curstack)-1
                while leftpos>=0:
                    if curstack[leftpos] in self.Grammar.terminals and self.operator_table[topchar][curstack[leftpos]] == '<':
                        break
                    leftpos -= 1
                curstack = curstack[0:leftpos+1]
                curstack.append('F')
                row['移进或归约'] = '归约'
                row['剩余输入串'] = ''.join(leftstack[1:])

            elif topchar == '#':
                row['移进或归约'] = '接受'
                curstack.pop()
            else:
                row['移进或归约'] = '失败'
                data.append(row)
                print(data)
                print('匹配失败')
                return

            data.append(row)

        data = pd.DataFrame(
            data=data,
            columns=[
                '步骤',
                '栈',
                '优先关系',
                '当前输入符号',
                '剩余输入串',
                '移进或归约'
            ]
        )
        print(data)
        print('匹配成功')



def main():
    # TODO 1 : 从文件读入文法,要求此文法不包含左递归
    G = Grammar()
    G.read_from_file("./data5.3_origin.txt")

    # TODO 2 : 构造简单分析分析器
    analysis = OperatorPrecedenceAnalysis(grammar=G)
    analysis.Grammar.print_grammar()

    # TODO 3 : 计算FIRSTVT集
    analysis.get_operator_table()
    analysis.print_operator_table()

    # TODO 4 : 对输入串 i+i# 的算符优先归约过程
    analysis.judge('i+i#')


if __name__ == '__main__':
    main()
