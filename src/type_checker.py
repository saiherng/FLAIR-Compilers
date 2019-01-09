from flr_ast      import *
from error   import SemanticError

class TypeChecker:
  'Type-check an AST and construct a symbol table.'

  def __init__(self, ast):
    self._ast = ast
    self.symbol_table = {"print":["Undefined", "Undefined"]}
    self.toDoList = []
    self.patchingUp = False
    self.mainFn = None
    self.called_functions = []
    self.called_identifiers = {}
    self.caller_called = {}
    self.errors = []
    

  def ast(self):
    return self._ast

  def get_symbol_table(self):
    return self.symbol_table

  def function_called(self):
    ##List of info of which functions call which 
    
    return self.caller_called
   
  def type_check(self):
    
    self.symbol_table[self._ast.identifier().value()] = []
    fnName = self._ast.identifier().value()
    self.mainFn = fnName
    for i in self._ast.formals().value():

      self.type_formal(i, fnName)
    #print("Done parsing all the formals of main function")

    self.symbol_table[fnName].append(None)
    for i in self._ast.definitions().value():
      self.type_definition(i)
    #print("Done parsing all the definitions")

    self.patchUp()
    self.symbol_table[fnName][-1] = self.type_body(self._ast.body(), fnName)
    #self.postprocess()
    
    #print(self.called_identifiers)
    self._ast.setType(self.symbol_table[fnName][-1])
    return self.errors
      
  ##----------------------------------------------------------------------
  
  def type_formal(self, ast, fnName):
    if ast != None:
      formal = (ast.identifier().value(), ast.type())

      if formal in self.symbol_table[fnName]:
        msg = "Identifier '" + str(formal[0]) + "' declared twice in defintions " + \
              "declaration of '" + fnName + "'"
        self.errors.append(msg)
        #raise SemanticError() 
      
      self.symbol_table[fnName].append(formal)
      
    
  def type_definition(self, ast):
    if ast != None:

      functionName = ast.identifier().value()
      if functionName in self.symbol_table and not self.patchingUp:
        msg = "User tried to define function '" + functionName + "' twice"
        self.errors.append(msg)
        #raise SemanticError(msg)
      self.symbol_table[functionName] = []

      for k in ast.formals().value():
        self.type_formal(k, functionName)

      self.symbol_table[functionName].append(ast.type())
      bodyType = self.type_body(ast.body(), functionName)
      
      if bodyType == 0:
        self.toDoList.append(ast)
      else:

        if ast.type() != bodyType:
          msg = "Return type of function '" + functionName + \
                "' is not matching to declared return type"
          self.errors.append(msg)
          #raise SemanticError(msg)
      ast.setType(bodyType)
      #print("---------------1 def done-------------------------")

  def type_body(self, ast, fnName):

    for j in ast.value().value():
      expr = j.value().expr()
      if isinstance(j, Print_Node):
        if fnName in self.caller_called:
          self.caller_called[fnName].add('print')
        else:
          self.caller_called[fnName] = set()
          self.caller_called[fnName].add('print')
        typ = self.type_expr(expr, fnName)
        j.setType(typ)                  ##type of print node
        
      else:
        typ = self.type_expr(expr, fnName)
        ast.setType(typ)                 ##type of body
        ast.value().setType(typ)         ##type of statement list
        j.setType(typ)                   ##type of return node
        return typ

  def type_expr(self, ast, fnName):
    val = ast
    while isinstance(val, Expr_Node):
      val = val.expr()
    
    if isinstance(val, BinaryExp_Node):
      typ = self.type_binaryExpr(val, fnName)
      ast.setType(typ)
      val.setType(typ) ##might be redundant, might not be!
      return typ
    
    elif isinstance(val, Boolean_Node):
      typ = self.type_booleanNode(val, fnName)
      ast.setType(typ)
      val.setType(typ)
      return typ

    elif isinstance(val, Identifier_Node):
      typ = self.type_IdentifierNode(val, fnName)
      ast.setType(typ)
      val.setType(typ)
      return typ
    
    elif isinstance(val, If_Node):
      typ = self.type_ifNode(val, fnName)
      ast.setType(typ)
      val.setType(typ)
      return typ
    
    elif isinstance(val, Number_Node):
      typ = self.type_numberNode(val, fnName)
      ast.setType(typ)
      val.setType(typ)
      return typ
    
    elif isinstance(val, Negate_Node):
      typ = self.type_negateNode(val, fnName)
      ast.setType(typ)
      val.setType(typ)
      return typ
    
    elif isinstance(val, Negative_Node):
      typ = self.type_negativeNode(val, fnName)
      ast.setType(typ)
      val.setType(typ)
      return typ
    
##    elif isinstance(val, NestedExpr_Node):
##      typ =  self.type_nestedNode(val, fnName)
##      ast.setType(typ)
##      val.setType(typ)
##      return typ
    
    elif isinstance(val, Actuals_Node):
      typ = self.type_actualsNode(val, fnName)
      ast.setType(typ)
      val.setType(typ)
      return typ
    
    else:
      print("VAL", val, type(val))
      msg = "Something somewhere went wrong."
      raise SemanticError(msg)


  def type_binaryExpr(self, ast, fnName):

    type1 = self.type_expr(ast.left(), fnName)
    ast.left().setType(type1)
    type2 = self.type_expr(ast.right(), fnName)
    ast.right().setType(type2)
    
    if type1 == 0 or type2 == 0:
      return 0
    if ast.operator() in ['and', 'or']:
      if type1 == type2 == 'boolean':
        return 'boolean'
      msg = "Expected two booleans in the binary expr " + \
            str(ast.left()) + "\nOperator : " + str(ast.operator()) + " " + str(ast.right())
      self.errors.append(msg)
      #raise SemanticError(msg)
    else:

      if type1 == type2 == 'integer':
        if ast.operator() in "+-*/":
          return 'integer'
        else:
          return 'boolean'
      msg = "Expected two integers in the binary expr " + \
            str(ast.left()) + " \nOperator : " + str(ast.operator()) + " " + str(ast.right())
      self.errors.append(msg)
      #raise SemanticError(msg)

  def type_booleanNode(self, ast, fnName):
    ast.setType('boolean')
    return 'boolean'

  def type_IdentifierNode(self, ast, fnName):

    for i in self.symbol_table[fnName]:
      if isinstance(i, tuple):
        if i[0] == ast.value():
          if fnName in self.called_identifiers:
            self.called_identifiers[fnName].add(ast.value())
          else:
            self.called_identifiers[fnName] = set()
            self.called_identifiers[fnName].add(ast.value())
          ast.setType(i[1])
          return i[1]
    msg = "'" + str(ast.value()) + "' identifier not declared in the defintion of '" + fnName + "'"
    self.errors.append(msg)
    #raise SemanticError(msg)

  def type_ifNode(self, ast, fnName):

    condType = self.type_expr(ast.get_if(), fnName)
    ast.get_if().setType(condType)
    
    if condType != 'boolean':
      if condType == 0:
        return 0
      else:
        msg = "Expected a boolean value for the test of if statement at " + str(ast.get_if())
        self.errors.append(msg)
        #raise SemanticError(msg)

    thenType = self.type_expr(ast.get_then(), fnName)
    ast.get_then().setType(thenType)
    elseType = self.type_expr(ast.get_else(), fnName)
    ast.get_else().setType(elseType)
    
    if thenType == 0 or elseType == 0:
      return 0
    if thenType != elseType:
      msg = "Inconsistant return types of then and else in the if statement " + \
            str(ast.get_if()) + " " + str(ast.get_then()) + " " + str(ast.get_else())
      self.errors.append(msg)
      #raise SemanticError()
    return thenType

  def type_numberNode(self, ast, fnName):
    ast.setType('integer')
    return 'integer'

  def type_negateNode(self, ast, fnName):
    expr_type = self.type_expr(ast.value(), fnName)
    ast.value().setType(expr_type)
    
    if expr_type != 'boolean':
      if expr_type == 0:
        return 0
      msg = "Expected a boolean for negating: " + str(ast.value())
      self.errors.append(msg)
      #raise SemanticError("Expected a boolean at", ast.value())
    ast.setType('boolean')
    return 'boolean'

  def type_negativeNode(self, ast, fnName):
    expr_type = self.type_expr(ast.value(), fnName)
    ast.value().setType(expr_type)
    
    if expr_type != 'integer':
      if expr_type == 0:
        return 0
      msg = "Expected an integer to negate instead of: " + str(ast.value())
      self.errors.append(msg)
      #raise SemanticError()
    ast.setType('integer')
    return 'integer'

  def type_actualsNode(self, ast, fnName):  

    calledfnName = ast.getName().value()
    if calledfnName != fnName:
      self.called_functions.append(calledfnName)

    if fnName in self.caller_called:
      self.caller_called[fnName].add(calledfnName)
    else:
      self.caller_called[fnName] = set()
      self.caller_called[fnName].add(calledfnName)

    if calledfnName in self.symbol_table:
      length = len(self.symbol_table[calledfnName]) - 1

      if ast.getNumberOfActualParameters() != length:
        msg = "Wrong number of arguments sent to function call of '" + fnName + "'"
        self.errors.append(msg)
        #raise SemanticError(msg)
      paraList = ast.value()

      for j in range(len(paraList)):
        if isinstance(paraList[j], Expr_Node):
          send = paraList[j].expr()
        else:
          send = paraList[j]
        leftHand = self.type_expr(send, fnName)
        if leftHand == 0:
          return 0
        if leftHand != self.symbol_table[calledfnName][j][1]:
          msg = "The type of '" + self.symbol_table[calledfnName][j][0] + \
                "' does not match the expected type: '" + self.type_expr(paraList[j], fnName) + "'"
          self.errors.append(msg)
          #raise SemanticError(msg)

      ast.setType(self.symbol_table[calledfnName][-1])
      return self.symbol_table[calledfnName][-1]
    else:
      if self.patchingUp:
        msg = "The function '" + calledfnName + "' is not defined"
        self.errors.append(msg)
        #raise SemanticError(msg)

      return 0

  def patchUp(self):
    self.patchingUp = True
    for i in self.toDoList:
      self.type_definition(i)


  def postprocess(self):
    for i in self.symbol_table.keys():
      if not i in self.called_functions and i != 'print' and i != self.mainFn:
        print("**Warning** Function" + ' "' + i + '" ' "is defined but never",
              "called (not including recusive calls to itself)")

    for j in self.symbol_table.keys():
      if j != 'print':
        for k in self.symbol_table[j][:-1]:
          if j in self.called_identifiers:
            if not k[0] in self.called_identifiers[j]:
              print("**Warning** Identifier" + ' "' + k[0] + \
                    '" ' "is a formal parameter of function", '"' + j + '" ' + \
                    "but never used")

  def pretty_print(self):
    if len(self.errors) > 0:
      print("Errors:")
      print("====================================")
      f = True
      for i in self.errors:
          f = False
          print(i)
          print("\n-------------------------------------")
      if f:
          print("None\n")

    else:
      #t = self.symbol_table()
      #t2 = self.caller_called()

      string = "<< Symbol Table >>\n\n"

      for i in self.symbol_table.keys():
          string += "Function >> " + i
          string += "\nFormal Parameters >> "
          flag = True
          for k in self.symbol_table[i][:-1]:
              flag = False
              string += k[0] + " : " + k[1] + " , "
          if not flag:
              string = string[:-2] + '\n'
          else:
              string += 'None\n'
          string += "Return type >> " + str(self.symbol_table[i][-1]) + '\n'

          string += "Functions called >> "
          
          if i in self.caller_called.keys():
              flag2 = True
              for j in self.caller_called[i]:
                  flag = False
                  string += j + " , "
              if not flag:
                  string = string[:-2] + "\n\n"
              else:
                  string += "None\n\n"
          else:
              string += "None\n\n"
          
      print(string)
      print()
      self.postprocess()
    
