from lexer import Lexer
from parse import Parser
from gen import Generator

file = "SIN.sgl"
lex = Lexer("SIN.sgl")
parse = Parser(lex.tokenize())
gen = Generator("SIN.html")
parse.program()
