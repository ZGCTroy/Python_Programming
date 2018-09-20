"""
FileName    : NFA.py
Author      : 郑光聪,20167851,160211
Institution : School of computer and communication engineering, Northeastern University at Qinhuangdao
Version     : 0.1
Date        : 2018-09-19
Description : transer NFA to DFA
"""
from DFA import *

class NFA:
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

    def determine(self):
        """
        将NFA确定化为DFA
        Returns: DFA
        """
        D =DFA()
        C=list()
        T0=self.get_closure(self.K0)
        C.append(T0)
        D.K.add(0)
        D.K0.add(0)
        for i in self.Sigma:
            if i!='e0':
                D.Sigma.add(i)
                D.f[i]=[]
        l=0
        r=1
        while l<r:
            T=C[l]
            for i in self.Sigma:
                if i!='e0':
                    newT = self.get_closure(self.move(T,i))
                    if newT not in C:
                        # 加入DFA的总状态集
                        D.K.add(r)
                        # 如果DFA的状态中包含NFA的终态，则此状态为DFA的终态
                        if self.Kt.issubset(newT):
                            D.Kt.add(r)
                        C.append(newT)
                        # 添加DFA的f
                        D.f[i].append([l, r])
                        r=r+1
                    else:
                        pos=0
                        for t in C:
                            if t==newT:
                                break
                            pos=pos+1
                        D.f[i].append([l,pos])
            l = l + 1
        return D

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

    def get_closure(self,T):
        """
        获得集合T的闭包U
        Args:
            T ：集合T
        Returns:
            U : 集合T中所有状态经过任意条e0所能到达的状态集合U
        """
        U = set()
        while len(T)>0:
            for t in list(T):
                U.add(t)
                for v in self.f['e0']:
                    if t==v[0] and v[1] not in U:
                        T.add(v[1])
            T.remove(t)
        return U

    def move(self,T,a):
        U = set()
        for t in T:
            for j in self.f[a]:
                if t==j[0]:
                    U.add(j[1])
        return U

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
    N = NFA()
    N.read_from_file(filepath="./datain.txt")
    N.print()
    D = N.determine()
    D.print()

if __name__=='__main__':
    main()
