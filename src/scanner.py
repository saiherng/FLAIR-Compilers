"""
    @author         :  Sai Herng, Rishabh Dalal, Phu Vijaranakorn
    @description    :  Scanner for language Flair
    @since          :  12 Sept. 2018
 
"""
import sys
from enum import Enum
from flr_token import Token, TokenType
from error import LexicalError

RESERVED_WORDS = ["program", "function", "begin", "end", "print", "or", \
                  "and", "if", "then", "else", "not", "return", "integer", "boolean",\
                  "true", "false"]

HIGH_RANGE = (2**32) - 1
IDENTIFIER_LIMIT = 256

class State(Enum):
    looking    = 1
    number     = 3
    string     = 4
    comment    = 5
    zero       = 6
    openparen  = 7
    closeparen = 8
    dot        = 9
    comma      = 10
    semicolon  = 11
    colon      = 12
    lessthan   = 13
    equal      = 14
    multiply   = 15
    divide     = 16
    subtract   = 17
    add        = 18

class Scanner:
    def __init__(self, programStr):
        self.programStr = programStr
        self.index      = 0
        self.linenumber = 1
        self.length     = len(self.programStr)
        self.char_sums = sys.maxsize
        self.state = State.looking
        self.accum = ""
        self.peektoken = None

    ##----------------------PUBLIC---------------------------
        
    def peek(self):
        ##for peeking a token
        
        if not self.peektoken:
            self.peektoken = self.get_next_token()
        return self.peektoken


    def next(self):
        ## for returning the next token
        
        if self.peektoken:
            token = self.peektoken
            self.peektoken = None

            return token 
        else:

            return self.get_next_token()

    ##------------PRIVATE-------------------------------------
        
    def get_next_token(self):
        ##getting the next token to return
        
        self.accum = ''
        while self.index < self.length:
            ch = self.programStr[self.index]
            
            if self.state == State.looking:  
                self.handleInitialState(ch)

            elif self.state == State.number:
                if self.programStr[self.index].isdigit():
                    self.accum += self.programStr[self.index]
                    self.index += 1
                else:
                    return self.handleNumberState()

            elif self.state == State.zero:
                return self.handleZeroState()

            elif self.state == State.string:
                if ch.isalpha() or ch.isdigit() or ch == "_":
                    self.accum += ch
                    self.index += 1
                else:
                    return self.handleStringState()

            elif self.state == State.add:
                self.state = State.looking
                self.index += 1
                return Token(TokenType.ADD)

            elif self.state == State.dot:
                self.state = State.looking
                self.index += 1
                return Token(TokenType.PERIOD)

            elif self.state == State.comma:
                self.state = State.looking
                self.index += 1
                return Token(TokenType.COMMA)

            elif self.state == State.openparen:
                self.state = State.looking
                self.index += 1
                return Token(TokenType.LEFT_PAREN)

            elif self.state == State.closeparen:
                self.state = State.looking
                self.index += 1
                return Token(TokenType.RIGHT_PAREN)

            elif self.state == State.colon:
                self.state = State.looking
                self.index += 1
                return Token(TokenType.COLON)

            elif self.state == State.semicolon:
                self.state = State.looking
                self.index += 1
                return Token(TokenType.SEMI_COLON)

            elif self.state == State.equal:
                self.state = State.looking
                self.index += 1
                return Token(TokenType.EQUAL)

            elif self.state == State.multiply:
                self.state = State.looking
                self.index += 1
                return Token(TokenType.MULTIPLY)

            elif self.state == State.divide:
                self.state = State.looking
                self.index += 1
                return Token(TokenType.DIVIDE)

            elif self.state == State.lessthan:
                self.state = State.looking
                self.index += 1
                return Token(TokenType.LESSTHAN)

            elif self.state == State.subtract:
                self.state = State.looking
                self.index += 1
                return Token(TokenType.SUBTRACT)

            elif self.state == State.add:
                self.state = State.looking
                self.index += 1
                return Token(TokenType.ADD)
            
            elif self.state == State.comment:
                ch = self.programStr[self.index]
                if ch == "}":
                    self.state = State.looking
                self.index += 1

            else:
                msg = 'Invalid character {} at position {}, line {}'.format(ch, self.index%self.char_sums, self.linenumber)
                raise LexicalError(msg)

        if self.accum:
            if self.state == State.number:
                number, self.accum = self.accum, ""
                return self.handleNumber(number)                
            elif self.state == State.string:
                string, self.accum = self.accum, ""
                return self.handleString(string)
            else:
                msg = "Invalid state at position {}, line {}.  How did that happen?".format(self.index%self.char_sums, self.linenumber)
                raise LexicalError(msg)
        return Token(TokenType.EOF, "$")
            
    def is_whitespace(self, ch):
        ##Checking to see if a character is considered whitespace
        
        if '\n' in ch:
            self.linenumber += 1
            self.char_sums = self.index
        return ch in "\n\t\r "

    def handleString(self, string):
        ##Returning appropriate string token
        
        if string in RESERVED_WORDS:
            if string == "integer":
                return Token(TokenType.INTEGER, "integer")
            if string == "boolean":
                return Token(TokenType.BOOLEANLITERAL, "boolean")
            elif string == "true":
                return Token(TokenType.TRUE)
            elif string == "false":
                return Token(TokenType.FALSE)
            elif string == "if":
                return Token(TokenType.IF)
            elif string == "then":
                return Token(TokenType.THEN)
            elif string == "else":
                return Token(TokenType.ELSE)
            elif string == "not":
                return Token(TokenType.NOT)
            elif string == "or":
                return Token(TokenType.OR)
            elif string == "and":
                return Token(TokenType.AND)
            elif string == "print":
                return Token(TokenType.PRINT)
            elif string == "program":
                return Token(TokenType.PROGRAM)
            elif string == "function":
                return Token(TokenType.FUNCTION)
            elif string == "return":
                return Token(TokenType.RETURN)
            elif string == "begin":
                return Token(TokenType.BEGIN)
            elif string == "end":
                return Token(TokenType.END)
        
        if len(string) > IDENTIFIER_LIMIT:
            msg = "Maximum identifier length surpassed in line {}".format(string, self.linenumber)
            raise LexicalError(msg)
        return Token(TokenType.IDENTIFIER, string)

    def handleNumber(self, number):
        ##Handling number edge cases
        
        number = int(number)
        if number <= HIGH_RANGE:
            return Token(TokenType.NUMBER, int(number))
        else:
            msg = "Integer {} out of bounds in line {}".format(number, self.linenumber)
            raise LexicalError(msg)

    def handleInitialState(self, ch):
        ##Taking care of initial state
        
        if self.is_whitespace(ch):
            self.index += 1
    
        elif ch.isdigit() and ch != "0":
            self.state = State.number
            self.index += 1
            self.accum = ch

        elif ch.isalpha():
            self.state = State.string
            self.accum = ch
            self.index += 1

        elif ch == ".":
            self.state = State.dot

        elif ch == ",":
            self.state = State.comma

        elif ch == "(":
            self.state = State.openparen
            
        elif ch == ")":    
            self.state = State.closeparen

        elif ch == ":":
            self.state = State.colon

        elif ch == ";":
            self.state = State.semicolon

        elif ch == "=":
            self.state = State.equal

        elif ch == "*":
            self.state = State.multiply

        elif ch == "/":
            self.state = State.divide

        elif ch == "-":
            self.state = State.subtract

        elif ch == "+":
            self.state = State.add
            
        elif ch == "{":
            self.state = State.comment
            self.index += 1

        elif ch == "<":
            self.state = State.lessthan
            self.index += 1

        elif ch == "0":
            self.state = State.zero
            self.index += 1
            
        else:
            msg = 'invalid characters at position {}, line {}'.format(self.index%self.char_sums, self.linenumber)
            raise LexicalError(msg)

    def handleNumberState(self):
        ##Taking care of number state

        ch = self.programStr[self.index]
         
        if self.is_whitespace(self.programStr[self.index]):
            number, self.accum = self.accum, ""
            self.state = State.looking
            return self.handleNumber(number)


        elif ch == ".":
            number, self.accum = self.accum, ""
            self.state = State.dot
            return self.handleNumber(number)

        elif ch == ",":
            number, self.accum = self.accum, ""
            self.state = State.comma
            return self.handleNumber(number)

        elif ch == "(":
            print("INSIED2")
            number, self.accum = self.accum, ""
            self.state = State.openparen
            return self.handleNumber(number)

        elif ch == ")":
            number, self.accum = self.accum, ""
            self.state = State.closeparen
            return self.handleNumber(number)

        elif ch == ":":
            number, self.accum = self.accum, ""
            self.state = State.colon
            return self.handleNumber(number)

        elif ch == ";":
            number, self.accum = self.accum, ""
            self.state = State.semicolon
            return self.handleNumber(number)

        elif ch == "=":
            number, self.accum = self.accum, ""
            self.state = State.equal
            return self.handleNumber(number)

        elif ch == "<":
            number, self.accum = self.accum, ""
            self.state = State.lessthan
            return self.handleNumber(number)
        
        elif ch == "*":
            number, self.accum = self.accum, ""
            self.state = State.multiply
            return self.handleNumber(number)

        elif ch == "/":
            number, self.accum = self.accum, ""
            self.state = State.divide
            return self.handleNumber(number)
        
        elif ch == "-":
            number, self.accum = self.accum, ""
            self.state = State.subtract
            return self.handleNumber(number)
        
        elif ch == "+":
            number, self.accum = self.accum, ""
            self.state = State.add
            return self.handleNumber(number)
            
        elif ch == "{":
            self.state = State.comment
            self.index += 1

        elif self.programStr[self.index] == "{":
            number, self.accum = self.accum, ""
            self.state = State.comment
            return self.handleNumber(number)
        
        else:
            msg = 'invalid character at position {}, line {}'.format(self.index%self.char_sums, self.linenumber)
            raise LexicalError(msg)

    def handleZeroState(self):
        ##Taking care of zero state
        
        ch = self.programStr[self.index]
        if self.is_whitespace(ch):
            self.index += 1
            self.state = State.looking
            return Token(TokenType.NUMBER, 0)

        elif ch == ".":
            self.state = State.dot
            return Token(TokenType.NUMBER, 0)

        elif ch == ",":
            self.state = State.comma
            return Token(TokenType.NUMBER, 0)

        elif ch == "(":
            self.state = State.openparen
            return Token(TokenType.NUMBER, 0)

        elif ch == "<":
            self.state = State.lessthan
            return Token(TokenType.NUMBER, 0)

        elif ch == ")":
            self.state = State.closeparen
            return Token(TokenType.NUMBER, 0)

        elif ch == ":":
            self.state = State.colon
            return Token(TokenType.NUMBER, 0)

        elif ch == ";":
            self.state = State.semicolon
            return Token(TokenType.NUMBER, 0)

        elif ch == "=":
            self.state = State.equal
            return Token(TokenType.NUMBER, 0)
        
        elif ch == "*":
            self.state = State.multiply
            return Token(TokenType.NUMBER, 0)

        elif ch == "/":
            self.state = State.divide
            return Token(TokenType.NUMBER, 0)
        
        elif ch == "-":
            self.state = State.subtract
            return Token(TokenType.NUMBER, 0)
        
        elif ch == "+":
            self.state = State.add
            return Token(TokenType.NUMBER, 0)

        elif ch == "{":
            self.state = State.comment
            self.index += 1
            return Token(TokenType.NUMBER, 0)    
        else:
            if ch.isdigit():        
                msg = "Integer cannot start with 0 in line {}".format(self.index%self.char_sums, self.linenumber)
            else:
                msg = "Invalid character {} at position {}, line {}".format(ch, self.index%self.char_sums, self.linenumber)
            raise LexicalError(msg)


    def handleStringState(self):
        ##Taking care of string state
        
        ch = self.programStr[self.index]
        
        if self.is_whitespace(ch):
            word, self.accum = self.accum, ""
            self.state = State.looking
            return self.handleString(word)

        elif ch == "{":
            self.state = State.comment
            word, self.accum = self.accum, ""
            return self.handleString(word)


        elif ch == ".":
            word, self.accum = self.accum, ""
            self.state = State.dot
            return self.handleString(word)

        elif ch == "<":
            word, self.accum = self.accum, ""
            self.state = State.lessthan
            return self.handleString(word)

        elif ch == ",":
            word, self.accum = self.accum, ""
            self.state = State.comma
            return self.handleString(word)

        elif ch == "(":
            word, self.accum = self.accum, ""
            self.state = State.openparen
            return self.handleString(word)

        elif ch == "(":
            word, self.accum = self.accum, ""
            self.state = State.lessthan
            return self.handleString(word)

        elif ch == ")":
            word, self.accum = self.accum, ""
            self.state = State.closeparen
            return self.handleString(word)

        elif ch == ":":
            word, self.accum = self.accum, ""
            self.state = State.colon
            return self.handleString(word)

        elif ch == ";":
            word, self.accum = self.accum, ""
            self.state = State.semicolon
            return self.handleString(word)

        elif ch == "=":
            word, self.accum = self.accum, ""
            self.state = State.equal
            return self.handleString(word)
        
        elif ch == "*":
            word, self.accum = self.accum, ""
            self.state = State.multiply
            return self.handleString(word)

        elif ch == "/":
            word, self.accum = self.accum, ""
            self.state = State.divide
            return self.handleString(word)
        
        elif ch == "-":
            word, self.accum = self.accum, ""
            self.state = State.subtract
            return self.handleString(word)
        
        elif ch == "+":
            word, self.accum = self.accum, ""
            self.state = State.add
            return self.handleString(word)     

            
        else:
            msg = 'Invalid character {} at position {}, line {}'.format(ch, self.index%self.char_sums, self.linenumber)
            raise LexicalError(msg)

