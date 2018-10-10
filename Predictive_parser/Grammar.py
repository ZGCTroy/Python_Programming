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
        for i in self.P:
            for j in self.P[i]:
                print(i,' -> ',end=' ')
                for k in j:
                    print(k,end=' ')
                print()
        print()

    def read_from_keyboard(self):
        print("请输入文法的开始符,一行一个，以#结束:")
        while True:
            str = input().strip()
            if str == "#":
                break
            self.start_symbols.add(str)

        print("请输入文法的终结符集,一行一个，以#结束:")
        while True:
            str = input().strip()
            if str == "#":
                break
            self.terminals.add(str)

        print("请输入文法的非终结符集,一行一个，以#结束:")
        while True:
            str = input().strip()
            if str == "#":
                break
            self.nonterminals.add(str)

        print("请输入文法.(如:'S->AB').最后文法以'#'结束.")
        while True:
            str = input().strip()
            if str == "#":
                break
            left, right = str.split("->")
            left = left.strip()
            right = tuple(right.strip().split(" "))
            if left in self.P.keys():
                self.P[left].add(right)
            else:
                self.P[left] = set()
                self.P[left].add(right)

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
                right = tuple(right.strip().split(" "))
                if left in self.P.keys():
                    self.P[left].add(right)
                else:
                    self.P[left] = set()
                    self.P[left].add(right)

def main():
    G = Grammar()
    #G.read_from_keyboard()
    G.read_from_file("./datain.txt")
    G.print_grammar()

if __name__ == '__main__':
    main()
