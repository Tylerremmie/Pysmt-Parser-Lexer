from lexer import Lexer, Location
import sys

class Grammar:
    def __init__(self, kind):
        self.kind = kind
        self.value = None
    
    def __repr__(self):
        return str(self.kind)

class Parser:
    def __init__(self):
        self.list = []
        self.tokens = []
        self.currentpos = 0
        self.eof = 0
        self.LPARS = 0
        self.RPARS = 0
        self.errorflag = 0
        self.errorloc = []

    def parse(self, tokenlist):
        self.tokens = tokenlist
        self.eof = (len(self.tokens)-1)
        self.propositions()
        self.checkErrors()
        if self.errorflag:
            return "Syntax Error at line " + self.errorloc[0] + " column " + self.errorloc[1] + "."
        else:
            return self.list

    def propositions(self):
        self.list.append(Grammar("propositions"))
        self.proposition()
        self.more_propositions()

    def more_propositions(self):
        self.list.append(Grammar("more-proposition"))
        if self.currentpos < self.eof:
            #self.checkPARS()
            self.list.append(Grammar("comma"))
            self.currentpos += 1 if self.currentpos < self.eof else 0
            self.propositions()
        else:
            self.list.append(Grammar("epsilon"))

    def proposition(self):
        self.list.append(Grammar("proposition"))
        # Check for LPAR or NOT(!)
        peek = self.currentpos
        if self.tokens[self.currentpos].kind == "LPAR" or self.tokens[self.currentpos].kind == "NOT":
            self.compound()
        elif self.tokens[self.currentpos].kind == "ID":
            # Check for atomic connective (AND, OR, IFF, IMPLIES)
            if (peek + 1 <= len(self.tokens) - 1) and (self.tokens[peek + 1].kind == "AND" or self.tokens[peek + 1].kind == "OR" or self.tokens[peek + 1].kind == "IFF" or self.tokens[peek + 1].kind == "IMPLIES"):
                self.compound()
            # Normal atomic    
            else:
                self.atomic()

    def atomic(self):
        self.list.append(Grammar("atomic"))
        self.list.append(Grammar("ID"))
        self.list[-1].value = self.tokens[self.currentpos].value
        self.currentpos += 1 if self.currentpos < self.eof else 0

    def compound(self):
        self.list.append(Grammar("compound"))

        if self.tokens[self.currentpos].kind == "LPAR":
            self.list.append(Grammar("LPAR"))
            self.currentpos += 1 if self.currentpos < self.eof else 0
            self.proposition()
            self.list.append(Grammar("RPAR"))
            self.currentpos += 1 if self.currentpos < self.eof else 0
        
        elif self.tokens[self.currentpos].kind == "NOT":
            self.list.append(Grammar("NOT"))
            self.currentpos += 1 if self.currentpos < self.eof else 0
            self.proposition()

        else:
            self.atomic()
            self.connective()
            self.proposition()

    def connective(self):
        self.list.append(Grammar("connective"))
        
        if self.tokens[self.currentpos].kind == "AND":
            self.list.append(Grammar("AND"))
            self.currentpos += 1 if self.currentpos < self.eof else 0
        
        elif self.tokens[self.currentpos].kind == "OR":
            self.list.append(Grammar("OR"))
            self.currentpos += 1 if self.currentpos < self.eof else 0

        elif self.tokens[self.currentpos].kind == "IMPLIES":
            self.list.append(Grammar("IMPLIES"))
            self.currentpos += 1 if self.currentpos < self.eof else 0

        elif self.tokens[self.currentpos].kind == "IFF":
            self.list.append(Grammar("IFF"))
            self.currentpos += 1 if self.currentpos < self.eof else 0

    def checkErrors(self):
        errorpos = 0
        index = 0

        for token in self.tokens:
            
            # CHECKS FOR MISMATCHING PARS
            if token.kind == "LPAR":
                if self.LPARS == 0:
                    errorpos = index                
                self.LPARS += 1

            if token.kind == "RPAR":
                if self.LPARS > 0:
                    self.LPARS -= 1
                else:
                    errorpos = index
                    self.RPARS += 1
            
            # CHECKS FOR OUT OF PLACE COMMAS
            # Comma at beginning of list
            if token.kind == "COMMA" and index == 0:
                errorpos = index
                self.errorflag = 1
                self.errorloc = [str(self.tokens[errorpos].loc.line), str(self.tokens[errorpos].loc.col)]
                return
            
            # Comma following wrong token - error
            if token.kind == "COMMA" and index > 0:
                if self.tokens[index - 1].kind != "RPAR" and self.tokens[index - 1].kind != "ID":
                    errorpos = index
                    self.errorflag = 1
                    self.errorloc = [str(self.tokens[errorpos].loc.line), str(self.tokens[errorpos].loc.col)]
                    return
            # CHECKS CONNECTIVES
            if (token.kind == "AND" or token.kind == "OR" or token.kind == "IMPLIES" or token.kind == "IFF"):
                if(index < self.eof):
                    if (self.tokens[index + 1].kind != "ID" and self.tokens[index + 1].kind != "LPAR" and self.tokens[index + 1].kind != "NOT"):
                        errorpos = index + 1
                        self.errorflag = 1
                        self.errorloc = [str(self.tokens[errorpos].loc.line), str(self.tokens[errorpos].loc.col)]
                        return

                # Connective at end - Error
                if(index == self.eof) or (index == 0):
                    errorpos = index
                    self.errorflag = 1
                    self.errorloc = [str(self.tokens[errorpos].loc.line), str(self.tokens[errorpos].loc.col)]
                    return

            index += 1

        # PARENTHESIS ARE UNEQUAL
        if self.LPARS != self.RPARS:
            self.errorflag = 1
            self.errorloc = [str(self.tokens[errorpos].loc.line), str(self.tokens[errorpos].loc.col)]