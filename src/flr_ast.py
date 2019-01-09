# root class for all AST nodes

"""
    @author:       Sai Herng, Rishabh Dalal
    @description:  LL1 parser for flair
    
"""


tab = 0
count = 0
toString = []
labelNumber = 0
rememberFlag = False
rememberVal = 'None'

class AST_Node(object):
    pass

class Actuals_Node(AST_Node): 

    def __init__(self):
        self._list = []
        self.name = None
        self.annotated_type = None

    def setType(self, t):
        self.annotated_type = t

    def add(self, formals):
        return self._list.insert(0, formals)

    def addName(self, name):
        self.name = name
            
    def get(self, i):
        return self._list[i]

    def value(self):
        return self._list

    def getName(self):
        return self.name

    def getNumberOfActualParameters(self):
        return len(self._list)

    def __len__(self):

        return len(self._list)

    def __str__(self):
        global tab
        word_str = ""
        tabLast = tab
        tab += 1
        for item in self._list:
            word_str += str(item)

         
        string = "\n" + '  '*tab + "Actuals: "
        tab += 1
        string += "{}".format(self.name)
        tab -= 1
        string += word_str
        tab = tabLast
        return string


    def createIR(self):
        global count
        global toString
        temp_lst = []
        toString.append(["BEGIN_CALL", '', '', ''])
        for j in self._list:
            temp_lst.append(j.createIR())
        for temp in temp_lst:
            toString.append(["PARAM", temp, '', ''])
        toString.append(["CALL", str(self.name.value()), '', ''])
        toString.append(["RECEIVE", ('t' + str(count)), '', ''])
        count += 1
        return 't' + str(count-1)

    

class BinaryExp_Node(AST_Node):
    
    def __init__(self, left, op, right):
        self._left = left
        self._right = right
        self._operator = op
        self.annotated_type = None

    def setType(self, t):
        self.annotated_type = t

##        self._operatorList = ["or", "+", "-",
##                              "and", "*","/",
##                              "<","="        ]
##        self.isvalid()                   
        
    def operator(self):
        return self._operator

    def left(self):
        return self._left

    def right(self):
        return self._right

    def is_valid(self):
        pass

    def __str__(self):
        global tab
        lastTab = tab
        string = '\n' + '  '*tab + str(self._operator) + ' Binary Expr: '
        tab += 1
        string += '\n' + '  '*tab + 'left: {}'.format(self.left())
        string += '\n' + '  '*tab + 'right: {}'.format(self.right())
        tab = lastTab
        return string

    def createIR(self):
        global count
        global toString
        temp1 = self._left.createIR()
        temp2 = self._right.createIR()
        returnVal = [self._operator, temp1, temp2, ("t" + str(count))]
        count += 1
        toString.append(returnVal)
        return "t" + str(count-1)
    
class Body_Node(AST_Node):

    def __init__(self, statement_lst):

        self._statement_list = statement_lst
        self.annotated_type = None

    def setType(self, t):
        self.annotated_type = t

    def value(self):

        return self._statement_list

    def __str__(self):
        global tab
        lastTab = tab
        tab += 1
        string = '\n'+'  '*(tab-1) + 'Body: {}'.format(str(self.value()))
        tab = lastTab
        return string

    def createIR(self):
        self._statement_list.createIR()
        
class Boolean_Node(AST_Node):

    def __init__(self, boolean):
        self._boolean = boolean
        self.annotated_type = None

    def setType(self, t):
        self.annotated_type = t

    def value(self):
        return self._boolean

    def __str__(self):
        global tab
        string = '\n' + '  '*tab + 'Boolean: {}'.format(str(self.value()))
        return string

    def createIR(self):
        global count
        global toString
        msg = ['', str(self._boolean), '', ('t' + str(count))]
        toString.append(msg)
        count += 1
        return "t" + str(count-1)

class Expr_Node(AST_Node):

    def __init__(self, expr):
        self._expr = expr
        self.annotated_type = None

    def setType(self, t):
        self.annotated_type = t
       
    def expr(self):
        return self._expr

    def __str__(self):
        global tab
        lastTab = tab
        tab += 2
        string = '\n' + '  '*(tab-1) + 'Expr Node: {}'.format(str(self.expr()))
        tab = lastTab
        return string

    def createIR(self):
        return self._expr.createIR()

class Definition_List_Node(AST_Node): 

    def __init__(self):
        self._list = []


    def add(self, formals):
        return self._list.insert(0, formals)

            
    def get(self, i):
        return self._list[i]

    def value(self):
        return self._list

    def __len__(self):

        return len(self._list)

    def __str__(self):
        global tab
        word_str = ""
        tabLast = tab
        tab += 1
        for item in self._list:
            word_str += str(item)

        tab = tabLast 
        return "\n" + '  '*tab + "Definitions: " + word_str

    def createIR(self):
        for i in self._list:
            if i != None:
                i.createIR()

class Definition_Node(AST_Node):

    def __init__(self, identifier, formals, TYPE, body):
        self._identifier = identifier
        self._formals = formals
        self._type = TYPE
        self._body = body
        self.annotated_type = None

    def setType(self, t):
        self.annotated_type = t

    def identifier(self):
        return self._identifier

    def formals(self):
        return self._formals

    def type(self):
        return self._type

    def body(self):
        return self._body

    def __str__(self):
        global tab
        lastTab = tab
        string = "\n" + '  '*tab + "Definition:"
        tab += 1
        string += '{}'.format(self.identifier())
        string += '\n' + '  '*tab + '{}'.format(self._formals)
        string += '\n' + '  '*tab + 'Type:{}'.format(self.type())
        string += '\n' + '  '*tab + '{}'.format(self.body())
        tab = lastTab
        return string

    def createIR(self):
        toString.append(['ENTRY', self._identifier.value(), '', ''])
        self._body.createIR()
        toString.append(['EXIT', self._identifier.value(), '', ''])
        

class Formal_Node(AST_Node):
    
    def __init__(self, identifier, TYPE):
        self._identifier = identifier
        self._type = TYPE
        self.annotated_type = None

    def setType(self, t):
        self.annotated_type = t

    def identifier(self):
        return self._identifier

    def type(self):
        return self._type

    def __str__(self):
        global tab
        lastTab = tab
        string ="\n" + '  '*tab + "Formal:"
        tab += 1
        string += '{}'.format(self.identifier())
        string += '\n' + '  '*tab + 'Type:{}'.format(self.type())
        
        tab = lastTab
        return string
    

class Formals_List_Node(AST_Node): 
    
    def __init__(self):
        self._list = []


    def add(self, formals):
        return self._list.insert(0, formals)

            
    def get(self, i):
        return self._list[i]

    def value(self):
        return self._list

    def __len__(self):

        return len(self._list)
    
    def __str__(self):
        global tab
        word_str = ""
        tabLast = tab
        tab += 1
        for item in self._list:
            word_str += str(item)

        tab = tabLast 
        return "\n" + '  '*tab + "Formals: " + word_str

class Identifier_Node(AST_Node):

    def __init__(self, value):
        self._value = value
        self.annotated_type = None

    def setType(self, t):
        self.annotated_type = t

    def value(self):
        return self._value

    def __str__(self):
        return '\n'+'  '*tab +"Identifier_Node: {}".format(self.value())

    def createIR(self):
        global count
        global toString
        returnVal = ['',  str(self._value), '', ("t" + str(count))]
        count += 1
        toString.append(returnVal)
        return "t" + str(count-1)

class If_Node(AST_Node):
    
    def __init__(self, if_cond, then_cond, else_cond):
        self._if = if_cond
        self._then = then_cond
        self._else = else_cond
        self.annotated_type = None
        self.flag = False
        self.rememberVal = None

    def setType(self, t):
        self.annotated_type = t

    def get_if(self):
        return self._if

    def get_then(self):
        return self._then

    def get_else(self):
        return self._else

    def __str__(self):
        global tab
        lastTab = tab
        tab += 1
        string = '\n' + '  '*tab + 'If Node:'
        tab += 1
        string += '\n' + '  '*tab + 'Test: {}'.format(self.get_if())
        string += '\n' + '  '*tab + 'then: {}'.format(self.get_then())
        string += '\n' + '  '*tab + 'else: {}'.format(self.get_else())
        
        tab = lastTab
        return string

    def createIR(self):
        global count
        global toString
        global labelNumber
        global rememberFlag
        
        temp1 = self._if.createIR()
        temp1 = self.oppose()
        toString.append(["if", temp1, "GOTO L" + str(labelNumber)])

        firstLabel = labelNumber
        labelNumber += 1
        self._then.createIR()

        self.handleBaseCase()

        #print("SETTING rememberFlag = True")
        rememberFlag = True
        #print("RF", rememberFlag)

        toString.append(['GOTO', 'L' + str(labelNumber), '', ''])
        lastLabel = labelNumber
        labelNumber += 1

        toString.append(["LABEL", ('L' + str(firstLabel)), '', ''])
        self._else.createIR()

        self.handleBaseCase()
            
        toString.append(['LABEL', 'L'+str(lastLabel), '', ''])
        return str(rememberVal)

    def handleBaseCase(self):
        global rememberFlag
        global rememberVal
        global toString
        
        if rememberFlag:
            #print("INSIDE")
            val = toString.pop()
            if val[-1] == '':
                #print("VAL", val)
                #print(toString)
                toString.append(val)
            else:
                val[-1] = rememberVal
                toString.append(val)
                #print('REMEMBER FLAG = TRUE')
                #print(toString)
        else:
            #print("RV", rememberVal)
            #print(toString)
            rememberVal = toString[-1][-1]
            #print("RV now", rememberVal)
            
            
    def oppose(self):
        global toString
        global count
        
        val = toString.pop()
        flag = False
        
        if val[0] == "<":
            ##comparator
            val[0] = ">="

        else:
            ##Function call / boolean
            count += 1
            newExpr = ['not', val[-1], '', 't'+str(count)]
            flag = True
        toString.append(val)
        if flag:
            toString.append(newExpr)
        return toString[-1][-1]
    
class Number_Node(AST_Node):

    def __init__(self, value):
        self._value = value
        self.annotated_type = None

    def setType(self, t):
        self.annotated_type = t

    def value(self):
        return self._value

    def __str__(self):
        global tab
        string = '\n' + '  '*tab + 'Number: {}'.format(str(self.value()))
        return string

    def createIR(self):
        global count
        global toString
        msg = ['', str(self._value), '', ('t' + str(count))]
        toString.append(msg)
        count += 1
        return "t" + str(count-1)

    
class Negate_Node(AST_Node):

    def __init__(self, value):
        self._value = value
        self.annotated_type = None

    def setType(self, t):
        self.annotated_type = t

    def value(self):
        return self._value

    def __str__(self):
        global tab
        string = '\n' + '  '*tab + 'Negate (not): {}'.format(str(self.value()))
        return string

    def createIR(self):
        global count
        global toString
        temp = self._value.createIR()
        returnVal = ['not', str(temp), '', ('t' + str(count))]
        count += 1
        toString.append(returnVal)
        return "t" + str(count-1)
    
    
class Negative_Node(AST_Node):

    def __init__(self, value):
        self._value = value
        self.annotated_type = None

    def setType(self, t):
        self.annotated_type = t

    def value(self):
        return self._value

    def __str__(self):
        global tab
        string = '\n' + '  '*tab + 'Negative (-): {}'.format(str(self.value()))
        return string

    def createIR(self):
        global count
        global toString
        returnVal = ['-', str(self._value.createIR()), '', ('t' + str(count))]
        count += 1
        toString.append(returnVal)
        return "t" + str(count-1)    
    
class Program_Node(AST_Node):
    
    def __init__(self, identifier, formals, defs, body ):
        self._identifier = identifier
        self._formals = formals
        self._definitions = defs
        self._body = body
        self.annotated_type = None

    def setType(self, t):
        self.annotated_type = t

    def identifier(self):
        return self._identifier

    def formals(self):
        return self._formals

    def definitions(self):
        return self._definitions

    def body(self):
        return self._body

    def __str__(self):
        global tab
        tab = 1
        string = 'Program:'
        string += '{}'.format(self.identifier())
        tab = 1
        string += '{}'.format(self.formals())
        tab = 1
        string += '{}'.format(self.definitions())
        tab = 1
        string += '{}'.format( self.body())   
        return string

    #############NEED TO ASK#####################
    def createIR(self):
        global toString
        self._definitions.createIR()
        toString.append(['ENTRY', self._identifier.value(), '', ''])
        self._body.createIR()
        toString.append(['EXIT', self._identifier.value(), '', ''])
        return toString


class Print_Node(AST_Node):
                
    def __init__(self, expr):
        self._expr = expr
        self.annotated_type = None

    def setType(self, t):
        self.annotated_type = t

    def value(self):
        return self._expr

    def __str__(self):
        global tab
        string = '\n'+'  '*tab + 'Print: {}'.format(str(self.value()))
        return string

    def createIR(self):
        msg = ["PRINT" , self._expr.createIR(), '', '']
        toString.append(msg)

class Return_Node(AST_Node):

    def __init__(self, expr):
        self._expr = expr
        self.annotated_type = None

    def setType(self, t):
        self.annotated_type = t

    def value(self):
        return self._expr

    def __str__(self):
        global tab
        string = '\n'+'  '*tab + 'Return: {}'.format(str(self.value()))
        return string

    def createIR(self):
        global toString
        global rememberFlag
        msg = ["RETURN", self._expr.createIR(), '', '']
        #print("SETTING rememberFlag = False")
        rememberFlag = False
        #print("RF", rememberFlag)
        toString.append(msg)


class Statement_List_Node(AST_Node): 

    def __init__(self):
        self._list = []
        self.annotated_type = None

    def setType(self, t):
        self.annotated_type = t


    def add(self, formals):
        return self._list.insert(0, formals)

            
    def get(self, i):
        return self._list[i]

    def value(self):
        return self._list


    def __len__(self):

        return len(self._list)

    def __str__(self):
        global tab
        word_str = ""
        tabLast = tab
        tab += 1
        for item in self._list:
            word_str += str(item)

        tab = tabLast 
        return "\n" + '  '*tab + "Statement List: " + word_str

    def createIR(self):
        for i in self._list:
            i.createIR()
