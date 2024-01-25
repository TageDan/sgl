import enum
import sys
from typing import Any

class tokenType(enum.Enum):
    #Symbols
    PLUS = 0
    MINUS = 1
    MULTIPLY = 2
    DIVIDE = 3
    EQ = 18
    EQEQ = 4
    NOTEQ = 5
    LESS_EQ = 6
    GREAT_EQ = 7
    LESS = 8
    GREAT = 9
    LEFT_PAREN = 10
    RIGHT_PAREN = 11
    LEFT_SQUIG = 12
    RIGHT_SQUIG = 13
    NEWLINE = 14
    MOD = 15
    LEFT_SQUARE = 16
    RIGHT_SQUARE = 17
    EXP = 19

    #Types
    NUMBER = 100
    NAME = 101
    STRING = 102
    SECTION = 103
    
    #Keywords
    IF = 200
    # WHILE = 201
    LET = 202
    DRAW = 203
    CLEAR = 204
    LOOP = 205
    BREAK = 206
    PUSH = 207
    PRINT = 208
    SHOW = 211
    DRAWFILL = 212

class Token:
    def __init__(self, type: tokenType, literal):
        self.type = type
        self.literal = literal

    def __str__(self):
        return self.type.name + " | " + self.literal

class Lexer:

    def __init__(self, filePath):
        with open(filePath, "r") as source:
            self.source = source.read() + "\n"
        self.curChar = ""
        self.curPos = -1
        self.nextChar()
    
    def nextChar(self):
        self.curPos += 1
        self.curChar = self.source[self.curPos]
    
    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos + 1]

    def skipWhitespace(self):
        while self.curChar == " " or self.curChar== "\r" or self.curChar=="\t":
            self.nextChar()

    def getToken(self):
        self.skipWhitespace()
        if self.curChar == "+":
            token = Token(tokenType.PLUS, "+")
        elif self.curChar == "-":
            token = Token(tokenType.MINUS, "-")
        elif self.curChar == "*":
            if self.peek() == "*":
                self.nextChar()
                token = Token(tokenType.EXP, "**")
            else:
                token = Token(tokenType.MULTIPLY, "*")
            
        elif self.curChar == "/":
            token = Token(tokenType.DIVIDE, "/")
        elif self.curChar == "%":
            token = Token(tokenType.MOD, "%")
        elif self.curChar == "(":
            token = Token(tokenType.LEFT_PAREN, "(")
        elif self.curChar == "{":
            token = Token(tokenType.LEFT_SQUIG, "{")
        elif self.curChar == ")":
            token = Token(tokenType.RIGHT_PAREN, ")")
        elif self.curChar == "}":
            token = Token(tokenType.RIGHT_SQUIG, "}")
        elif self.curChar == "=":
            if self.peek() == "=":
                token = Token(tokenType.EQEQ, "==")
                self.nextChar()
            else:
                token = Token(tokenType.EQ, "=")
        elif self.curChar == "!":
            if self.peek() != "=":
                self.abort("Excpected '=' after '!'")
            else:
                self.nextChar()
                token = Token(tokenType.NOTEQ, "!=")
        elif self.curChar == ">":
            if self.peek() == "=":
                token = Token(tokenType.GREAT_EQ, ">=")
                self.nextChar()
            else:
                token = Token(tokenType.GREAT, ">")
        elif self.curChar == "<":
            if self.peek() == "=":
                token = Token(tokenType.LESS_EQ, "<=")
                self.nextChar()
            else:
                token = Token(tokenType.LESS, "<")
        elif self.curChar.isdigit():
            literal = self.curChar
            point = False
            while self.peek().isdigit() or (self.peek() == "." and not point):
                self.nextChar()
                literal += self.curChar
                if self.curChar == ".":
                    if not self.peek().isdigit():
                        self.abort("expected digits after decimal point")
                    point == True
            token = Token(tokenType.NUMBER, literal)
        elif self.curChar.isalpha():
            literal = self.curChar
            while self.peek().isalnum() or self.peek() == "_":
                self.nextChar()
                literal += self.curChar
            
            token = Token(tokenType.NAME, literal)
            for type in tokenType:
                if type.name == literal.upper() and literal.islower() and type.value > 199:
                    token = Token(type, literal)
        elif self.curChar == "[":
            token = Token(tokenType.LEFT_SQUARE, "[")
        elif self.curChar == "]":
            token = Token(tokenType.RIGHT_SQUARE, "]")
        elif self.curChar == "\n":
            token = Token(tokenType.NEWLINE, "\n")
        elif self.curChar == "#":
            literal = ""
            while self.peek() != "#":
                self.nextChar()
                literal += self.curChar
            self.nextChar()
            token = Token(tokenType.SECTION, literal)

        else:
            self.abort("Unkown token: "+ self.curChar)
        
        self.nextChar()
        return token
    
    def tokenize(self):
        result = []
        while self.peek() != "\0":
            result.append(self.getToken())
        return result
            

    def abort(self, message):
        sys.exit("Lexing error. " + message)



    
