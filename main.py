from lexer import Lexer
from parserr import Parser
from smtbuilder import SMTbuilder
import os, sys, unittest

file = open(sys.argv[1],"r")
data = file.readlines()
file.close()

currentline = 1

for lines in data:
    lexerlist = Lexer(lines.rstrip()).tokenize(currentline)
    parserlist = Parser().parse(lexerlist)

    if not "Syntax Error" in parserlist: # no grammar error found
        SMTbuilder("output.py").build(lexerlist)
        import output
    else:
        print parserlist # prints error

    currentline += 1

class Test(unittest.TestCase):
    def test1(self):
        lexerlist = Lexer('Q').tokenize(1)
        self.assertEqual(lexerlist[0].kind, "ID")
        self.assertEqual(lexerlist[0].loc.col, 1)
        self.assertEqual(lexerlist[0].loc.line, 1)

    def test2(self):
        lexerlist = Lexer('Q').tokenize(1)
        parserlist = Parser().parse(lexerlist)
        self.assertEqual(parserlist[0].kind, "propositions")
        self.assertEqual(parserlist[1].kind, "proposition")
        self.assertEqual(parserlist[2].kind, "atomic")
        self.assertEqual(parserlist[3].kind, "ID")
        self.assertEqual(parserlist[4].kind, "more-proposition")
        self.assertEqual(parserlist[5].kind, "epsilon")

    def test3(self):
        lexerlist = Lexer('Q').tokenize(1)
        SMTbuilder("testoutput.py").build(lexerlist)
        file = open("testoutput.py","r")
        data = file.readlines()
        file.close()
        os.remove("testoutput.py")

        self.assertEqual(data[0].rstrip(), "from pysmt.shortcuts import Symbol, And, Or, Not, Iff, Implies, is_sat")
        self.assertEqual(data[2].rstrip(), "Q = Symbol(\"Q\")")
        self.assertEqual(data[3].rstrip(), "prop1 = Q")
        self.assertEqual(data[4].rstrip(), "f = prop1")
        self.assertEqual(data[5].rstrip(), "print is_sat(f)")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        sys.argv.pop()
    unittest.main()