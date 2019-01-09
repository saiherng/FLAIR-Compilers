#! /Library/Frameworks/Python.framework/Versions/3.4/bin/python3.4


import sys
import os
from flr_token import Token, TokenType
from scanner import Scanner
from error import LexicalError, ParseError, SemanticError
from flr_parser import Parser
from type_checker import TypeChecker
from codeGen import CodeGenerator

program  = """
program main(a:integer, b:integer);
begin
  return 1
end.
"""
scanner  = Scanner(program)
parser   = Parser(scanner)
ast = parser.parse()
t_checker = TypeChecker(ast)
t_checker.type_check()
#t_checker.pretty_print()
tm_code = CodeGenerator(ast, t_checker.get_symbol_table(), t_checker.function_called())
print(tm_code.generate())


