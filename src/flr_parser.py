"""
    @author:       Sai Herng, Rishabh Dalal
    @description:  LL1 parser for flair
    @since:        11 Oct. 2018

"""
from scanner import Scanner
from flr_token import Token, TokenType
import os
from enum import Enum
from error import ParseError, LexicalError
from flr_ast import *
from flr_stack import Stack

class NonTerminal(Enum):
    PROGRAM              =  0
    DEFINITIONS          =  1
    DEF                  =  2
    FORMALS              =  3
    NONEMPTYFORMALS      =  4
    NONEMPTY_F_REST      =  5
    FORMAL               =  6
    BODY                 =  7
    STATEMENT_LIST       =  8
    TYPE                 =  9
    EXPR                 =  10
    E_TAIL               =  11
    SIMPLE_EXPR          =  12
    SE_TAIL              =  13
    TERM                 =  14
    T_TAIL               =  15
    FACTOR               =  16
    ID                   =  17
    ID_REST              =  18
    ACTUALS              =  19
    NONEMPTYACTUALS      =  20
    NONEMPTY_A_REST      =  21
    LITERAL              =  22
    PRINT_STATEMENT      =  23

class AstAction(Enum):

    MakeProgram         = 0
    MakeDefs            = 1
    MakeDef             = 2
    MakeFormalsList     = 3
    MakeBody            = 4
    MakeFormal          = 5
    MakeLessExp         = 6    
    MakeEqExp           = 7
    MakeOrExp           = 8
    MakePlusExp         = 9
    MakeMinusExp        = 10
    MakeAndExp          = 11
    MakeTimesExp        = 12
    MakeDivideExp       = 13    
    MakeIfExp           = 14    
    MakeNegate          = 15
    MakeNegative        = 16    
    MakeIdentifier      = 17   
    MakeNumber          = 19
    MakeBoolean         = 20
    MakePrint           = 21
    MakeExpr            = 22
    MakeExprList        = 23    
    MakeStatementList   = 24
    MakeReturn          = 25
    MakeAddExp          = 26
    #MakeType            = 27
    MakeDefList         = 28
    MakeActualsList     = 31
    MakeActuals         = 34
    
    

def make_program(ast_stack):

    body = ast_stack.pop()
    defs = ast_stack.pop()
    formals_list = ast_stack.pop()
    idn = ast_stack.pop()
    ast_stack.pushProper(Program_Node(idn, formals_list, defs, body))


def make_formals_list(ast_stack):
  
    list_of_assignments = Formals_List_Node()
    while isinstance(ast_stack.top(), Formal_Node):
        list_of_assignments.add(ast_stack.pop())

    if len(list_of_assignments) == 0:
        list_of_assignments.add(None)       
    ast_stack.pushProper(list_of_assignments)

def make_statement_list(ast_stack):

    list_of_assignments = Statement_List_Node()
    while isinstance(ast_stack.top(), Return_Node) \
          or isinstance(ast_stack.top(), Print_Node):
        list_of_assignments.add(ast_stack.pop())
    if len(list_of_assignments) == 0:
        list_of_assignments.add(None)
    ast_stack.pushProper(list_of_assignments)
           
def make_def(ast_stack):
    if isinstance(ast_stack.top(), Body_Node):
        body = ast_stack.pop()
    else:
        body = Body_Node(None)

    if isinstance(ast_stack.top(), str):
        tp = ast_stack.pop()
    else:
        tp = None

    if isinstance(ast_stack.top(), Formals_List_Node):
        formals_list = ast_stack.pop()
    else:
        formals_list = Formals_List_Node().add(None)

    if isinstance(ast_stack.top(), Identifier_Node):
        idn = ast_stack.pop()
    else:
        idn = Identifier_Node(None)
        
    ast_stack.pushProper(Definition_Node(idn,formals_list, tp, body))
                                         

def make_body(ast_stack):
    if isinstance(ast_stack.top(), Statement_List_Node):
        value = ast_stack.pop()
    else:
        value = Statement_List_Node().add(None)

    ast_stack.pushProper(Body_Node(value))
    

def make_formal(ast_stack):
    if isinstance(ast_stack.top(), str):
        tp = ast_stack.pop()
    else:
        tp = None

    if isinstance(ast_stack.top(), Identifier_Node):
        idn = ast_stack.pop()
    else:
        idn = Identifier_Node(None)
    
    ast_stack.pushProper(Formal_Node(idn, tp))
    
def make_less_exp(ast_stack):
    right = ast_stack.pop()
    left = ast_stack.pop()   
    ast_stack.pushProper(BinaryExp_Node(left,"<", right))

def make_eq_exp(ast_stack):
    
    right = ast_stack.pop()
    left = ast_stack.pop()
    ast_stack.pushProper(BinaryExp_Node(left,"=", right))

def make_or_exp(ast_stack):
    
    right = ast_stack.pop()
    left = ast_stack.pop()
    ast_stack.pushProper(BinaryExp_Node(left,"or", right))

def make_plus_exp(ast_stack):
    right = ast_stack.pop()    
    left = ast_stack.pop()
    ast_stack.pushProper(BinaryExp_Node(left,"+", right))

def make_minus_exp(ast_stack):
    
    right = ast_stack.pop()
    left = ast_stack.pop()   
    ast_stack.pushProper(BinaryExp_Node(left,"-", right))

def make_and_exp(ast_stack):
    
    left = ast_stack.pop()
    right = ast_stack.pop()
    ast_stack.pushProper(BinaryExp_Node(left,"and", right))

def make_times_exp(ast_stack):
    
    right = ast_stack.pop()
    left = ast_stack.pop()    
    ast_stack.pushProper(BinaryExp_Node(left,"*", right))

def make_divide_exp(ast_stack):
    
    right = ast_stack.pop()
    left = ast_stack.pop()   
    ast_stack.pushProper(BinaryExp_Node(left,"/", right))

def make_if_exp(ast_stack):
    else_cond = ast_stack.pop()
    then_cond = ast_stack.pop()
    if_cond = ast_stack.pop()
    ast_stack.pushProper(If_Node(if_cond, then_cond, else_cond))

def make_negate(ast_stack):
    value = ast_stack.pop()   
    ast_stack.pushProper(Negate_Node(value))

def make_negative(ast_stack):
    value = ast_stack.pop()   
    ast_stack.pushProper(Negative_Node(value))

def make_identifier(ast_stack):
    value = ast_stack.pop()   
    ast_stack.pushProper(Identifier_Node(value))

def make_number(ast_stack):
    value = ast_stack.pop()   
    ast_stack.pushProper(Number_Node(value))

def make_boolean(ast_stack):
    value = ast_stack.pop()   
    ast_stack.pushProper(Boolean_Node(value))

def make_print(ast_stack):
    value = ast_stack.pop()   
    ast_stack.pushProper(Print_Node(value))

def make_exp(ast_stack):
    
    value = ast_stack.pop()
    ast_stack.pushProper(Expr_Node(value))

##def make_expr_list(ast_stack):
##
##    list_of_assignments = Expr_List_Node()
##    while isinstance(ast_stack.top(), Expr_Node):
##        val = ast_stack.pop()
##        list_of_assignments.add(val)
##
##    if len(list_of_assignments) == 0:
##        list_of_assignments.add(None)
##    
##    ast_stack.pushProper(list_of_assignments)
    

def make_def_list(ast_stack):

    list_of_assignments = Definition_List_Node()    
    while isinstance(ast_stack.top(), Definition_Node):
        val = ast_stack.pop()
        list_of_assignments.add(val)
    if len(list_of_assignments) == 0:
        list_of_assignments.add(None)
    ast_stack.pushProper(list_of_assignments)

    
def make_actuals_list(ast_stack):

    list_of_assignments = Actuals_List_Node()
    
    while isinstance(ast_stack.top(), Expr_Node):
        val = ast_stack.pop()
        list_of_assignments.add(val)
        
    if len(list_of_assignments) == 0:
        list_of_assignments.add(None)
        
    ast_stack.pushProper(list_of_assignments)
    

def make_return(ast_stack):
    
    value = ast_stack.pop()   
    ast_stack.pushProper(Return_Node(value))

def make_actuals(ast_stack):
    node = Actuals_Node()
    #print("TOP::", ast_stack.top())
    while isinstance(ast_stack.top(), Expr_Node):
        node.add(ast_stack.pop())
    
    node.addName(ast_stack.pop())
    ast_stack.pushProper(node)


class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.parse_stack = Stack()
        self.semantic_stack = Stack()
        self.last = None
        self.parseTable = {
            ( NonTerminal.PROGRAM , TokenType.PROGRAM ) : [TokenType.PROGRAM,TokenType.IDENTIFIER,AstAction.MakeIdentifier,TokenType.LEFT_PAREN,
                                                           NonTerminal.FORMALS,TokenType.RIGHT_PAREN, AstAction.MakeFormalsList,
                                                           TokenType.SEMI_COLON,NonTerminal.DEFINITIONS, AstAction.MakeDefList, NonTerminal.BODY,TokenType.PERIOD, AstAction.MakeProgram],
            ( NonTerminal.DEFINITIONS  , TokenType.FUNCTION ) : [NonTerminal.DEF, NonTerminal.DEFINITIONS ],
            ( NonTerminal.DEFINITIONS  , TokenType.BEGIN ) : ["epsilon"],
            ( NonTerminal.DEF , TokenType.FUNCTION ) : [TokenType.FUNCTION,TokenType.IDENTIFIER,AstAction.MakeIdentifier,TokenType.LEFT_PAREN,NonTerminal.FORMALS,TokenType.RIGHT_PAREN,AstAction.MakeFormalsList,TokenType.COLON,NonTerminal.TYPE
                                                        ,NonTerminal.BODY,TokenType.SEMI_COLON, AstAction.MakeDef],
            ( NonTerminal.FORMALS , TokenType.RIGHT_PAREN ) : ["epsilon"],
            ( NonTerminal.FORMALS , TokenType.IDENTIFIER ) : [NonTerminal.NONEMPTYFORMALS],
            ( NonTerminal.NONEMPTYFORMALS , TokenType.IDENTIFIER ) : [NonTerminal.FORMAL,NonTerminal.NONEMPTY_F_REST],
            ( NonTerminal.NONEMPTY_F_REST , TokenType.RIGHT_PAREN ) : ["epsilon"],
            ( NonTerminal.NONEMPTY_F_REST , TokenType.COMMA ) : [TokenType.COMMA,NonTerminal.FORMAL,NonTerminal.NONEMPTY_F_REST],
            ( NonTerminal.FORMAL , TokenType.IDENTIFIER ) : [TokenType.IDENTIFIER,AstAction.MakeIdentifier,TokenType.COLON,NonTerminal.TYPE, AstAction.MakeFormal],
            ( NonTerminal.BODY , TokenType.BEGIN ) : [TokenType.BEGIN,NonTerminal.STATEMENT_LIST, AstAction.MakeStatementList,TokenType.END, AstAction.MakeBody],
            ( NonTerminal.STATEMENT_LIST , TokenType.RETURN ) : [TokenType.RETURN,NonTerminal.EXPR, AstAction.MakeReturn],
            ( NonTerminal.STATEMENT_LIST , TokenType.PRINT ) : [NonTerminal.PRINT_STATEMENT,NonTerminal.STATEMENT_LIST],
            ( NonTerminal.TYPE , TokenType.INTEGER ) : [TokenType.INTEGER],
            ( NonTerminal.TYPE , TokenType.BOOLEANLITERAL ) : [TokenType.BOOLEANLITERAL],
            ( NonTerminal.EXPR , TokenType.LEFT_PAREN ) : [NonTerminal.SIMPLE_EXPR,NonTerminal.E_TAIL, AstAction.MakeExpr],
            ( NonTerminal.EXPR , TokenType.IDENTIFIER ) : [NonTerminal.SIMPLE_EXPR,NonTerminal.E_TAIL, AstAction.MakeExpr],
            ( NonTerminal.EXPR , TokenType.NUMBER ) : [NonTerminal.SIMPLE_EXPR,NonTerminal.E_TAIL, AstAction.MakeExpr],
            ( NonTerminal.EXPR , TokenType.TRUE ) : [NonTerminal.SIMPLE_EXPR,NonTerminal.E_TAIL, AstAction.MakeExpr],
            ( NonTerminal.EXPR , TokenType.FALSE ) : [NonTerminal.SIMPLE_EXPR,NonTerminal.E_TAIL, AstAction.MakeExpr],
            ( NonTerminal.EXPR , TokenType.NOT ) : [NonTerminal.SIMPLE_EXPR,NonTerminal.E_TAIL, AstAction.MakeExpr],
            ( NonTerminal.EXPR , TokenType.IF ) : [NonTerminal.SIMPLE_EXPR,NonTerminal.E_TAIL, AstAction.MakeExpr],
            ( NonTerminal.EXPR , TokenType.SUBTRACT ) : [NonTerminal.SIMPLE_EXPR,NonTerminal.E_TAIL, AstAction.MakeExpr],
            ( NonTerminal.E_TAIL , TokenType.RIGHT_PAREN ) : ["epsilon"],
            ( NonTerminal.E_TAIL , TokenType.EQUAL ) : [TokenType.EQUAL,NonTerminal.SIMPLE_EXPR, AstAction.MakeEqExp, NonTerminal.E_TAIL],
            ( NonTerminal.E_TAIL , TokenType.LESSTHAN ) : [TokenType.LESSTHAN, NonTerminal.SIMPLE_EXPR, AstAction.MakeLessExp, NonTerminal.E_TAIL],
            ( NonTerminal.E_TAIL , TokenType.MULTIPLY ) : ["epsilon"],
            ( NonTerminal.E_TAIL , TokenType.DIVIDE ) : ["epsilon"],
            ( NonTerminal.E_TAIL , TokenType.ADD ) : ["epsilon"],
            ( NonTerminal.E_TAIL , TokenType.ELSE ) : ["epsilon"],
            ( NonTerminal.E_TAIL , TokenType.THEN ) : ["epsilon"],
            ( NonTerminal.E_TAIL , TokenType.AND ) : ["epsilon"],
            ( NonTerminal.E_TAIL , TokenType.END ) : ["epsilon"],
            ( NonTerminal.E_TAIL , TokenType.SUBTRACT ) : ["epsilon"],
            ( NonTerminal.E_TAIL , TokenType.OR ) : ["epsilon"],
            ( NonTerminal.E_TAIL , TokenType.COMMA ) : ["epsilon"],
            ( NonTerminal.SIMPLE_EXPR , TokenType.LEFT_PAREN ) : [NonTerminal.TERM,NonTerminal.SE_TAIL],
            ( NonTerminal.SIMPLE_EXPR , TokenType.IDENTIFIER ) : [NonTerminal.TERM,NonTerminal.SE_TAIL],
            ( NonTerminal.SIMPLE_EXPR , TokenType.NUMBER ) : [NonTerminal.TERM,NonTerminal.SE_TAIL],
            ( NonTerminal.SIMPLE_EXPR , TokenType.TRUE ) : [NonTerminal.TERM,NonTerminal.SE_TAIL],
            ( NonTerminal.SIMPLE_EXPR , TokenType.FALSE ) : [NonTerminal.TERM,NonTerminal.SE_TAIL],
            ( NonTerminal.SIMPLE_EXPR , TokenType.NOT ) : [NonTerminal.TERM,NonTerminal.SE_TAIL],
            ( NonTerminal.SIMPLE_EXPR , TokenType.IF ) : [NonTerminal.TERM,NonTerminal.SE_TAIL],
            ( NonTerminal.SIMPLE_EXPR , TokenType.SUBTRACT ) : [NonTerminal.TERM,NonTerminal.SE_TAIL],
            ( NonTerminal.SE_TAIL , TokenType.RIGHT_PAREN ) : ["epsilon"],
            ( NonTerminal.SE_TAIL , TokenType.EQUAL ) : ["epsilon"],
            ( NonTerminal.SE_TAIL , TokenType.LESSTHAN ) : ["epsilon"],
            ( NonTerminal.SE_TAIL , TokenType.MULTIPLY ) : ["epsilon"],
            ( NonTerminal.SE_TAIL , TokenType.DIVIDE ) : ["epsilon"],
            ( NonTerminal.SE_TAIL , TokenType.ADD ) : [TokenType.ADD,NonTerminal.TERM, AstAction.MakeAddExp, NonTerminal.SE_TAIL],
            ( NonTerminal.SE_TAIL , TokenType.ELSE ) : ["epsilon"],
            ( NonTerminal.SE_TAIL , TokenType.THEN ) : ["epsilon"],
            ( NonTerminal.SE_TAIL , TokenType.AND ) : ["epsilon"],
            ( NonTerminal.SE_TAIL , TokenType.END ) : ["epsilon"],
            ( NonTerminal.SE_TAIL , TokenType.SUBTRACT ) : [TokenType.SUBTRACT,NonTerminal.TERM, AstAction.MakeMinusExp, NonTerminal.SE_TAIL],
            ( NonTerminal.SE_TAIL , TokenType.OR ) : [TokenType.OR, NonTerminal.TERM, AstAction.MakeOrExp, NonTerminal.SE_TAIL],
            ( NonTerminal.SE_TAIL , TokenType.COMMA ) : ["epsilon"],
            ( NonTerminal.TERM , TokenType.LEFT_PAREN ) : [NonTerminal.FACTOR,NonTerminal.T_TAIL],
            ( NonTerminal.TERM , TokenType.IDENTIFIER ) : [NonTerminal.FACTOR,NonTerminal.T_TAIL],
            ( NonTerminal.TERM , TokenType.NUMBER ) : [NonTerminal.FACTOR,NonTerminal.T_TAIL],
            ( NonTerminal.TERM , TokenType.TRUE ) : [NonTerminal.FACTOR,NonTerminal.T_TAIL],
            ( NonTerminal.TERM , TokenType.FALSE ) : [NonTerminal.FACTOR,NonTerminal.T_TAIL],
            ( NonTerminal.TERM , TokenType.NOT ) : [NonTerminal.FACTOR,NonTerminal.T_TAIL],
            ( NonTerminal.TERM , TokenType.IF ) : [NonTerminal.FACTOR,NonTerminal.T_TAIL],
            ( NonTerminal.TERM , TokenType.SUBTRACT ) : [NonTerminal.FACTOR,NonTerminal.T_TAIL],
            ( NonTerminal.T_TAIL , TokenType.RIGHT_PAREN ) : ["epsilon"],
            ( NonTerminal.T_TAIL , TokenType.EQUAL ) : ["epsilon"],
            ( NonTerminal.T_TAIL , TokenType.OR ) : ["epsilon"],
            ( NonTerminal.T_TAIL , TokenType.LESSTHAN ) : ["epsilon"],
            ( NonTerminal.T_TAIL , TokenType.MULTIPLY ) : [TokenType.MULTIPLY,NonTerminal.FACTOR, AstAction.MakeTimesExp, NonTerminal.T_TAIL],
            ( NonTerminal.T_TAIL , TokenType.DIVIDE ) : [TokenType.DIVIDE,NonTerminal.FACTOR, AstAction.MakeDivideExp, NonTerminal.T_TAIL],
            ( NonTerminal.T_TAIL , TokenType.ADD ) : ["epsilon"],
            ( NonTerminal.T_TAIL , TokenType.ELSE ) : ["epsilon"],
            ( NonTerminal.T_TAIL , TokenType.THEN ) : ["epsilon"],
            ( NonTerminal.T_TAIL , TokenType.AND ) : [TokenType.AND,NonTerminal.FACTOR, AstAction.MakeAndExp, NonTerminal.T_TAIL],
            ( NonTerminal.T_TAIL , TokenType.END ) : ["epsilon"],
            ( NonTerminal.T_TAIL , TokenType.SUBTRACT ) : ["epsilon"],
            ( NonTerminal.T_TAIL , TokenType.COMMA ) : ["epsilon"],
            ###( NonTerminal.FACTOR , TokenType.LEFT_PAREN ) : [TokenType.LEFT_PAREN,NonTerminal.EXPR,TokenType.RIGHT_PAREN, AstAction.MakeNestedExpr],
            ( NonTerminal.FACTOR , TokenType.LEFT_PAREN ) : [TokenType.LEFT_PAREN,NonTerminal.EXPR,TokenType.RIGHT_PAREN, AstAction.MakeExpr],
            ( NonTerminal.FACTOR , TokenType.IDENTIFIER ) : [NonTerminal.ID],
            ( NonTerminal.FACTOR , TokenType.NUMBER ) : [NonTerminal.LITERAL],
            ( NonTerminal.FACTOR , TokenType.TRUE ) : [NonTerminal.LITERAL],
            ( NonTerminal.FACTOR , TokenType.FALSE ) : [NonTerminal.LITERAL],
            ( NonTerminal.FACTOR , TokenType.NOT ) : [TokenType.NOT,NonTerminal.FACTOR, AstAction.MakeNegate],
            ( NonTerminal.FACTOR , TokenType.IF ) : [TokenType.IF,NonTerminal.EXPR,TokenType.THEN,NonTerminal.EXPR,TokenType.ELSE,NonTerminal.EXPR, AstAction.MakeIfExp],
            ( NonTerminal.FACTOR , TokenType.SUBTRACT ) : [TokenType.SUBTRACT,NonTerminal.FACTOR, AstAction.MakeNegative],
            ( NonTerminal.ID , TokenType.IDENTIFIER ) : [TokenType.IDENTIFIER,AstAction.MakeIdentifier,NonTerminal.ID_REST],
            ( NonTerminal.ID_REST , TokenType.LEFT_PAREN ) : [TokenType.LEFT_PAREN,NonTerminal.ACTUALS,TokenType.RIGHT_PAREN, AstAction.MakeActuals],
            ( NonTerminal.ID_REST , TokenType.RIGHT_PAREN ) : ["epsilon"],
            ( NonTerminal.ID_REST , TokenType.EQUAL ) : ["epsilon"],
            ( NonTerminal.ID_REST , TokenType.LESSTHAN ) : ["epsilon"],
            ( NonTerminal.ID_REST , TokenType.MULTIPLY ) : ["epsilon"],
            ( NonTerminal.ID_REST , TokenType.DIVIDE ) : ["epsilon"],
            ( NonTerminal.ID_REST , TokenType.ADD ) : ["epsilon"],
            ( NonTerminal.ID_REST , TokenType.ELSE ) : ["epsilon"],
            ( NonTerminal.ID_REST , TokenType.THEN ) : ["epsilon"],
            ( NonTerminal.ID_REST , TokenType.END ) : ["epsilon"],
            ( NonTerminal.ID_REST , TokenType.SUBTRACT ) : ["epsilon"],
            ( NonTerminal.ID_REST , TokenType.OR ) : ["epsilon"],
            ( NonTerminal.ID_REST , TokenType.COMMA ) : ["epsilon"],
            ( NonTerminal.ACTUALS , TokenType.LEFT_PAREN ) : [NonTerminal.NONEMPTYACTUALS],
            ( NonTerminal.ACTUALS , TokenType.RIGHT_PAREN ) : ["epsilon"],
            ( NonTerminal.ACTUALS , TokenType.IDENTIFIER ) : [NonTerminal.NONEMPTYACTUALS],
            ( NonTerminal.ACTUALS , TokenType.NUMBER ) : [NonTerminal.NONEMPTYACTUALS],
            ( NonTerminal.ACTUALS , TokenType.TRUE ) : [NonTerminal.NONEMPTYACTUALS],
            ( NonTerminal.ACTUALS , TokenType.FALSE ) : [NonTerminal.NONEMPTYACTUALS],
            ( NonTerminal.ACTUALS , TokenType.NOT ) : [NonTerminal.NONEMPTYACTUALS],
            ( NonTerminal.ACTUALS , TokenType.IF ) : [NonTerminal.NONEMPTYACTUALS],
            ( NonTerminal.ACTUALS , TokenType.SUBTRACT ) : [NonTerminal.NONEMPTYACTUALS],
            ( NonTerminal.NONEMPTYACTUALS , TokenType.LEFT_PAREN ) : [NonTerminal.EXPR,NonTerminal.NONEMPTY_A_REST],
            ( NonTerminal.NONEMPTYACTUALS , TokenType.IDENTIFIER ) : [NonTerminal.EXPR,NonTerminal.NONEMPTY_A_REST],
            ( NonTerminal.NONEMPTYACTUALS , TokenType.NUMBER ) : [NonTerminal.EXPR,NonTerminal.NONEMPTY_A_REST],
            ( NonTerminal.NONEMPTYACTUALS , TokenType.TRUE ) : [NonTerminal.EXPR,NonTerminal.NONEMPTY_A_REST],
            ( NonTerminal.NONEMPTYACTUALS , TokenType.FALSE ) : [NonTerminal.EXPR,NonTerminal.NONEMPTY_A_REST],
            ( NonTerminal.NONEMPTYACTUALS , TokenType.NOT ) : [NonTerminal.EXPR,NonTerminal.NONEMPTY_A_REST],
            ( NonTerminal.NONEMPTYACTUALS , TokenType.IF ) : [NonTerminal.EXPR,NonTerminal.NONEMPTY_A_REST],
            ( NonTerminal.NONEMPTYACTUALS , TokenType.SUBTRACT ) : [NonTerminal.EXPR,NonTerminal.NONEMPTY_A_REST],
            ( NonTerminal.NONEMPTY_A_REST , TokenType.RIGHT_PAREN ) : ["epsilon"],
            ( NonTerminal.NONEMPTY_A_REST , TokenType.COMMA ) : [TokenType.COMMA,NonTerminal.NONEMPTYACTUALS],
            ( NonTerminal.LITERAL , TokenType.NUMBER ) : [TokenType.NUMBER, AstAction.MakeNumber],
            ( NonTerminal.LITERAL , TokenType.TRUE ) : [TokenType.TRUE, AstAction.MakeBoolean],
            ( NonTerminal.LITERAL , TokenType.FALSE ) : [TokenType.FALSE, AstAction.MakeBoolean],
            ( NonTerminal.PRINT_STATEMENT , TokenType.PRINT ) : [TokenType.PRINT,TokenType.LEFT_PAREN,NonTerminal.EXPR,TokenType.RIGHT_PAREN,
                                                                 AstAction.MakePrint, TokenType.SEMI_COLON]
        }

        self.astTable = {
            AstAction.MakeProgram       : make_program, 
            AstAction.MakeDef           : make_def,
            AstAction.MakeFormalsList   : make_formals_list,
            AstAction.MakeBody          : make_body,
            AstAction.MakeFormal        : make_formal,
            AstAction.MakeLessExp       : make_less_exp,
            AstAction.MakeEqExp         : make_eq_exp,
            AstAction.MakeOrExp         : make_or_exp,
            AstAction.MakeAddExp        : make_plus_exp,
            AstAction.MakeMinusExp      : make_minus_exp,
            AstAction.MakeAndExp        : make_and_exp, 
            AstAction.MakeTimesExp      : make_times_exp,
            AstAction.MakeDivideExp     : make_divide_exp,
            AstAction.MakeExpr          : make_exp,
            AstAction.MakeIfExp         : make_if_exp,
            AstAction.MakeNegate        : make_negate, 
            AstAction.MakeNegative      : make_negative,            
            AstAction.MakeIdentifier    : make_identifier,           
            AstAction.MakeNumber        : make_number,
            AstAction.MakeBoolean       : make_boolean,
            AstAction.MakePrint         : make_print,
            #AstAction.MakeExprList     : make_expr_list,
            AstAction.MakeReturn        : make_return,
            AstAction.MakeStatementList : make_statement_list,
            AstAction.MakeDefList       : make_def_list, 
            AstAction.MakeFormalsList   : make_formals_list,
            AstAction.MakeActuals       : make_actuals
            #AstAction.MakeFunctionCall  : make_function_call
        }
            
      
        
    def parse(self):
        ##LL1 parser for Flair       
        self.parse_stack.pushProper(TokenType.EOF)  
        self.parse_stack.pushProper(NonTerminal.PROGRAM)
        
        while self.parse_stack.size() > 0:
            #input()
            #print("================")
            #print("Parse", self.parse_stack)
            #print("------------------")
            #print("Semantic",self.semantic_stack)
            #print("==================")
            A = self.parse_stack.top()
            #print(self.semantic_stack.size())
            
            if isinstance(A, TokenType):
                t = self.scanner.next()                
                if t.getTokenType() == A:
                                         
                    if t.getTokenType() in [TokenType.IDENTIFIER, \
                                            TokenType.NUMBER, TokenType.INTEGER , TokenType.BOOLEANLITERAL]:
                        self.semantic_stack.pushProper(t.getValue())
                    elif t.getTokenType() == TokenType.TRUE:
                        self.semantic_stack.pushProper('true')
                    elif t.getTokenType() == TokenType.FALSE:
                        self.semantic_stack.pushProper('false')
                    self.parse_stack.pop()
                else:
                    msg = 'token mismatch: {} and {}'
                    raise ParseError(msg.format(A, t))
                
            elif isinstance(A, NonTerminal):
                t = self.scanner.peek()
                
                tup = (A, t.getTokenType())
                #print("TUP", tup)
                try:
                    rule = self.parseTable[tup]  #error here (used to be)
                except:
                    msg = 'cannot expand {} on stack: {}'
                    raise ParseError(msg.format(A, t))
                #print("RULE", rule)
                self.parse_stack.pop()
                self.parse_stack.pushRule(rule)
            

            elif isinstance(A, AstAction):

                action = self.parse_stack.pop()
                #print("ACTION", action, "resulting stack ->")
                
                self.astTable[action](self.semantic_stack)                           
            else:
                msg = 'invalid item on stack: {}'
                raise ParseError(msg.format(A))

        if not t.isEOF():
            msg = 'unexpected token at end: {}'
            raise ParseError(msg.format(t))
        #print("SIZE:", self.semantic_stack.size())
        if (self.semantic_stack.size()) > 1:
            raise ValueError("Something went wrong")   
        return (self.semantic_stack.pop())
        
