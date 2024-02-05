from lexer import Lexer
from parse_lib import Lib_Parser
from gen_compile_lib import Lib_Generator
import os
import sys


def comp(path):
    if not os.path.isfile(path) and os.path.isfile(path+".js"):
        return open(path+".js").read()
    lex = Lexer(path)
    gen = Lib_Generator(path+".js")
    tokens = lex.tokenize()
    parse = Lib_Parser(tokens, gen)
    parse.section = "FUNCTIONS"
    try:
        parse.functions()
    except SystemExit as e:
        if str(e) != "0":
            sys.exit(str(e))
    return open(path+".js").read()
