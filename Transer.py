"""
FileName    : Transer.py
Author      : 郑光聪,20167851,160211
Institution : School of computer and communication engineering, Northeastern University at Qinhuangdao
Version     : 0.1
Date        : 2018-09-19
Description : transer NFA to DFA
"""
from DFA import *
from NFA import *


class Transer:
    def __init__(self,NFA=NFA(),DFA=DFA()):
        """
        Args:
            NFA       : 不确定的有穷自动机，类NFA
            DFA       : 确定的有穷自动机，类DFA
        """
        self.NFA=NFA
        self.DFA=DFA





def main():
    transer = Transer()
    transer.NFA.file_read("./datain.txt")
    transer.change()

if __name__=='__main__':
    main()
