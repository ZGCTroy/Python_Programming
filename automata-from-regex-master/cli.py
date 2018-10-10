#-*-coding:utf-8 -*-
from AutomataTheory import *
import sys

def main():
    inp = "0+1*0"
    if len(sys.argv)>1:
        inp = sys.argv[1]
    print "Regular Expression: ", inp
    #实例一个保存NFA的结构对象
    nfaObj = NFAfromRegex(inp)
    nfa = nfaObj.getNFA()
    #实例一个保存DFA的结构对象
    dfaObj = DFAfromNFA(nfa)
    dfa = dfaObj.getDFA()
    
    # minDFA = dfaObj.getMinimisedDFA()
    print "\nNFA: "
    nfaObj.displayNFA()
    print "\nDFA: "
    dfaObj.displayDFA()
    # print "\nMinimised DFA: "
    # dfaObj.displayMinimisedDFA()
    if isInstalled("dot"):        
        drawGraph(dfa, "dfa")
        drawGraph(nfa, "nfa")
        # drawGraph(minDFA, "mdfa")
        print "\nGraphs have been created in the code directory"
        print minDFA.getDotFile()

if __name__  ==  '__main__':
    t = time.time()
    try:
        main()
    except BaseException as e:
        print "\nFailure:", e
    print "\nExecution time: ", time.time() - t, "seconds"
