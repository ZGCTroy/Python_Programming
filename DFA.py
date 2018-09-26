"""
FileName    : DFA.py
Author      : 郑光聪,20167851,160211
Institution : School of computer and communication engineering, Northeastern University at Qinhuangdao
Version     : 0.1
Date        : 2018-09-19
Description : transer NFA to DFA
"""
class DFA:
    def __init__(self,K=set(),Sigma=set(),f=dict(),K0=set(),Kt=set()):
        """
        Args:
            K       : 一个有穷集，它的每个元素称为一个状态
            Sigma   : 一个有穷字母表，它的每个元素称为一个输入符号
            f       : 状态转换
            S       : 一个非空初态集
            Z       : 一个终态集
        """
        self.K = K
        self.Sigma=Sigma
        self.f=f
        self.K0=K0
        self.Kt=Kt

    def minimize(self):
        C=[]
        C.append(self.Kt)
        C.append(self.K.difference(self.Kt))
        num_of_subset=2
        while True:
            for subset in C:
                for item in subset:
                    for i in self.f:
                        for j in self.f[i]:
                            print(j)
            if len(newC) <= num_of_subset:
                break
            else:
                num_of_subset=len(newC)




    def read_from_keyboard(self):
        """
        从键盘读入NFA
        """
        self.K = eval(str(input("所有状态集K,如{1,2,3} : ")))
        self.K0 = eval(str(input("初始状态集K0,如{1} : ")))
        self.Kt = eval(str(input("终止状态集Kt,如{3} : ")))
        self.Sigma = eval(str(input("输入字符集Sigma,如{'a','b'} : ")))
        self.f = eval(str(input("状态转移集f,如{'a':[[1,2],[1,3]],'b':[[2,3]]} : ")))

    def read_from_file(self,filepath):
        """
        从文件读入NFA
        Args:
            filepath ：文件路径
        """
        with open(filepath) as f:
            lines=[]
            for line in f:
                lines.append(line)
            self.K = eval(lines[0])
            self.K0=eval(lines[1])
            self.Kt=eval(lines[2])
            self.Sigma=eval(lines[3])
            self.f=eval(lines[4])

    def print(self):
        print("此DFA的属性如下:\n")
        print("状态集K为", self.K)
        print()
        print("初始状态集K0为", self.K0)
        print()
        print("终止状态集Kt为", self.Kt)
        print()
        print("输入字符集Sigma为", self.Sigma)
        print()
        print("状态转移集f为", self.f)

def main():
    D = DFA()
    D.read_from_file("./datain.txt")
    D.print()
    D.minimize()

if __name__=='__main__':
    main()
