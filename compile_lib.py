from lexer import Lexer
from parse_lib import Lib_Parser
from gen_compile_lib import Lib_Generator
import os


def comp(path):
    if not os.path.isfile(path) and os.path.isfile(path+".js"):
        return open(path+".js").read()
    print(path)
    print(os.path.isfile(path))
    print(os.path.isfile(path+".js"))
    lex = Lexer(path)
    gen = Lib_Generator(path+".js")
    tokens = lex.tokenize()
    parse = Lib_Parser(tokens, gen)
    parse.section = "FUNCTIONS"
    parse.functions()
    return open(path+".js").read()
