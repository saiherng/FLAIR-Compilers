#! /Library/Frameworks/Python.framework/Versions/3.4/bin/python3.4

import sys
sys.path.insert(0, 'src/')
from flr_token import Token, TokenType
from scanner import Scanner
from error import LexicalError

try:
    filename = sys.argv[1]
    myfile   = open(filename)
    program  = myfile.read()

    scanner  = Scanner(program)
    token = Token(TokenType.EOF)

    print("Tokens:\n")
    while True:
        tkn = scanner.get_next_token()
        if not tkn:
            print("Something is wrong. Correct me.")
            break
        if tkn.isEOF():                  
            print("\nExecution complete.")
            break 
        print(tkn)   

except LexicalError as le:
    print('Lexical error: ' + str(le))
except Exception as exc:
    print('Something went wrong: ' + str(exc))
