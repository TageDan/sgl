from lexer import Lexer
from parse import Parser

file = "SIN.sgl"
lex = Lexer("SIN.sgl")
parse = Parser(lex.tokenize())
parse.program()
