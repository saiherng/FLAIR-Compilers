def manage(lst):
    lst = lst.split()
    for i in range(len(lst)):
        if lst[i] == "+":
            lst[i] = "TokenType.ADD"
        elif lst[i] == "-":
            lst[i] = "TokenType.SUBTRACT"
        elif lst[i] == "/":
            lst[i] = "TokenType.DIVIDE"
        elif lst[i] == "*":
            lst[i] = "TokenType.MULTIPLY"
        elif lst[i] == "<":
            lst[i] = "TokenType.LESSTHAN"
        elif lst[i] == "not":
            lst[i] = "TokenType.NOT"
        
        elif lst[i] == "not":
            lst[i] = "TokenType.NOT"
        elif lst[i] == ".":
            lst[i] = "TokenType.PERIOD"
        elif lst[i] == "$":
            lst[i] = "TokenType.EOF"
        elif lst[i] == "integer":
            lst[i] = "TokenType.INTEGER"
        elif lst[i] == "true":
            lst[i] = "TokenType.TRUE"
        elif lst[i] == "false":
            lst[i] = "TokenType.FALSE"
        elif lst[i] == "if":
            lst[i] = "TokenType.IF"
        elif lst[i] == "then":
            lst[i] = "TokenType.THEN"
        elif lst[i] == "else":
            lst[i] = "TokenType.ELSE"
        elif lst[i] == "or":
            lst[i] = "TokenType.OR"
        elif lst[i] == "and":
            lst[i] = "TokenType.AND"

        elif lst[i] == "print":
            lst[i] = "TokenType.PRINT"
        elif lst[i] == "program":
            lst[i] = "TokenType.PROGRAM"
        elif lst[i] == "function":
            lst[i] = "TokenType.FUNCTION"
        elif lst[i] == "return":
            lst[i] = "TokenType.RETURN"
        elif lst[i] == "=":
            lst[i] = "TokenType.EQUAL"
        elif lst[i] == "begin":
            lst[i] = "TokenType.BEGIN"
        elif lst[i] == "end":
            lst[i] = "TokenType.END"
        elif lst[i] == ",":
            lst[i] = "TokenType.COMMA"
        elif lst[i] == ";":
            lst[i] = "TokenType.SEMI_COLON"
        elif lst[i] == ":":
            lst[i] = "TokenType.COLON"

        elif lst[i] == "(":
            lst[i] = "TokenType.LEFT_PAREN"
        elif lst[i] == ")":
            lst[i] = "TokenType.RIGHT_PAREN"
        elif lst[i] == "<NUMBER>":
            lst[i] = "TokenType.NUMBER"
        elif lst[i] == "<IDENTIFIER>":
            lst[i] = "TokenType.IDENTIFIER"

        elif lst[i] == "<PROGRAM>":
            lst[i] = "NonTerminal.PROGRAM"

        elif lst[i] == "<DEFINITIONS>":
            lst[i] = "NonTerminal.DEFINITIONS "

        elif lst[i] == "<DEF>":
            lst[i] = "NonTerminal.DEF"

        elif lst[i] == "<FORMALS>":
            lst[i] = "NonTerminal.FORMALS"

        elif lst[i] == "<NONEMPTYFORMALS>":
            lst[i] = "NonTerminal.NONEMPTYFORMALS"

        elif lst[i] == "<NONEMPTY-F-REST>":
            lst[i] = "NonTerminal.NONEMPTY_F_REST"

        elif lst[i] == "<FORMAL>":
            lst[i] = "NonTerminal.FORMAL"


        elif lst[i] == "<BODY>":
            lst[i] = "NonTerminal.BODY"

        elif lst[i] == "<STATEMENT-LIST>":
            lst[i] = "NonTerminal.STATEMENT_LIST"

        elif lst[i] == "<TYPE>":
            lst[i] = "NonTerminal.TYPE"

        elif lst[i] == "<EXPR>":
            lst[i] = "NonTerminal.EXPR"

        elif lst[i] == "<E-TAIL>":
            lst[i] = "NonTerminal.E_TAIL"

        elif lst[i] == "<SIMPLE-EXPR>":
            lst[i] = "NonTerminal.SIMPLE_EXPR"

        elif lst[i] == "<SE-TAIL>":
            lst[i] = "NonTerminal.SE_TAIL"



        elif lst[i] == "<TERM>":
            lst[i] = "NonTerminal.TERM"

        elif lst[i] == "<T-TAIL>":
            lst[i] = "NonTerminal.T_TAIL"

        elif lst[i] == "<FACTOR>":
            lst[i] = "NonTerminal.FACTOR"

        elif lst[i] == "<ID>":
            lst[i] = "NonTerminal.ID"

        elif lst[i] == "<ID-REST>":
            lst[i] = "NonTerminal.ID_REST"

        elif lst[i] == "<ACTUALS>":
            lst[i] = "NonTerminal.ACTUALS"

        elif lst[i] == "<NONEMPTYACTUALS>":
            lst[i] = "NonTerminal.NONEMPTYACTUALS"

        elif lst[i] == "<NONEMPTY-A-REST>":
            lst[i] = "NonTerminal.NONEMPTY_A_REST"

        elif lst[i] == "<PRINT-STATEMENT>":
            lst[i] = "NonTerminal.PRINT_STATEMENT"

        elif lst[i] == "<NONEMPTYACTUALS>":
            lst[i] = "NonTerminal.NONEMPTYACTUALS"
        elif lst[i] == "<LITERAL>":
            lst[i] = "NonTerminal.LITERAL"
        elif lst[i] == "boolean":
            lst[i] = "Terminal.BOOLEANLITERAL"

    return ",".join(lst)

def main():
    file = open("parTable2.txt", 'r')
    terminalList = ["(", "(", ")", "=", "<IDENTIFIER>", "return", \
                                 "<NUMBER>", "<", "*", "/", "function", "begin", \
                                 "integer", "+", "else", "boolean", "then", ";", \
                                 "<BOOLEAN>", "and", "end", "not", "$", "print", \
                                 "if", "e", "-", ".", "or", "program", ",", ":"]
    file.readline()
    string = ""
    for line in file:
        if line[0] != "-":
            line = line.split("|")
            for index in range(1, len(line)):
                if line[index].strip() != "":
                    string += "( " + manage(line[0])
                    string += " , "
                    string += manage(terminalList[index]) + " ) : ["
                    string += manage(line[index]) + "],\n"
    print(string)


        
main()
