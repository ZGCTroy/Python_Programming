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
        self.FIRSTVT = []
        self.LASTVT = []

    def print_operator_table(self):
        cols = ['+','*','u','i','(',')','#']
        self.operator_table = self.operator_table.ix[:,cols]
        self.operator_table = self.operator_table.ix[cols, :]
        print(self.operator_table)

    def get_firstvt(self):
        # init,若有产生式A->a或A->Ba,则a属于FIRSTVT(A)
        for left in self.Grammar.P:
            for right in self.Grammar.P[left]:
                if right != "":
                    if right[0] in self.Grammar.terminals:
                        self.FIRSTVT
        return None


    def get_lastvt(self):
        return None

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



if __name__ == '__main__':
    main()
