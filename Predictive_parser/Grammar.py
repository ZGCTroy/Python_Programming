class Grammar:
    def __init__(self,alphabet=set(),start_symbols=set(),terminals=set(),nonterminals=set()):
        self.start_symbols = start_symbols
        self.terminals = terminals
        self.nonterminals = nonterminals
        self.P = {}

    def print_grammar(self):
        print("文法的开始符集为:")
        for i in self.start_symbols:
            print(i)
        print("\n文法的终结符集为:")
        for i in self.terminals:
            print(i)
        print("\n文法的非终结符集为:")
        for i in self.nonterminals:
            print(i)
        print("\n文法的规则集为:")
        for nonterminal in self.P:
            for j in self.P[nonterminal]:
                print(nonterminal,'-> ',end='')
                for k in j:
                    print(k,end='')
                print()
        print()

    def read_from_file(self,filepath):
        with open(filepath,'r',encoding='utf-8') as f:
            str = f.readline()
            while True:
                str = f.readline().strip()
                if str == "#":
                    break
                self.start_symbols.add(str)
            str = f.readline()
            while True:
                str = f.readline().strip()
                if str == "#":
                    break
                self.terminals.add(str)
            str = f.readline()
            while True:
                str = f.readline().strip()
                if str == "#":
                    break
                self.nonterminals.add(str)
            str = f.readline()
            while True:
                str = f.readline().strip()
                if str == "#":
                    break
                left, right = str.split("->")
                left = left.strip()
                if left in self.P.keys():
                    self.P[left].add(right)
                else:
                    self.P[left] = set()
                    self.P[left].add(right)
        self.terminals.add('#')
        self.terminals = list(self.terminals)
        self.nonterminals = list(self.nonterminals)
        self.start_symbols = list(self.start_symbols)
        self.terminals.sort()
        self.nonterminals.sort()
        self.start_symbols.sort()


def main():
    G = Grammar()
    G.read_from_file("./datain3.txt")
    G.print_grammar()

if __name__ == '__main__':
    main()
