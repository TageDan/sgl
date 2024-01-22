from lexer import Token, tokenType
import sys

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.curToken: Token
        self.curPos = -1
        self.section = "none"
        self.line = 1

    def nextToken(self):
        self.curPos += 1
        try:
            self.curToken = self.tokens[self.curPos]
            # print(self.curToken)
            return True
        except IndexError:
            return False


    def peek(self):
        return self.tokens[self.curPos +1]
    
    def NL(self):
        while self.curToken.type == tokenType.NEWLINE:
            self.nextToken()
            self.line += 1
        print()
        print(f"{self.line}: ", end= "")

    def program(self):
        print("Program")
        self.nextToken()
        print("1: ", end="")
        while self.curPos < len(self.tokens):
            self.NL()
            if self.curToken.type != tokenType.SECTION:
                self.abort("Excpected section declaration!")
            elif self.curToken.literal == "FUNCTIONS":
                self.section = "FUNCTIONS"
                self.functions()
            elif self.curToken.literal == "CONFIG":
                self.section = "CONFIG"
                self.config()
            elif self.curToken.literal == "MAIN":
                self.section = "MAIN"
                self.main()
        
    def config(self):
        self.nextToken()
        while self.curToken.type != tokenType.SECTION:
            self.NL()
            if self.curToken.type != tokenType.SECTION:
                self.nextToken()
            

    def main(self):
        print("Section main")
        self.nextToken()
        while self.curToken.type != tokenType.SECTION:
            self.NL()
            self.statement()


    def functions(self):
        print("section - functions")
        if self.peek().type != tokenType.NEWLINE:
            self.abort("Expected newline after section declaration")
        self.nextToken()
        while self.curToken.type != tokenType.SECTION:
            self.NL()
            if self.curToken.type == tokenType.NAME:
                self.functionDeclaration()
            elif self.curToken.type == tokenType.SECTION:
                break
            else:
                self.abort("Excpected function declaration in section FUNCTIONS")
            
    def functionDeclaration(self):
        print("function declaration")
        buffer = self.curToken.literal
        self.nextToken()
        if self.curToken.type != tokenType.LEFT_PAREN:
            self.abort("Excpected left-paren in function declaration, got " + self.curToken.type.name)
        buffer += self.curToken.literal
        while self.peek().type != tokenType.RIGHT_PAREN:
            self.nextToken()
            if self.curToken.type != tokenType.NAME:
                self.abort("Expected name token for function parameter")
            buffer += self.curToken.literal
            if self.peek().type != tokenType.RIGHT_PAREN:
                buffer += ","
        self.nextToken()
        buffer += self.curToken.literal
        print("Function name and params: " + buffer)
        self.nextToken()
        if self.curToken.type != tokenType.EQ:
            self.abort("Expected equals sign in function declaration")
        self.nextToken()
        if self.curToken.type != tokenType.LEFT_SQUIG:
            self.abort("Expected '{' in function declaration")
        if self.peek().type != tokenType.NEWLINE:
            self.abort("Expected newline after function declaration")
        self.nextToken()
        while self.curToken.type != tokenType.RIGHT_SQUIG:
            self.NL()
            self.statement()
        self.nextToken()

    def statement(self):
        if self.curToken.type == tokenType.DRAW:
            self.draw()
        elif self.curToken.type == tokenType.NAME:
            if self.peek().type == tokenType.EQ:
                self.declaration()
            elif self.peek().type == tokenType.LEFT_PAREN:
                self.functionCall()
            elif self.section == "FUNCTIONS":
                self.functionReturn()
        elif self.curToken.type in [tokenType.NUMBER, tokenType.LEFT_SQUARE, tokenType.MINUS, tokenType.STRING] and self.section == "FUNCTIONS":
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

    def functionCall(self):
        print("Statement - function call")
        "ident"
        self.nextToken()
        "("
        self.nextToken()
        while self.curToken.type != tokenType.RIGHT_PAREN:
            self.expression()

    def declaration(self):
        print("Statement - declaration")
        "ident"
        self.nextToken()
        "="
        self.nextToken()
        "exp"
        self.expression()
        if self.curToken.type != tokenType.NEWLINE:
            self.abort("Expected newline after variable declaration")
        self.NL()
        

    def expression(self):
        print("expression")
        if self.curToken.type == tokenType.LEFT_SQUARE:
            self.list()
        else:
            self.unary()
            while self.curToken.type in [tokenType.PLUS, tokenType.MINUS, tokenType.MOD, tokenType.MULTIPLY, tokenType.DIVIDE, tokenType.EXP]:
                self.nextToken()
                self.unary()
        
    def unary(self):
        print("unary")
        if self.curToken.type == tokenType.MINUS:
            print("negative")
            self.nextToken()
        if self.curToken.type == tokenType.NAME:
            if self.peek().type == tokenType.LEFT_PAREN:
                self.functionCall()
            else:
                print("ident")
            self.nextToken()
        elif self.curToken.type == tokenType.NUMBER:
            print("number")
            self.nextToken()
        elif self.curToken.type == tokenType.LEFT_PAREN:
            self.nextToken()
            self.expression()
            if self.curToken.type != tokenType.RIGHT_PAREN:
                self.abort("Expected closing paren")
            self.nextToken()
        else:
            self.abort("Expected name or number as unary")
    
    def list(self):
        print("list")
        "["
        self.nextToken()
        while self.curToken.type != tokenType.RIGHT_SQUARE:
            self.expression()
        self.nextToken()
        

    def functionReturn(self):
        print("Statement - function return")
        self.expression()
        self.NL()
    
    def IF(self):
        print("Statement - if")
        "if"
        self.nextToken()
        self.comparison()

    def comparison(self):
        pass

    def loop(self):
        print("Statement - loop")
        "loop"
        self.nextToken()
        if self.curToken.type != tokenType.LEFT_SQUIG:
            self.abort("Expected '{' in loop statement")
        self.nextToken()
        if self.curToken.type != tokenType.NEWLINE:
            self.abort("Expected newline in loop statement")
        self.NL()
        while self.curToken.type != tokenType.RIGHT_SQUIG:
            self.statement()
            self.NL()

    def clear(self):
        print("Statement - clear")
        "clear"
        self.nextToken()
        if self.curToken.type != tokenType.LEFT_PAREN:
            self.abort("Expected left paren for clear statement")
        self.nextToken()
        if self.curToken.type != tokenType.RIGHT_PAREN:
            self.abort("Expected right paren for clear statement (clear doesn't take any params)")
        self.nextToken()
        if self.curToken.type != tokenType.NEWLINE:
            self.abort("Expected newline after clear")
        self.NL()

    def push(self):
        print("Statement - push")
        "push"
        self.nextToken()
        if self.curToken.type != tokenType.LEFT_PAREN:
            self.abort("Expected left paren for push statement")
        self.nextToken()
        for i in range(2):
            self.expression()
        if self.curToken.type != tokenType.RIGHT_PAREN:
            self.abort("Expected right paren for push statement, (push takes exactly 2 params)")
        self.nextToken()
        if self.curToken.type != tokenType.NEWLINE:
            self.abort("Expected newline after push")
        self.NL()

    def BREAK(self):
        print("Statement - break")
        self.nextToken()
        if self.curToken.type != tokenType.NEWLINE:
            self.abort("Expected newline after break")
        self.NL()

    def print(self):
        print("Statement - print")
        self.nextToken()
        if self.curToken.type != tokenType.LEFT_PAREN:
            self.abort("Expected left paren for print statement")
        self.nextToken()
        self.expression()
        if self.curToken.type != tokenType.RIGHT_PAREN:
            self.abort("Expected right paren for print statement, (print takes exactly 1 params)")
        self.nextToken()
        if self.curToken.type != tokenType.NEWLINE:
            self.abort("Expected newline after push")
        self.NL()
        
    def draw(self):
        print("Statement - draw")
        "draw"
        self.nextToken()
        if self.curToken.type != tokenType.LEFT_PAREN:
            self.abort("Expected left paren for draw statement")
        self.nextToken()
        for i in range(3):
            self.expression()
        if self.curToken.type != tokenType.RIGHT_PAREN:
            self.abort("Expected right paren for draw statement, (draw takes exactly 3 params)")
        self.nextToken()
        if self.curToken.type != tokenType.NEWLINE:
            self.abort("Expected newline after draw")
        self.NL()
        


    
            
            

    def abort(self, message):
        sys.exit("Parser Error: "+message+" : line " + str(self.line))