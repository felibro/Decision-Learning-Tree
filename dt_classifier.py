from math import log
from copy import deepcopy
import random
import sys

class Node:
    def __init__(self, val, split, ye, no):
        self.val = val
        self.spl = split
        self.ye = ye
        self.no = no
    
def partition(split, items, cond):
    y = [x for x in items if x[split]==cond]
    yc = [x for x in y if x[0]=="cat"]
    yd = [x for x in y if x[0]=="dog"]
    return y,yc,yd

def smalllog(y,yc,yd):
    a= b= 0 
    if len(yc)!=0 and len(yd)!=0:
        a = len(yc)*log(len(yc)/len(y))
        b = len(yd)*log(len(yd)/len(y))
    return a + b

def logloss(y,yc,yd,n,nc,nd):
    yl = smalllog(y,yc,yd)
    nl = smalllog(n,nc,nd)
    return -(nl+yl)/(len(y)+len(n))

def minloss(c, e):
    listy = []
    for i in c:
        y,yc,yd = partition(i, e, "y")
        n,nc,nd = partition(i, e, "n")
       
        if len(y)==0 or len(n)==0:
            continue
 
        x = logloss(y,yc,yd,n,nc,nd)
        listy.append((i, x))
    if len(listy)==0:
        return 0,0
    return min(listy, key=lambda x: x[1])

def dsl(c:"poss cond set", y: "target feat", e:"set of traing ex", stop):  
    g = minloss(c,e)[1]
    if g ==0  or stop == 0:
        cat = [x for x in e if x[0]=="cat"]
        dog = [x for x in e if x[0]=="dog"] 
        return Node({"cat":len(cat), "dog":len(dog)}, None, None, None)      
    else:
        ml = minloss(c,e)[0] 
        c.remove(ml)
        yes = partition(ml, e, "y")[0]
        yT = dsl(c, y, yes, stop-1)
        no = partition(ml, e, "n")[0]
        nT = dsl(c, y, no, stop-1)
        return Node(None, ml-1, yT, nT)
        
def classify(oneTest, nod):
    if nod.val:
        return nod.val
    if oneTest[nod.spl]=="y":
        return classify(oneTest, nod.ye)
    return classify(oneTest,nod.no)

def check(test):
    with open("pets_train.csv", "r") as f:
        b = f.read()
    with open(test, "r") as g:
        d = g.read()
        
    training = [i.split(',') for i in b.split("\n")]
    colNums = len(training[0]) #first 0 is cat/dog class; rest is y/n
    c = [i for i in range(1, colNums)]
    #ans = [x.split()[0] for x in h.split('\n')]
    test_case = [i.split(",") for i in d.split("\n")]
    
    l = dsl(deepcopy(c), minloss(c,training)[0], training,4)

    for j,i in enumerate(test_case):
        k = classify(i, l)
        if k["cat"]==k["dog"]:
            a = random.choice(["cat", "dog"])
            v = 0.5
        elif k["cat"]>k["dog"]:
            a = "cat"
            v = k["cat"]/(k["cat"]+k["dog"])
        else:
            a="dog"
            v = k["dog"]/(k["cat"]+k["dog"])
        
        print(a, v)
    
if __name__ == "__main__":
    f = sys.argv[1]
    check(f)
