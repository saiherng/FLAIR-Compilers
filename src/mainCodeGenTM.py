#! /Library/Frameworks/Python.framework/Versions/3.4/bin/python3.4


import sys
import os
from flr_token import Token, TokenType
from scanner import Scanner
from error import LexicalError, ParseError, SemanticError
from flr_parser import Parser
from type_checker import TypeChecker
from codeGen import CodeGenerator
from code_latest import CodeGenerator

program  = """
program main();
begin
  return 1+2
end.
"""
scanner  = Scanner(program)
parser   = Parser(scanner)
ast = parser.parse()
t_checker = TypeChecker(ast)
t_checker.type_check()


c = CodeGenerator(ast, t_checker.get_symbol_table(), t_checker.get_symbol_table())
c.generate()
