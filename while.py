#!/usr/bin/env python3
from lexer import Lexer 
from parser import Parser
from interpreter import Interpreter
import fileinput

for expr in fileinput.input():
    expr = expr.rstrip()
    lexer = Lexer(expr)
    tokens, error = lexer.generate_tokens()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter(ast)
    interpreter.interpret()
    # print(interpreter.show())
    break

# input_text = input('Enter expr: ')
# lexer = Lexer(input_text)
# tokens, error = lexer.generate_tokens()
# parser = Parser(tokens)
# ast = parser.parse()
# interpreter = Interpreter(ast)
# interpreter.interpret()
# # # interpreter.store_repr
# # # print(interpreter.store_repr)
# # print(interpreter.repr_result())