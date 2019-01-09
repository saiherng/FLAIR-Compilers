"""
    author:      Rishabh Dalal, Sai Herng
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
        for i in self.IR:
            print(i)
        self.symbol_table = symbol_table
        self.function_call = caller_called
        self.new_symbol_table = {}
        self.jumps = []
        self.result = ""
        self.count = 36
        self.offset = 6
        self.last = []

        self.nextUse = {}
        self.registerMap = [0,0,0,0,0]
        self.function = None
        self.assn = {}
        
        
    def generate(self):
        self.initialize()
        
        print(self.result)
        
    def initialize(self):
        #status pointer
        self.comment()
        self.outOff("LDC", 5,-1, 0)
        #top ptr
        self.outOff("LDC", 6,2, 0)
        self.prolog('main')
        self.prolog('print')
        self.outClean('HALT', 0,0,0)
        self.jumps[1].append(self.print_ar())
        self.jumps[0].append(self.main_ar())
        self.handleIR(self.IR)
        self.handle_jumps()

    def handle_jumps(self):
        self.comment()
        for i in self.jumps:
            val = str(i[0])+ ": LDA 7," + str(i[1]) +"(0)\n"
            self.result += val

    def main_ar(self):
        jump_to = self.count
                       
        for i in range(5):
            self.outOff('ST', i, i+1, 5)

        ##return 1
        self.outOff('LDC', 2, 1, 0)
        self.outOff('ST', 2, -1, 5)
        
        ##restore registers
        for i in range(5):
            self.outOff('LD', i, i+1, 5)

        self.outOff('LD', 7,0,5)
        return jump_to

    def print_ar(self):
        jump_to = self.count
        
        for i in range(5):
            self.outOff('ST', i, i+1, 5)

        ##only 1 formal parameter
        self.outOff('LD', 1, -1, 5)     
        self.outClean('OUT', 1, 0, 0)

        for i in range(5):
            self.outOff('LD', i, i+1, 5)
        self.outOff('LD', 7,0,5)
        return jump_to
            
    def handleIR(self, lst):
        
        for i in range(len(lst)):
            print("Handling", lst[i])
            if lst[i][0] == 'ENTRY':
                print("1")
                self.startFunction(i, lst)
            elif lst[i][0] == 'EXIT':
                print("2")
                self.endFunction()
            elif lst[i][0] == 'RETURN':
                print("3")
                self.returnVal(lst[i])
            elif lst[i][0] == '':
                print("4")
                self.handleAssn(lst[i])
            elif lst[i][0] in '+-/*':
                print("5")
                self.handleArithOp(lst[i])
            elif lst[i][0] in ['not', 'and', 'or']:
                print("6")
                self.handleBoolOp(lst[i])
            else:
                print("7")
                print('Can\'t handle now', lst[i])
        #print("RESULT\n" +  self.result, '\n')

    def startFunction(self, index, lst):
        self.function = lst[index][1]
        for i in range(6):
            #self.outOff('ST', i, i+1, 5)
            self.outOff('ST', i, i+1, 5)
        index += 1
        print()
        while lst[index][0] != 'EXIT':
            #print('1', lst[index])
            op1 = lst[index][1]
            op2 = lst[index][2]
            
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
        print("self.nextUse\n", self.nextUse)
        print()
                    
    def endFunction(self):
        for i in range(6):
            #self.outOff('LD', i, i+1, 5)
            self.outOff('LD', i, i+1, 5)
        #self.outOff('LD', 7, 0, 5)
        self.outOff('LD', 7, 0, 5)

    def returnVal(self, i):
        print('i[1]', i[1])
        #self.outOff('ST', self.assn[i[1]], -1, 5)
        print("self.last", self.last)
        if i[1] == self.last[0]:
            self.outOff('ST', self.last[1], -1, 5)
        else:
            print("Seomthing went wrong")

    def getRegister(self, j):
        l = []
        for i in range(1, len(self.registerMap)):
            if self.registerMap[i] == 0:
                self.registerMap[i] = j[-1]
                print("Giving", i)
                return i
            elif self.registerMap[i] not in self.nextUse:
                self.registerMap[i] = j[-1]
                print("Giving", i)
                return i
            else:
                l.append(self.nextUse[self.registerMap[i]])
        mnm = min(l)
        print("Giving", l.index(mnm))
        return l.index(mnm)
                    

    def handleAssn(self, i):
        reg = self.getRegister(i)
        print("Register returned:", reg)
        #print("I", i[-1])
        self.assn[i[-1]] = reg
        if i[1].isdigit():

            self.outOff('LDC', reg, str(i[1]), 0)
        else:
            if i[1] == 'true':

                self.outOff('LDC', reg, str(1), 0)
                
            elif i[1] == 'false':

                self.outOff('LDC', reg, str(0), 0)
            else:

                total = len(self.symbol_table[self.function])
                for j in range(total - 1):
                    if self.symbol_table[self.function][j][0] == i[1]:
                        
                        self.outOff('LD', reg, -1*(total-j), 5)
                        break     

    def handleBoolOp(self, i):

        regToOutput = getRegister(i)
        print("REgister returned:", regToOutput)
        outOff('LDA', regToOutput, getAddInStackFrame(i[-1]), 5)
        
        if i[0] == 'not':
            ###
            pass
        
        elif i[0] == 'or':
            ##
            pass
        elif i[0] == 'and':
            ##
            pass

        outOff('ST', operand, 0, regToOutput)
        self.assn = {}

    def handleArithOp(self, i):
        regToOutput = self.getRegister(i[-1])
        #self.outOff('LDA', regToOutput, self.getAddInStackFrame(i[-1]), 5)
        self.outOff('LDA', regToOutput, self.offset, 5)
        self.new_symbol_table[i[-1]] = self.offset
        self.offset += 1
        

        if not i[1] in self.assn:
            self.assn[i[1]] = self.getRegister(i[1])
            self.outOff('LD', self.assn[i[1]], \
                        self.new_symbol_table[i[1]], 5)
        if not i[2] in self.assn:
            self.assn[i[2]] = self.getRegister(i[2])
            self.outOff('LD', self.assn[i[2]], \
                        self.new_symbol_table[i[2]], 5)
        if i[0] == '-':
            if i[2] != '':
                outClean('SUB', self.assn[i[1]], self.assn[i[1]], \
                     self.assn[i[2]])
            else:
                reg = getRegister(['','','','-1'])
                outOff('LDC', reg, str(-1), 0)
                outClean('MUL', self.assn[i[1]], self.assn[i[1]], \
                     reg)                                  
        elif i[0] == '*':
            outClean('MUL', self.assn[i[1]], self.assn[i[1]], \
                     self.assn[i[2]])
        elif i[0] == '/':
            outClean('DIV', self.assn[i[1]], self.assn[i[1]], \
                     self.assn[i[2]])
        else:
            #self.outClean('ADD', self.assn[i[1]], self.assn[i[1]], \
            #         self.assn[i[2]])
            self.outClean('ADD', self.assn[i[1]], self.assn[i[1]], \
                     self.assn[i[2]])
        #self.outOff('ST', self.assn[i[1]], 0, regToOutput)
        self.outOff('ST', self.assn[i[1]], 0, regToOutput)
        self.last = [i[-1], self.assn[i[1]]]
        self.assn = {}
        

    def getAddInStackFrame(self, i):
        i = i[1:]
        return str(6+int(i))

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
