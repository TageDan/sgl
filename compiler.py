from lexer import Lexer
from parse import Parser
from gen import Generator
import sys

def main():
    p = sys.argv[1]
    file = p+".sgl"
    print(file)
    lex = Lexer(file)
    gen = Generator(p+".html")
    tokens = lex.tokenize()
    parse = Parser(tokens, gen)
    parse.program()

if __name__ == "__main__":
    main()