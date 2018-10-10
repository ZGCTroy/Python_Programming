'''
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
'''
G = {}
# input
print("请输入文法的开始符:")
S = input()
print("请输入文法.(如:'S->AB').最后文法以'#->#'结束.")
while True:
    key,value = input().split("->")
    if key=='#' and value == '#': break
    elif key in G.keys():G[key].append(value)
    else: G[key] = [value]

# print(G)

# first
def first(str,firstset=[]):
    t = str[0]
    if t=='&': firstset.append('&')
    elif t>='A' and t<='Z':
        for s in G[t]:
            tempset = first(s, firstset=[])
            firstset.extend(tempset)
            if '&' in tempset and len(str)>1:
                firstset.extend(first(str[1:],firstset))                 
    else: firstset.append(t)
    return set(firstset)

# print first
# print(first(input(), firstset=[]))

# follow
def follow(ch,followset=[],father=[]):
    father.append(ch)
    if ch==S:
        followset.append('#')
#         return followset
    for key in G:
        for s in G[key]:
            if ch in s:
#                 print(s,s.index(ch))
                i = s.index(ch)
                if i == len(s)-1:
#                     print(father)
                    if key in father: continue
                    followset.extend(follow(key,followset,father))
                elif i < len(s)-1:
                    tempset = first(s[i+1:], firstset=[])
                    #print(tempset)
                    if '&' in tempset:
                        if key in father: continue
#                         print('tempset=',tempset)
                        tempset.remove('&')
                        followset.extend(tempset)
#                         print('tempset=',tempset)
                        followset.extend(follow(key,followset,father))
                    else:followset.extend(tempset)
    return set(followset)

# print follow             
# print(follow(input(), followset=[]))

# select
selectset={}
def select():
    for key in G:
        for s in G[key]:
            selectset[key+'->'+s] = first(s, firstset=[])
            if '&' in selectset[key+'->'+s]:
                selectset[key+'->'+s].remove('&')
                selectset[key+'->'+s] = selectset[key+'->'+s] | set(follow(key, followset=[],father=[]))
    return selectset

# print selectset
# print(select())

def judeLL1():
    flag = True
    select()
    print('文法的select set如下：')
    for key in selectset:
        print(key+':',selectset[key])
    print('LL(1)判断过程如下(即select集合的求交集过程)：')
    for key1 in selectset:
        for key2 in selectset:
            if key1==key2: continue
            elif key1[0]==key2[0]:
                print(selectset[key1],'U',selectset[key2],end='')
                tempset = selectset[key1] & selectset[key2]
                if tempset:
                    flag = False
                    print(' =',tempset)
                else:print(' = NULL')
    return flag
    
# jude LL(1)         
# judeLL1() 

def check():
    print('-------------------------------------')
    print('输入1进入人脑计算select set！')
    t = input()
    if int(t)==1:
        while True:
            print('求first set 按1，follow set 按2，退出按0：')
            ot = input()
            if int(ot)==1:
                print('请输入要求first set 的字符串：')
                print('first set:',first(input(),firstset=[]))
            if int(ot)==2:
                print('请输入要求follow set 的字符串：')
                print('follow set:',follow(input(),followset=[],father=[]))
            if int(ot)==0:
                print('欢迎下次进入！')
                break
    else:
        print('程序已关闭，欢迎下次进入！')





    