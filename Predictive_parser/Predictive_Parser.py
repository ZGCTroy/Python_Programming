from Grammar import Grammar

class Predictive_Parser:
    def __init__(self,grammar=Grammar()):
        self.grammar = grammar
        self.predictive_parse_table = {}
        self.epsilonable = set()

    def first(str, firstset=[]):
        t = str[0]
        if t == '&':
            firstset.append('&')
        elif t >= 'A' and t <= 'Z':
            for s in G[t]:
                tempset = first(s, firstset=[])
                firstset.extend(tempset)
                if '&' in tempset and len(str) > 1:
                    firstset.extend(first(str[1:], firstset))
        else:
            firstset.append(t)
        return set(firstset)

    def get_first(self,str):
        First = set()
        print(str,":")
        for i in str:
            print(i)
            if i == 'epsilon':
                First.add(i)
                return First

            if i in self.grammar.terminals:
                First.add(i)
                break

            if i not in self.grammar.nonterminals:
                print('sb')
                break

            NextFirst = set()
            for j in self.grammar.P[i]:
                NextFirst = NextFirst | self.get_first(j)

            First = First | NextFirst
            if 'epsilon' not in NextFirst:
                break
        return First

    def judgeLL1(self):
        t = ('<bexpr>',)
        self.get_first(str=t)


def main():
    G = Grammar()
    G.read_from_file("./datain.txt")
    predictive_parser = Predictive_Parser(grammar=G)
    predictive_parser.grammar.print_grammar()
    t = (1,2)
    #predictive_parser.judgeLL1()
if __name__ == '__main__':
    main()