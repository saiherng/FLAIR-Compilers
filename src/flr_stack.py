"""
    @author:       Sai Herng, Rishabh Dalal
    @description:  LL1 parser for flair
    
"""


class Stack:
    def __init__(self):
        self.lst = []
        
    def top(self):
        if len(self.lst) <= 0:
            return None
        return self.lst[-1]

    def pop(self):
        if len(self.lst) <= 0:
            raise ValueError("Popping from empty stack")
        return self.lst.pop()

    def pushRule(self, lst):
        for i in range(len(lst)-1,-1,-1):
            if lst[i] != "epsilon":
                self.lst.append(lst[i])

    def size(self):
        return len(self.lst)

    def pushProper(self, obj):
        self.lst.append(obj)

    def __str__(self):
        output = "\nStack:\n"
        for i in self.lst:
            output += "-> " + str(i) + "\n"
        return output
