"""
    author:      Rishabh dalal, Sai Herng
    description: codegen for print_one.flr
"""

##  1 .. Storing returned value of each fn
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
        self.symbol_table = symbol_table
        self.function_call = caller_called
        self.jumps = []
        self.result = ""
        self.count = 0
        self.initialize()
        
    def generate(self):
        return self.result
    
    def initialize(self):
        #status pointer
        self.comment()
        self.out("LDC", 5,-1, 0)
        #top ptr
        self.out("LDC", 6,2, 0)

        self.prolog('main')
        self.prolog('print')
        self.outClean('HALT', 0,0,0)
        self.jumps[1].append(self.print_ar())
        self.jumps[0].append(self.main_ar())
        
        
        self.handle_jumps()

    def handle_jumps(self):
        self.comment()
        for i in self.jumps:
            val = str(i[0])+ ": LDA 7," + str(i[1]) +"(0)\n"
            self.result += val
        
    def prolog(self, fnName):
        self.comment()
        offset = 0

        for i in range(len(self.symbol_table[fnName]) - 1):
            self.out('ST', 1, offset+1,6)
            offset += 1
            
        self.out('LDA', 1,6, 7) ##store return add
        self.out('ST',  1, offset+1, 6)
        self.out('ST',  5, offset+7, 6)
        self.out('LDA', 5, offset+1, 6)
        self.out('ST',  6, offset+8, 6)
        self.out('LDA',  6, offset+9, 6)
        ##jump
        self.jumps.append([self.count])
        self.count += 1

        
        self.out('LD', 6, 7, 5) ##restore status ptr
        self.out('LD', 5, 6, 5) ##restore top ptr
        if fnName != 'print':
            ##self.out does not have a return
            self.out('LD', 1, 0, 6)
             
    def main_ar(self):
        self.comment()
        jump_to = self.count
        self.comment("*    calling sequence")
                        
        for i in range(5):
            self.out('ST', i, i+1, 5)

        ##return 1
        self.out('LDC', 2, 1, 0)
        self.out('ST', 2, -1, 5)
        
        ##restore registers
        for i in range(5):
            self.out('LD', i, i+1, 5)

        self.out('LD', 7,0,5)
        return jump_to

    def print_ar(self):
        self.comment()
        jump_to = self.count
        
        self.comment("*    calling sequence")
        for i in range(5):
            self.out('ST', i, i+1, 5)

        ##only 1 formal parameter
        self.out('LD', 1, -1, 5)     
        self.comment("*    handle body")
        self.outClean('OUT', 1, 0, 0)

        self.comment("*    return sequence")
        for i in range(5):
            self.out('LD', i, i+1, 5)
        self.out('LD', 7,0,5)
        return jump_to

    def out(self, op, reg1, off, reg2):
        val = str(self.count)+ ": " + op + " " + str(reg1) + ","\
              + str(off) +"(" +str(reg2) + ")\n"
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
