import sys
import os
from Lexer import Lexer
from Parser import Parser

# from Parser import Parser;

# print("Args:")
# print(sys.argv);

dir_path = os.path.dirname(os.path.realpath(__file__))
# Initialize path of the system


def loadFile(address):

    lexer = Lexer()

    with open(address, "r") as myfile:
        lines = myfile.readlines()

        lexer.processText(lines)
        print("LEXICAL ANALYSIS COMPLETE")

    with open("symboltable.txt", "w") as file:
        file.write(lexer.getOutput())
        print("symboltable.txt is written.")

    parser = Parser(lexer.lexemeList)
    parser.parse()


if sys.argv[1][-4] + (sys.argv[1][-3] + sys.argv[1][-2] + sys.argv[1][-1]).lower() == ".pyt":
    loadFile(sys.argv[1])
else:
    print("Invalid filetype")
# try:
# except:
#     print("No file found at address found")
