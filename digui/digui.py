'''
@author: ZGC
@license: (C) Copyright 2013-2018, Node Supply Chain Manager Corporation Limited.
@contact: zgc_troy@163.com
@github:  https://github.com/ZGCTroy
@file: Predictive_Parser.py
@time: 2018/10/11 17:29
@desc:
'''

class Predictive_Parser:
    def __init__(self):
        self.str_id = 0
        self.str = ""

    def MatchToken(self,ch):
        curchar = self.str[self.str_id]
        print(curchar,ch)
        if curchar == ch:
            self.str_id += 1
            return True
        else:
            return False

    def ParseE(self):
        curchar = self.str[self.str_id]
        if curchar == 'e':
            if self.MatchToken('e') == False:
                return False
            if self.ParseB() == False:
                return False
            if self.MatchToken('a') == False:
                return False
            if self.ParseA() == False:
                return False
        else:
            return False
        return True

    def ParseA(self):
        curchar = self.str[self.str_id]
        if curchar == 'a':
            if self.MatchToken('a') == False:
                return False
        elif curchar == 'b':
            if self.MatchToken('b') == False:
                return False
            if self.ParseA() == False:
                return False
            if self.MatchToken('c') == False:
                return False
            if self.ParseB() == False:
                return False
        else:
            return False
        return True

    def ParseB(self):
        curchar = self.str[self.str_id]
        if curchar == 'a':
            if self.MatchToken('a') == False:
                return False
            if self.ParseC() == False:
                return False
        elif curchar == 'd':
            if self.MatchToken('d') == False:
                return False
            if self.ParseE() == False:
                return False
            if self.MatchToken('d') == False:
                return False
        else:
            return False
        return True

    def ParseC(self):
        curchar = self.str[self.str_id]
        if curchar == 'e':
            if self.MatchToken('e') == False:
                return False
        elif curchar == 'd':
            if self.MatchToken('d') == False:
                return False
            if self.ParseC() == False:
                return False
        else:
            return False
        return True

    def judge(self, str):
        """
        判断输入串的分析过程
        :param str: 要代入预测分析器进行语法分析预测的字符串
        :return:
        """
        self.str = str
        self.str_id = 0
        print(str)
        if self.ParseE():
            print('True\n')
        else:
            print('False\n')



def main():

    parser = Predictive_Parser()
    parser.judge('eadeaa#')

    parser.judge('edeaebd#')

    parser.judge('edeaeaadabacae#')



if __name__ == '__main__':
    main()

