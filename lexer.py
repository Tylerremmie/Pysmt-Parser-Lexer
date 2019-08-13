
import string

class Location:
    def __init__(self, line, col):
        self.line = line
        self.col = col

class TokenKind:
    ID = 0      # identifier
    LPAR = 1    # (
    RPAR = 2    # )
    NOT = 3     # !
    AND = 4     # /\
    OR = 5      # \/
    IMPLIES = 6 # =>
    IFF = 7     # <=>
    COMMA = 8   # ,


def match(symbol):
    tokens = [
        ('(', 'LPAR'),
        (')', 'RPAR'),
        ('!', 'NOT'),
        ('/\\', 'AND'),
        ('\\/', 'OR'),
        ('=>', 'IMPLIES'),
        ('<=>', 'IFF'),
        (',', 'COMMA')
    ]
    for token in tokens:
        if symbol == token[0]:
            return token[1]

class Token:
    def __init__(self, loc, kind):
        self.loc = loc
        self.kind = kind
        self.value = None

    def __str__(self):
       return str(self.kind)

    def __repr__(self):
        return str(self.kind)

class Lexer:
    def __init__(self, text):
        self.text = text

    def tokenize(self, line):
        pos = 0
        col = 1
        tokenbuilder = ''
        tokens = []
        while pos < len(self.text):

            # SPACE WAS FOUND - ADVANCE TOKENS FORWARD
            if self.text[pos] == " ":
                pos += 1

            # CHECKS FOR ID
            if self.text[pos].isalnum():
                value = self.text[pos]
                while(self.text[pos].isalnum() and pos < len(self.text) - 1):
                    pos +=1
                tokens.append(Token(Location(line,col), "ID"))
                tokens[-1].value = value
                col += 1

            # BUILD TOKENS FROM CHARACTERS
            if self.text[pos] == '/':
                tokenbuilder = tokenbuilder + self.text[pos]
            if self.text[pos] == '\\':
                tokenbuilder = tokenbuilder + self.text[pos]
            if self.text[pos] == '=':
                tokenbuilder = tokenbuilder + self.text[pos]
            if self.text[pos] == '<':
                tokenbuilder = tokenbuilder + self.text[pos]
            if self.text[pos] == '>':
                tokenbuilder = tokenbuilder + self.text[pos]

            # CHECK IF TOKEN IS BUILT FULLY
            if tokenbuilder == "\\/" or tokenbuilder == "/\\" or tokenbuilder == "=>" or tokenbuilder == "<=>" or tokenbuilder == "=>" or tokenbuilder == "<=>":
                tokenmatch = match(tokenbuilder)
                tokenbuilder = ''
                if tokenmatch:
                    tokens.append(Token(Location(line,col), tokenmatch))
                    col += 1
            # SEND SINGLE TOKENS
            else:
                tokenmatch = match(self.text[pos])
                if tokenmatch:
                    tokens.append(Token(Location(line,col), tokenmatch))
                    col += 1

            pos += 1

        return tokens