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
## 2         .. r1
## 3         .. r2
## 4         .. r3


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
        self.count = 0
        self.offset = 4
        self.function = None
        self.start = 0
        
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
        self.handleIR(self.IR)
        self.jumps[0].append(self.start)
        
        self.handle_jumps()

    def handle_jumps(self):
        for i in self.jumps:
            val = str(i[0])+ ": LDA 7," + str(i[1]) +"(0)\n"
            self.result += val

    def prolog(self, fnName):
        offset = 0

        for i in range(len(self.symbol_table[fnName]) - 1):
            self.outOff('ST', 1, offset+1,6)
            offset += 1
            
        self.outOff('LDA', 1,6, 7) ##store return add
        self.outOff('ST',  1, offset+1, 6)
        self.outOff('ST',  5, offset+7, 6)
        self.outOff('LDA', 5, offset+1, 6)
        self.outOff('ST',  6, offset+8, 6)
        self.outOff('LDA',  6, offset+9, 6)
        ##jump
        self.jumps.append([self.count])
        self.count += 1


        self.outOff('LD',  1, offset+1, 6)
        self.outOff('LD',  5, offset+7, 6)
        
        if fnName != 'print':
            ##self.out does not have a return
            self.outOff('LD', 1, 0, 6)

    def main_ar(self):
        jump_to = self.count
                       
        for i in range(1,4):
            self.outOff('ST', i, i, 5)

        ##return 1
        self.outOff('LDC', 2, 1, 0)
        self.outOff('ST', 2, -1, 5)
        
        ##restore registers
        for i in range(1,4):
            self.outOff('LD', i, i, 5)

        self.outOff('LD', 7,0,5)
        return jump_to

    def print_ar(self):
        jump_to = self.count
        
        for i in range(1,4):
            self.outOff('ST', i, i, 5)

        ##only 1 formal parameter
        self.outOff('LD', 1, -1, 5)     
        self.outClean('OUT', 1, 0, 0)

        for i in range(1,4):
            self.outOff('LD', i, i, 5)
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

    def startFunction(self, index, lst):
        self.start = self.count
        self.function = lst[index][1]
        for i in range(1,4):
            #self.outOff('ST', i, i+1, 5)
            self.outOff('ST', i, i, 5)
        index += 1
                    
    def endFunction(self):
        for i in range(1,4):
            self.outOff('LD', i, i, 5)
        self.outOff('LD', 7, 0, 5)

    def returnVal(self, i):
        self.outOff('LD', 1, self.new_symbol_table[i[1]], 5)
        self.outOff('ST', 1, -1, 5)        
        

    def handleAssn(self, i):
        reg = 1
        
        if i[1].isdigit():

            self.outOff('LDC', reg, i[1], 0)
            self.outOff('ST', reg, self.offset, 5)
        else:
            if i[1] == 'true':

                self.outOff('LDC', reg, 1, 0)
                self.outOff('ST', reg, self.offset, 5)    
            elif i[1] == 'false':

                self.outOff('LDC', reg, 0, 0)
                self.outOff('ST', reg, self.offset, 5)
            else:

                total = len(self.symbol_table[self.function])
                for j in range(total - 1):
                    if self.symbol_table[self.function][j][0] == i[1]:
                        self.outOff('LD', reg, -1*(total-j), 5)
                        self.outOff('ST', reg, self.offset, 5)
                        break
        self.new_symbol_table[i[-1]] = self.offset
        self.offset += 1
                

    def handleBoolOp(self, i):
        #implementing short circuit
        
        regToOutput = 3
        self.new_symbol_table[i[-1]] = self.offset

        self.outOff('LD', 1, self.new_symbol_table[i[1]], 5)
        
        if i[0] == 'not':
            self.outOff('JNE', 1, 2, 7)
            self.outOff('LDC', 1, 1, 0)
            self.outOff('LDA', 7, 1, 7)
            self.outOff('LDC', 1, 0, 0)
            
        else:
            self.outOff('LD', 2, self.new_symbol_table[i[2]], 5)
            if i[0] == 'or':    
                self.outOff('JNE', 1, 3, 7)
                self.outOff('JNE', 2, 2, 7)
                self.outOff('LDC', 1, 0, 0)
                self.outOff('LDA', 7, 1, 7)
                self.outOff('LDC', 1, 1, 0)
            
            else:
                self.outClean('MUL', 1, 1, 2)

        self.outOff('ST', 1, self.offset, 5)
        self.offset += 1

    def handleArithOp(self, i):
        regToOutput = 3
        self.new_symbol_table[i[-1]] = self.offset

        self.outOff('LD', 1, self.new_symbol_table[i[1]], 5)
        if i[2] != '':
            self.outOff('LD', 2, self.new_symbol_table[i[2]], 5)
        
        if i[0] == '-':
            if i[2] != '':
                outClean('SUB', 1, 1, 1)
            else:
                self.outClean('SUB', 1, 0, 1)                                  
        elif i[0] == '*':
            self.outClean('MUL', 1, 1, 2)
        elif i[0] == '/':
            self.outClean('DIV', 1, 1, 2)
        else:
            
            self.outClean('ADD', 1, 1, 2)

        self.outOff('ST', 1, self.offset, 5)
        self.offset += 1

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
