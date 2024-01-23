from lexer import Token, tokenType
import sys
from gen import Generator

class Parser:
    def __init__(self, tokens, generator: Generator):
        self.tokens = tokens
        self.curToken: Token
        self.curPos = -1
        self.section = "none"
        self.line = 1
        self.generator = generator

    def nextToken(self):
        self.curPos += 1
        try:
            self.curToken = self.tokens[self.curPos]
            return True
        except IndexError:
            self.generator.buffer_to_body()
            self.generator.write_to_file()
            sys.exit("file parsed")


    def peek(self):
        return self.tokens[self.curPos +1]
    
    def NL(self):
        while self.curToken.type == tokenType.NEWLINE:
            self.nextToken()
            self.line += 1

    def program(self):
        self.nextToken()
        while self.curPos < len(self.tokens):
            self.NL()
            if self.curToken.type != tokenType.SECTION:
                self.abort("Excpected section declaration!")
            elif self.curToken.literal == "FUNCTIONS":
                self.section = "FUNCTIONS"
                self.generator.set_section("FUNCTIONS")
                self.functions()
            elif self.curToken.literal == "CONFIG":
                self.section = "CONFIG"
                self.generator.set_section("CONFIG")
                self.config()
            elif self.curToken.literal == "MAIN":
                self.section = "MAIN"
                self.generator.set_section("MAIN")
                self.main()
        
    def config(self):
        self.nextToken()
        while self.curToken.type != tokenType.SECTION:
            self.NL()
            if self.curToken.type not in [tokenType.NAME, tokenType.SECTION]:
                self.abort("Expected declaration in config")
            if self.curToken.type == tokenType.SECTION:
                # self.generator.buffer_to_body()
                continue
            self.declaration()

    def main(self):
        self.nextToken()
        while self.curToken.type != tokenType.SECTION:
            self.NL()
            self.statement()

    def writeCurToBuf(self):
        self.generator.write_to_buffer(self.curToken.literal)

    def functions(self):
        if self.peek().type != tokenType.NEWLINE:
            self.abort("Expected newline after section declaration")
        self.nextToken()
        while self.curToken.type != tokenType.SECTION:
            self.NL()
            if self.curToken.type == tokenType.NAME:
                self.functionDeclaration()
            elif self.curToken.type == tokenType.SECTION:
                self.generator.buffer_to_body()
                break
            else:
                self.abort("Excpected function declaration in section FUNCTIONS")
            
    def functionDeclaration(self):
        self.generator.write_to_buffer("function ")
        self.writeCurToBuf()
        self.nextToken()
        if self.curToken.type != tokenType.LEFT_PAREN:
            self.abort("Excpected left-paren in function declaration, got " + self.curToken.type.name)
        self.writeCurToBuf()
        while self.peek().type != tokenType.RIGHT_PAREN:
            self.nextToken()
            if self.curToken.type != tokenType.NAME:
                self.abort("Expected name token for function parameter")
            self.writeCurToBuf()
            if self.peek().type != tokenType.RIGHT_PAREN:
                self.generator.write_to_buffer(",")
        self.nextToken()
        self.writeCurToBuf()
        self.nextToken()
        if self.curToken.type != tokenType.EQ:
            self.abort("Expected equals sign in function declaration")
        self.nextToken()
        if self.curToken.type != tokenType.LEFT_SQUIG:
            self.abort("Expected '{' in function declaration")
        self.writeCurToBuf()
        if self.peek().type != tokenType.NEWLINE:
            self.abort("Expected newline after function declaration")
        self.nextToken()
        self.writeCurToBuf()
        while self.curToken.type != tokenType.RIGHT_SQUIG:
            self.NL()
            self.statement()
        self.writeCurToBuf()
        self.generator.write_to_buffer("\n")
        self.nextToken()

    def statement(self):
        if self.curToken.type == tokenType.DRAW:
            self.draw()
        elif self.curToken.type == tokenType.NAME:
            if self.peek().type == tokenType.EQ:
                self.declaration()
            elif self.peek().type == tokenType.LEFT_PAREN:
                self.functionCall()
                self.nextToken()
                if self.curToken.type != tokenType.NEWLINE:
                    self.abort("Expected newline after isolated function-call")
                self.writeCurToBuf()

            elif self.section == "FUNCTIONS":
                self.functionReturn()
        elif self.curToken.type in [tokenType.NUMBER, tokenType.LEFT_SQUARE, tokenType.MINUS, tokenType.STRING, tokenType.LEFT_PAREN] and self.section == "FUNCTIONS":
            self.functionReturn()
        elif self.curToken.type == tokenType.IF:
            self.IF()
        elif self.curToken.type == tokenType.LOOP:
            self.loop()
        elif self.curToken.type == tokenType.CLEAR:
            self.clear()
        elif self.curToken.type == tokenType.PUSH:
            self.push()
        elif self.curToken.type == tokenType.BREAK:
            self.BREAK()
        elif self.curToken.type == tokenType.PRINT:
            self.print()
        else:
            self.abort(f"Unexcpected statement ('{self.curToken.literal}')")

        self.generator.buffer_to_body()

    def functionCall(self):
        self.writeCurToBuf()
        self.nextToken()
        self.writeCurToBuf()
        self.nextToken()
        while self.curToken.type != tokenType.RIGHT_PAREN:
            self.expression()
        self.writeCurToBuf()

    def declaration(self):
        "ident"
        self.writeCurToBuf()
        self.nextToken()
        "="
        self.writeCurToBuf()
        self.nextToken()
        "exp"
        self.expression()
        if self.curToken.type != tokenType.NEWLINE:
            self.abort("Expected newline after variable declaration")
        self.generator.buffer_to_body()
        if self.section != "CONFIG":
            self.writeCurToBuf()
            self.generator.buffer_to_body()
        self.NL()
        
    def expression(self):
        if self.curToken.type == tokenType.LEFT_SQUARE:
            self.list()
        else:
            self.unary()
            while self.curToken.type in [tokenType.PLUS, tokenType.MINUS, tokenType.MOD, tokenType.MULTIPLY, tokenType.DIVIDE, tokenType.EXP]:
                self.writeCurToBuf()
                self.nextToken()
                self.unary()
        
    def unary(self):
        neg = False
        if self.curToken.type == tokenType.MINUS:
            neg = True
            self.generator.write_to_buffer("(-")
            self.nextToken()
        if self.curToken.type == tokenType.NAME:
            if self.peek().type == tokenType.LEFT_PAREN:
                self.functionCall()
            else:
                self.writeCurToBuf()
            self.nextToken()
        elif self.curToken.type == tokenType.NUMBER:
            self.writeCurToBuf()
            self.nextToken()
        elif self.curToken.type == tokenType.LEFT_PAREN:
            self.writeCurToBuf()
            self.nextToken()
            self.expression()
            if self.curToken.type != tokenType.RIGHT_PAREN:
                self.abort("Expected closing paren")
            self.writeCurToBuf()
            self.nextToken()
        else:
            self.abort("Expected name or number as unary")
        if neg:
            self.generator.write_to_buffer(")")
    
    def list(self):
        "["
        self.writeCurToBuf()
        self.nextToken()
        while self.curToken.type != tokenType.RIGHT_SQUARE:
            self.expression()
            if self.curToken.type != tokenType.RIGHT_SQUARE:
                self.generator.write_to_buffer(",")
        self.writeCurToBuf()
        self.nextToken()
        
    def functionReturn(self):
        self.generator.write_to_buffer("return ")
        self.expression()
        self.generator.write_to_buffer("\n")
        self.NL()
    
    def IF(self):
        "if"
        self.writeCurToBuf()
        self.nextToken()
        self.comparison()
        if self.curToken.type != tokenType.LEFT_SQUIG:
            self.abort("expected '{' after if statement")
        self.writeCurToBuf()
        self.nextToken()
        if self.curToken.type != tokenType.NEWLINE:
            self.abort("expected newline after if statement")
        self.writeCurToBuf()
        while self.curToken.type != tokenType.RIGHT_SQUIG:
            self.NL()
            self.statement()
        self.writeCurToBuf()
        self.nextToken()
        self.NL()

    def comparison(self):
        self.generator.write_to_buffer("(")
        self.expression()
        if self.curToken.type not in [tokenType.EQEQ, tokenType.LESS, tokenType.LESS_EQ, tokenType.GREAT, tokenType.GREAT_EQ, tokenType.NOTEQ]:
            self.abort("Excpected comparison in if statement")
        while self.curToken.type in [tokenType.EQEQ, tokenType.LESS, tokenType.LESS_EQ, tokenType.GREAT, tokenType.GREAT_EQ, tokenType.NOTEQ]:
            self.writeCurToBuf()
            self.nextToken()
            self.expression()
        self.generator.write_to_buffer(")")

    def loop(self):
        print(self.line)
        self.generator.write_to_buffer("while(true)")
        self.nextToken()
        if self.curToken.type != tokenType.LEFT_SQUIG:
            self.abort("Expected '{' in loop statement")
        self.writeCurToBuf()
        self.nextToken()
        if self.curToken.type != tokenType.NEWLINE:
            self.abort("Expected newline in loop statement")
        self.writeCurToBuf()
        self.NL()
        while self.curToken.type != tokenType.RIGHT_SQUIG:
            self.statement()
            self.NL()
        print(self.line)
        self.writeCurToBuf()
        self.nextToken()
        self.NL()

    def clear(self):
        "clear"
        self.generator.write_to_buffer("await ")
        self.writeCurToBuf()
        self.nextToken()
        if self.curToken.type != tokenType.LEFT_PAREN:
            self.abort("Expected left paren for clear statement")
        self.writeCurToBuf()
        self.nextToken()
        if self.curToken.type != tokenType.RIGHT_PAREN:
            self.abort("Expected right paren for clear statement (clear doesn't take any params)")
        self.writeCurToBuf()
        self.nextToken()
        if self.curToken.type != tokenType.NEWLINE:
            self.abort("Expected newline after clear")
        self.writeCurToBuf()
        self.NL()

    def push(self):
        "push"
        self.nextToken()
        if self.curToken.type != tokenType.LEFT_PAREN:
            self.abort("Expected left paren for push statement")
        self.nextToken()
        if self.curToken.type != tokenType.NAME:
            self.abort("Expected name as first parameter to push statement")
        self.writeCurToBuf()
        self.generator.write_to_buffer("[")
        self.expression()
        if self.curToken.type != tokenType.RIGHT_PAREN:
            self.abort("Expected right paren for push statement, (push takes exactly 2 params)")
        self.generator.write_to_buffer("]")
        self.nextToken()
        if self.curToken.type != tokenType.NEWLINE:
            self.abort("Expected newline after push")
        self.writeCurToBuf()
        self.NL()

    def BREAK(self):
        self.writeCurToBuf()
        self.nextToken()
        if self.curToken.type != tokenType.NEWLINE:
            self.abort("Expected newline after break")
        self.writeCurToBuf()
        self.NL()

    def print(self):
        self.nextToken()
        self.generator.write_to_buffer("console.log")
        if self.curToken.type != tokenType.LEFT_PAREN:
            self.abort("Expected left paren for print statement")
        self.writeCurToBuf()
        self.nextToken()
        if self.curToken.type == tokenType.STRING:
            self.writeCurToBuf()
            self.nextToken()
        else:
            self.expression()
        if self.curToken.type != tokenType.RIGHT_PAREN:
            self.abort("Expected right paren for print statement, (print takes exactly 1 params)")
        self.writeCurToBuf()
        self.nextToken()
        if self.curToken.type != tokenType.NEWLINE:
            self.abort("Expected newline after push")
        self.writeCurToBuf()
        self.NL()
        
    def draw(self):
        "draw"
        self.writeCurToBuf()
        self.nextToken()
        if self.curToken.type != tokenType.LEFT_PAREN:
            self.abort("Expected left paren for draw statement")
        self.writeCurToBuf()
        self.nextToken()
        for i in range(3):
            self.expression()
            if i != 2:
                self.generator.write_to_buffer(",")
        if self.curToken.type != tokenType.RIGHT_PAREN:
            self.abort("Expected right paren for draw statement, (draw takes exactly 3 params)")
        self.writeCurToBuf()
        self.nextToken()
        if self.curToken.type != tokenType.NEWLINE:
            self.abort("Expected newline after draw")
        self.writeCurToBuf()
        self.NL()
        


    
            
            

    def abort(self, message):
        sys.exit("Parser Error: "+message+" : line " + str(self.line))