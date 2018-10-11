from Grammar import Grammar
import pandas as pd
import numpy as np
class Predictive_Parser:
    def __init__(self,grammar=Grammar()):
        self.grammar = grammar
        self.First = {}
        self.Follow = {}
        self.Select = {}
        self.Table = {}
        self.pdTable = pd.DataFrame()

    def get_first(self,str):
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
                print('sb',i)
                break

            NextFirst = set()
            for j in self.grammar.P[i]:
                NextFirst = NextFirst | self.get_first(j)

            First = (First - {'@'}) | NextFirst
            if '@' not in NextFirst:
                break
        self.First[str]=First
        return First

    def get_follow(self,VN):
        if VN not in self.Follow:
            self.Follow[VN] = set()
        else:
            return self.Follow[VN]-{'@'}

        if VN in self.grammar.start_symbols:
            self.Follow[VN].add('#')

        for nonterminal in self.grammar.nonterminals:
            for str in self.grammar.P[nonterminal]:
                VNpos = str.find(VN)

                if VNpos != -1:
                    if VNpos == len(str)-1:
                        self.Follow[VN] |= self.get_follow(nonterminal)
                    else:
                        nextstr=str[VNpos+1::]
                        NextFirst = self.get_first(nextstr)
                        self.Follow[VN] |= NextFirst
                        if '@' in NextFirst:
                            self.Follow[VN] |= self.get_follow(nonterminal)

        return self.Follow[VN]-{'@'}

    def get_select(self,left,right):
        if left in self.Select:
            if right in self.Select[left]:
                return self.Select[left][right]
            else:
                self.Select[left][right]=set()
        else:
            self.Select[left]={}

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
                    nonterminal,self.get_first(nonterminal)
                )
            )
        print('\nFollow集如下:')
        for nonterminal in self.grammar.nonterminals:
            print(
                'Follow({}) = {}'.format(
                    nonterminal,self.get_follow(nonterminal)
                )
            )

        print('\nSelect集如下:')
        for nonterminal in self.grammar.P:
            for right in self.grammar.P[nonterminal]:
                print('Select({}->{}) = {}'.format(nonterminal,right,self.get_select(nonterminal,right)))
        print('\n')

    def init_table(self):
        # for nonterminal in self.grammar.nonterminals:
        #     self.Table[nonterminal]={}
        #     for terminal in self.grammar.terminals:
        #         self.Table[nonterminal][terminal]=set()
        #     self.Table[nonterminal]['@']=set()

        self.pdTable = pd.DataFrame(
            np.empty(
                shape=(len(self.grammar.nonterminals),len(self.grammar.terminals)+2),
                dtype=str
            ),
            index=list(self.grammar.nonterminals),
            columns=list(self.grammar.terminals)+['@','#']
        )
        print(self.pdTable)
        print(self.pdTable[0])


    def get_table(self):
        self.init_table()
        self.print_table()

        for nonterminal in self.grammar.nonterminals:
            if nonterminal in self.Select:
                for right in self.Select[nonterminal]:
                    print(nonterminal,'->',right,self.Select[nonterminal][right])
                    for terminal in self.Select[nonterminal][right]:
                        self.Table[nonterminal][terminal]=str(nonterminal+'->'+right)

        self.print_table()


    def print_table(self):
        print(end='       ')
        for terminal in self.grammar.terminals:
            print(terminal,end='       ')
        print('@', end='       ')
        print()
        for nonterminal in self.Table:
            print(nonterminal,end='    ')
            for terminal in self.Table[nonterminal]:
                print(self.Table[nonterminal][terminal],end='   ')
            print()
        print()
        print()

    def p(self):
        mypd = pd.DataFrame(data=self.Table,index=['S','A','B','C','D'],columns=['sb','n','(',')','o','#','@','a','t','f'])
        print(mypd)


def main():
    G = Grammar()
    G.read_from_file("./datain3.txt")
    predictive_parser = Predictive_Parser(grammar=G)
    predictive_parser.grammar.print_grammar()
    #predictive_parser.judgeLL1()
    #predictive_parser.get_table()
    predictive_parser.init_table()
if __name__ == '__main__':
    main()