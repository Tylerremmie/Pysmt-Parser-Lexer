class SMTbuilder():
    def __init__(self, filename):
        self.symbollist = []
        self.propsholder = []
        self.propositioncounter = 0
        self.stringbuilder = ''
        self.file = open(filename, "w")

    def build(self, list):
        self.printImports()
        lists = self.splitList(list)

        for list in lists:
            stack = []

            self.propositioncounter += 1
            list.reverse()
            i = 0 #index
            for token in list:
                length = len(list)

                # Token is an ID
                if token.kind == "ID":
                    value = token.value

                    # only print each symbol once
                    if not value in self.symbollist:
                        self.symbollist.append(value)
                        self.file.write(str(value).upper() + " = Symbol(\"" + str(value).upper() + "\")\n")
                        
                    # peek for NOT and append Not(Token)
                    if(i < length - 1 and list[i + 1].kind == "NOT"):
                        stack.append("Not(" + token.value + ")")
                    
                    # append just the token
                    else:
                        stack.append(token.value)

                # Token is a NOT 
                elif token.kind == "NOT":
                    None

                # Token is a connective (And, Or, Iff, Implies)
                else:
                    if token.kind == "AND":
                        stack.append("And(")
                    elif token.kind == "OR":
                        stack.append("Or(")
                    elif token.kind == "IMPLIES":
                        stack.append("Implies(")
                    elif token.kind == "IFF":
                        stack.append("Iff(")
                    else:
                        None

                # check stack to see if build is possible
                if len(stack) >= 3:
                    #build
                    temp = stack[1] + stack[2] + ", " + stack[0] + ")"
                    stack.pop()
                    stack.pop()
                    stack.pop()
                    stack.append(temp)
                    
                i += 1 # keep track of index
            self.propsholder.append("prop" + str(self.propositioncounter))
            self.file.write(self.propsholder[-1] + " = " + stack.pop())
            self.file.write("\n")

        self.printIsSat()
         
    def printImports(self):
        self.file.write("from pysmt.shortcuts import Symbol, And, Or, Not, Iff, Implies, is_sat\n\n")

    def printIsSat(self):
        while len(self.propsholder) > 1:
            temp = "And(" + self.propsholder.pop() + ", " + self.propsholder.pop() + ")"
            self.propsholder.append(temp)

        self.file.write("f = " + self.propsholder.pop())
        self.file.write("\n")
        self.file.write("print is_sat(f)")
        
    def splitList(self, tokenlist):
        list = []
        temp = []

        for token in tokenlist:
            if token.kind == "COMMA":
                list.append(temp)
                temp = []
            else:
                temp.append(token)

        list.append(temp)
        temp = []
        return list