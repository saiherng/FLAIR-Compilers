"""
    author:      Rishabh dalal, Sai Herng
    description: final codegen
"""

##free register pool : 1,2,3,4

##  0 .. 0
##  5 .. Staus ptr
##  6 .. top ptr
##  7 .. PC


## -- AR-- 
##status pointer pointing to 0 of this ar

## -n->-2    .. n arguments
## -1        .. return val
## 0         .. addr to branch back to
## 1         .. r0
## 2         .. r1
## 3         .. r2
## 4         .. r3
## 5         .. r4


class CodeGenerator:
    def __init__(self, ast, symbol_table, caller_called,):
        self.ast = ast
        self.IR = ast.createIR()
        self.symbol_table = symbol_table
        self.function_call = caller_called
        self.jumps = []
        self.result = ""
        self.count = 0
        self.initialize()
        self.registerMap = [0,[],[],[],[]]
        self.handleIR(self.IR)
        self.nextUse = {}
        self.function = None
        
    def generate(self):
        return self.result
    
    def initialize(self):
        #status pointer
        self.comment()
        self.outOff("LDC", 5,-1, 0)
        #top ptr
        self.outOff("LDC", 6,2, 0)

    def handleIR(self, lst):
        for i in range(len(lst)):
            if lst[i][0] == 'ENTRY':
                self.startFunction(i, lst)
            elif lst[i][0] == 'EXIT':
                self.endFunction()
            elif lst[i][0] == 'RETURN':
                self.returnVal(i)
            elif lst[i][0] == '':
                self.handleAssn(lst[i])
            elif lst[i][0] == '+-/*':
                self.handleArithOp(lst[i])
            elif lst[i][0] in ['not', 'and', 'or']:
                self.handleBoolOp(lst[i])
            else:
                print('Can\'t handle now', lst[i])

    def startFunction(self, index, lst):
        self.function = lst[index][1]
        for i in range(6):
            self.outOff('ST', i, i+1, 5)

        while lst[index] != 'END':
            op1 = lst[index][1]
            if op1 != '':
                if op1 in self.nextUse:
                    self.nextUse[op1].append(index)
                else:
                    self.nextUse[op1] = [index]

            if op2 != '':
                if op2 in self.nextUse:
                    self.nextUse[op2].append(index)
                else:
                    self.nextUse[op2] = [index]
            index += 1
                    
    def endFunction(self):
        for i in range(6):
            outOff('LD', i, i+1, 5)
        outOff('LD', 7, 0, 5)

    def returnVal(self, i):
        outOff('ST', inReg(i[1]), -1, 5)
        
    def handleAssn(self, i):
        if inReg(i[3]) != -1:
            reg = getRegister()
            
            if i[1].isdigit():
                outOff('LDC', reg, str(i[1]), 0)
            else:
                if i[1] == 'true':
                    outOff('LDA', reg, str(1), 0)
                elif i[1] == 'false':
                    outOff('LDA', reg, str(0), 0)
                else:
                    total = len(self.symbol_table[self.function])
                    for j in range(total - 1):
                        if self.symbol_table[j][0] == i[1]:
                            outOff('LD', reg, total-j+2, 5)
                            break
            
    def handleArithOp(self, i):
        storeAdd = getRegister()
        outTwo('LDA', storeAdd, i[-1])
        
        if inReg(i[1]) != -1:
            para1 = getReg(i[1])
        else:
            para1 = getRegister()
            outTwo('LD', para1, i[1])

        if i[2] == '':
            ## t2 := - t1
            ##Handle
            pass

        else:
        
            if inReg(i[2]) != -1:
                para2 = getReg(i[1])
            else:
                para2 = getRegister()
                outTwo('LD', para2, i[2])

            index = inReg(i[3])
            if i[0] == "+":
                op = 'ADD'
            elif i[0] == "-":
                op = 'SUB'
            elif i[0] == '*':
                op = 'MUL'
            else:
                i[0] = 'DIV'
                
            if index != -1:
                outClean('ADD', index, para1, para2)
                outOff('ST', index, 0, storeAdd) 
            else:
                outClean('ADD', para1, para1, para2)
                outOff('ST', para1, 0, storeAdd)       

    def handleBoolOp(self, i):

        storeAdd = getRegister()
        outTwo('LDA', storeAdd, i[-1])

        if inReg(i[1]) != -1:
            para1 = getReg(i[1])
        else:
            para1 = getRegister()
            outTwo('LD', para1, i[1])

        index = inReg(i[3])
            
        if index != -1:
            if i[0] == 'NOT':
                ##
                pass
            elif i[0] == 'OR':
                ##
                pass
            elif i[0] == 'AND':
                ##
                pass

            outOff('ST', index, 0, storeAdd) 
        else:
            if i[0] == 'NOT':
                ##
                pass
            elif i[0] == 'OR':
                ##
                pass
            elif i[0] == 'AND':
                ##
                pass
            outOff('ST', para1, 0, storeAdd)
            

    def inReg(self, x):
        for i in range(1, len(self.registerMap)+1):
            for j in self.registerMap[i]:
                if j == x:
                    return i
        return -1

    def outOff(self, op, reg1, off, reg2):
        val = str(self.count)+ ": " + op + " " + str(reg1) + ","\
              + str(off) +"(" +str(reg2) + ")\n"
        self.result += val
    
        self.count += 1

    def outTwo(self, op, reg1, reg2):
        val = str(self.count)+ ": " + op + " " + str(reg1) + ","\
              + str(reg2) + "\n"
        self.result += val
    
        self.count += 1

    def outClean(self, op, reg1, reg2, reg3):
        val = str(self.count)+ ": " + op + " " + str(reg1) + ","\
              + str(reg2) +"," +str(reg3) + "\n"
        self.result += val
    
        self.count += 1

    def comment(self, msg=None):
        if msg:
            self.result += msg + '\n'
        else:
            self.result += '\n'
