'''
Created on 2017年12月20日
 
@author: Busy
'''
'''
样例一:
S
S->AB
A->&
B->&
C->AD
D->aS
S->bC
A->b
B->aD
C->b
D->c
#->#
样例二:
S
S->LA
L->i:
L->&
A->i=e
#->#
样例三:
S
S->iA
A->:i=e
A->=e
#->#
样例四
E
E->TA
T->FB
F->i
F->(E)
A->+TA
A->&
B->*FB
B->&
#->#
EATBF
i+*()#
i+i*i#
'''

from AnalysisTable.SelectSet import judeLL1, check
from AnalysisTable.structure import analysis
try:
    flag = judeLL1()
except:
    flag = False
    print('文法输入有误，是否输入了左递归文法！')
if flag: 
    print("判断结果：该文法是LL(1)")
    print('----------------------------------------------------')
    try:
        analysis()
    except:
        print('字符串分析失败！')
else:print("判断结果：该文法不是LL(1)")
check()