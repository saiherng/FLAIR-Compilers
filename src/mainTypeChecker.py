#! /Library/Frameworks/Python.framework/Versions/3.4/bin/python3.4
"""
"OR" print function remaining in type_checker
"""

import sys
import os
from flr_token import Token, TokenType
from scanner import Scanner
from error import LexicalError, ParseError, SemanticError
from flr_parser import Parser
from type_checker import TypeChecker

program  = """
program factors( n : integer );
    begin
      return if n < 1 then
            if n < 5 then
                5
                else 10
         else
            1
    end.
"""
scanner  = Scanner(program)
parser   = Parser(scanner)
ast = parser.parse()
print("AST\n", ast, "\n\n\n")
t_checker = TypeChecker(ast)
t_checker.type_check()
t_checker.pretty_print()

