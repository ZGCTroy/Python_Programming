from Grammar import Grammar

class Predictive_Parser:
    def __init__(self,grammar=Grammar()):
        self.grammar = grammar
        self.predictive_parse_table = {}
        self.First = {}
        self.Follow = {}


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
        Select = set()
        RightFirst = self.get_first(right)
        if '@' in RightFirst:
            Select = RightFirst | self.get_follow(left)
        else:
            Select = RightFirst
        return Select

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
            for j in self.grammar.P[nonterminal]:
                print('Select({}->{}) = {}'.format(nonterminal,j,self.get_select(nonterminal,j)))

        self.select()






def main():
    G = Grammar()
    G.read_from_file("./datain3.txt")
    predictive_parser = Predictive_Parser(grammar=G)
    predictive_parser.grammar.print_grammar()
    predictive_parser.judgeLL1()
if __name__ == '__main__':
    main()