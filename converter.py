from pysmt.shortcuts import Symbol

class Convert:
    def __init__(self, capacity):
        self.capacity = capacity
        self.propositionlist = []
        self.top = -1
        self.stack = []
        self.output = []

    def build(self, tokenlist):
        temp = []

        for token in tokenlist:
            if token.kind == "COMMA":
                self.propositionlist.append(temp)
                temp = []
            else:
                temp.append(token)

        self.propositionlist.append(temp)
        temp = []
    
        self.infixtopostfix()
        return self.propositionlist
        

    def isEmpty(self):
        return True if self.top == -1 else False

    def pop(self): 
        if not self.isEmpty(): 
            self.top -= 1
            return self.stack.pop() 
        else: 
            return "$"
    
    def push(self, op): 
        self.top += 1
        self.stack.append(op.kind) 

    def infixtopostfix(self):
        temp = []
        for proposition in self.propositionlist:
            for token in proposition:

                #if token is a symbol
                if token.kind == "ID":
                    self.output.append(token.value)

                #if token is a NOT
                elif token.kind == "NOT":
                    self.push(token)

                #if token is an LPAR
                elif token.kind == "LPAR":
                    None

                #if token is an RPAR
                elif token.kind == "RPAR":
                    None

                #token is a connective (AND, OR, IMPLIES, IFF)
                else:
                    while(not self.isEmpty()):
                        self.output.append(self.pop())
                    self.push(token)

            while not self.isEmpty(): 
                self.output.append(self.pop())
            
            temp.append(self.output)
            self.output = []
        
        self.propositionlist = temp