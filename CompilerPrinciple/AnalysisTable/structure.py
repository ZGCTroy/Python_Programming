'''
Created on 2017年12月20日
 
@author: Busy
'''
'''
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

from AnalysisTable.SelectSet import selectset, S

# table
# judeLL1()
def inputstr():
    print('请输入非终集符（一个字符串）')
    nstr = list(input())
    print('请输入终集符（一个字符串）')
    tstr = list(input())
    return nstr,tstr
# tb = {}
def createtable(nstr,tstr):
    tb={}
    print("%5s " % (' '),end="")
    for s in tstr:
        print("%5s " % (s),end="");
    print("|\n")
    for x in nstr:
        print("%5s " % (x),end="")
        for y in tstr:
            flag = False
            for key in selectset:
                if x==key[0] and y in selectset[key]:
                    print("%5s " % (key[3:]),end="")
                    tb[x+','+y] = key[3:]
                    flag = True
                    break
                    
            if flag==False: print("%5s " % ('-'),end="")
        print('|')
    return tb
# createtable()
# print(tb)
# analysis
def analysis():
    nstr,tstr = inputstr()
    print('预测分析表：')
    tb = createtable(nstr,tstr)
    print('----------------------------------------------------')
    print('请输入需分析的字符串(字符串以#结尾)')
    instr = list(input())
    stack=['#',S]
    count = 0
    print('分析过程:')
    while stack:
        if stack[-1] in tstr:
            if stack[-1]==instr[0] and instr[0]=='#':
                t = instr[0]
                count += 1
                stack.pop()
                instr=instr[1:]
                print("%25s %5s %35s" % (stack,t,instr))
#                 print(stack,"%20s" % (t),instr)
            elif stack[-1]==instr[0] and instr[0]!='#':
                t=instr[0]
                count += 1
                stack.pop()
                instr=instr[1:]
                print("%25s %5s %35s" % (stack,t,instr))
#                 print(stack,"%20s" % (t),instr)
        elif stack[-1] in nstr:
            while True:
                for i in reversed(tb[stack.pop()+','+instr[0]]):
                    if i == '&':break
                    stack.append(i)
                print("%25s %5s %35s" % (stack,instr[0],instr))
#                 print(stack,"%20s" % (instr[0]),instr)
                if stack[-1] in tstr: break
                
    print('分析结果：字符串已接收！') 
# analysis()
                
                
            