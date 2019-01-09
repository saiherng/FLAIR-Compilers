"""
    @author         :  Phu Vijaranakorn, Sai Herng, Rishabh Dalal
    @description    :  Token object for language Flair
    @since          : 31 Aug. 2018
 
"""
from enum import Enum

class TokenType(Enum):
    KEYWORD       = 1         ## "program"   DONE
    IDENTIFIER    = 2         ##             DONE
    LEFT_PAREN    = 3         ##             DONE  
    COLON         = 4         ##             DONE         
    COMMA         = 5         ##             DONE
    RIGHT_PAREN   = 6         ##             DONE
    SEMI_COLON    = 7         ##             DONE
    NUMBER        = 9         ##             DONE


    BOOLEANLITERAL       = 10        ## true,false
    PERIOD        = 11        ##  .          DONE
    EOF           = 12        ##             DONE
    INTEGER       = 13
    TRUE          = 14
    FALSE         = 15
    IF            = 16
    THEN          = 17
    ELSE          = 18
    NOT           = 19
    OR            = 20
    AND           = 21
    PRINT         = 22
    PROGRAM       = 23
    FUNCTION      = 24
    RETURN        = 25
    BEGIN         = 26
    END           = 27

    ADD = 28
    SUBTRACT = 29
    DIVIDE = 30
    MULTIPLY = 31
    EQUAL = 32
    LESSTHAN = 33
    
class Token:
    def __init__(self, tokenType, tokenVal=None):
        self.token_type = tokenType
        self.token_value = tokenVal

    ##---------PRIVATE---------------------------------
        
    def prettyPrint(self, *strings):
        MAX_SPACE = 14
        spaceNum = MAX_SPACE - len(strings[0])
        space = ""  
        for i in range(spaceNum):
            space += " "
    
        return str(strings[0]) + space + str(strings[1])

    def __hash__(self):
        if self.token_type == TokenType.IDENTIFIER:
            return hash(self.token_type)
        elif self.token_type == TokenType.NUMBER:
            return hash(self.token_type)
        elif self.token_type == TokenType.KEYWORD and self.token_value in ['true', 'false']:
            return hash(self.token_type)
        
        return hash(self.token_value)

    def __eq__(self, obj):
        return self.token_value == obj.getValue()

    ##---------PUBLIC----------------------------------
    
    def getValue(self):
        return self.token_value

    def getTokenType(self):
        return self.token_type
    
    def isKeyWord(self):
        return self.token_type == TokenType.KEYWORD

    def isIdentifier(self):
        return self.token_type == TokenType.IDENTIFIER
    
    def isLeftParen(self):
        return self.token_type == TokenType.LEFT_PAREN

    def isRightParen(self):
        return self.token_type == TokenType.RIGHT_PAREN

    def isColon(self):
        return self.token_type == TokenType.COLON

    def isIntType(self):
        return self.token_type == TokenType.TYPE_INT

    def isComma(self):
        return self.token_type == TokenType.COMMA

    def isSemiColon(self):
        return self.token_type == TokenType.SEMI_COLON

    def isNumber(self):
        return self.token_type == TokenType.NUMBER

    def isPeriod(self):
        return self.token_type == TokenType.PERIOD

    def isEOF(self):
        return self.token_type == TokenType.EOF

    def isInteger(self):
        return self.token_type == TokenType.INTEGER

    def isBooleanLiteral(self):
        return self.token_type == TokenType.BOOLEANLITERAL

    def isTrue(self):
        return self.token_type == TokenType.TRUE

    def isFalse(self):
        return self.token_type == TokenType.FALSE

    def isIf(self):
        return self.token_type == TokenType.IF

    def isThen(self):
        return self.token_type == TokenType.THEN

    def isElse(self):
        return self.token_type == TokenType.ELSE

    def isNot(self):
        return self.token_type == TokenType.NOT

    def isOr(self):
        return self.token_type == TokenType.OR

    def isAND(self):
        return self.token_type == TokenType.AND

    def isPrint(self):
        return self.token_type == TokenType.PRINT

    def isProgram(self):
        return self.token_type == TokenType.PROGRAM

    def isFunction(self):
        return self.token_type == TokenType.FUNCTION

    def isReturn(self):
        return self.token_type == TokenType.RETURN

    def isBegin(self):
        return self.token_type == TokenType.BEGIN

    def isEnd(self):
        return self.token_type == TokenType.END    

    def isAdd(self):
        return self.token_type == TokenType.ADD

    def isSubtract(self):
        return self.token_type == TokenType.SUBTRACT

    def isDivide(self):
        return self.token_type == TokenType.DIVIDE
    
    def isMultiply(self):
        return self.token_type == TokenType.MULTIPLY

    def isEqual(self):
        return self.token_type == TokenType.EQUAL

    def isLessThan(self):
        return self.token_type == TokenType.LESSTHAN
    
    def __str__(self):

        if self.isKeyWord():
        
            return self.prettyPrint("Keyword", self.token_value)
            
        elif self.isIdentifier():
            return self.prettyPrint("Identifier", self.token_value)
    
        elif self.isLeftParen():
            return "LeftParen"

        elif self.isRightParen():
            return "RightParen"

        elif self.isColon():
            return "Colon"

        elif self.isComma():
            return "Comma"

        elif self.isSemiColon():
            return "Semicolon"
        
        elif self.isPeriod():
            return "Period"
        
        elif self.isNumber():
            return self.prettyPrint("Number", self.token_value)

        elif self.isAdd():
            return self.prettyPrint("Add", "+")

        elif self.isSubtract():
            return self.prettyPrint("Subtract", "-")

        elif self.isDivide():
            return self.prettyPrint("Divide", "/")
    
        elif self.isMultiply():
            return self.prettyPrint("Multiply", "*")

        elif self.isEqual():
            return self.prettyPrint("Equal", "=")

        elif self.isLessThan():
            return self.prettyPrint("Less than", "<")

        elif self.isInteger():
            return self.prettyPrint("Keyword", "integer")

        elif self.isBooleanLiteral():
            return self.prettyPrint("Keyword", "boolean")

        elif self.isTrue():
            return self.prettyPrint("Keyword", "true")
        
        elif self.isFalse():
            return self.prettyPrint("Keyword", "false")

        elif self.isIf():
            return self.prettyPrint("Keyword", "if")

        elif self.isThen():
            return self.prettyPrint("Keyword", "then")

        elif self.isElse():
            return self.prettyPrint("Keyword", "else")

        elif self.isNot():
            return self.prettyPrint("Keyword", "not")

        elif self.isOr():
            return self.prettyPrint("Keyword", "or")

        elif self.isAND():
            return self.prettyPrint("Keyword", "and")

        elif self.isPrint():
            return self.prettyPrint("Keyword", "print")

        elif self.isProgram():
            return self.prettyPrint("Keyword", "program")

        elif self.isFunction():
            return self.prettyPrint("Keyword", "function")

        elif self.isReturn():
            return self.prettyPrint("Keyword", "return")

        elif self.isBegin():
            return self.prettyPrint("Keyword", "begin")

        elif self.isEnd():
            return self.prettyPrint("Keyword", "end")
            
        else:   # is_eof()
            return 'end_of_stream'
