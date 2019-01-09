#! /Library/Frameworks/Python.framework/Versions/3.4/bin/python3.4

import sys
import os
#sys.path.insert(0, 'src/')
from flr_token import Token, TokenType
from scanner import Scanner
from error import LexicalError, ParseError
from flr_parser import Parser


try:
    filename = sys.argv[1]
    myfile   = open(filename)
    program  = myfile.read()
    scanner  = Scanner(program)
    parser   = Parser(scanner)
    print_out = parser.parse()
    print(print_out)

except LexicalError as le:
    print('Lexical error: ' + str(le))
except ParseError as pe:
    print('Parse error: ' + str(pe))
except Exception as exc:
    print('Something went wrong: ' + str(exc))
