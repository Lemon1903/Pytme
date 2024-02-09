from enum import Enum, auto


class Token(Enum):
    """An enum class for defining Tokens and accessed through its attributes.

    It is accessed as:  Token.<token name>

    Returns:
        __str__: name of token.
    """

    # Token type List:
    #   Format: <State Name> = auto()
    #   Legend:
    #      <State Name> = name of state
    #      auto()       = built in function of enum used for auto-count instead
    #                     of manually defining each state attribute by counting.
    IDENTIFIER = auto()
    KEYWORD = auto()

    RESERVEWORD = auto()
    NOISEWORD = auto()
    COMMENT = auto()

    #   Delmiters:
    BOXLEFT = auto()
    #   [
    BOXRIGHT = auto()
    #   ]

    PARENLEFT = auto()
    #   (
    PARENRIGHT = auto()
    #   )

    CURLYL = auto()
    #   {
    CURLYR = auto()
    #   }

    SEMICOLON = auto()
    #   ;

    # SINGLECOMMENTLEFT = auto(); #   //
    # MULTICOMMENTLEFT = auto();  #   /*
    # MULTICOMMENTRIGHT = auto(); #   */

    #   Arithmetic Operators
    ADD = auto()
    #   +
    SUBTRACT = auto()
    #   -
    MULTIPLY = auto()
    #   *
    DIVIDE = auto()
    #   /
    MODULO = auto()
    #   %
    EXPONENT = auto()
    #   **
    DIVFLOOR = auto()
    #   /_

    #   Boolean Operators
    GREAT = auto()
    #   >
    LESS = auto()
    #   <
    GREATQ = auto()
    #   <=
    LESSEQ = auto()
    #   >=
    NOTEQUAL = auto()
    #   !=
    EQUAL = auto()
    #   ==
    AND = auto()
    #   &&
    OR = auto()
    #   ||
    NOT = auto()
    #   !

    #   Other Operators
    DOT = auto()
    #   .
    COMMA = auto()
    #   ,

    #   Assignment Operators
    ASSIGN = auto()
    #   =
    ASSIGNADD = auto()
    #   +=
    ASSIGNSUB = auto()
    #   -=
    ASSIGNMULT = auto()
    #   *=
    ASSIGNDIV = auto()
    #   /=
    ASSIGNMOD = auto()
    #   %=

    #   Unary Operators
    UNARYMINUS = auto()
    #   -
    INCREMENT = auto()
    #   ++
    DECREMENT = auto()
    #   --

    #   Constants
    STRING = auto()
    #    PARTY = auto();
    INTEGER = auto()
    #    POINT = auto();
    FLOAT = auto()
    #    FIGURE = auto();
    BOOLEAN = auto()
    #    TRUTH = auto();
    CHAR = auto()
    #    AVATAR = auto();

    # newline
    NEWLINE = auto()

    #   Not a valid Lexeme
    INVALID = auto()

    EOF = auto()

    def __str__(self):
        """Function called if state is used as string such as in print()"""
        return self.name


class State(Enum):
    """An enum class for defining States and accessed through its attributes.

    It is accessed as:  State.<state name>

    Each state has a unique set of actions and transitions given the conditions.

    Returns:
        __str__: name of state.
    """

    # State type List:
    #   Format: <State Name> = auto()
    #   Legend:
    #      <State Name> = name of state
    #      auto()       = built in function of enum used for auto-count instead
    #                     of manually defining each state attribute by counting.
    initialized = auto()
    activated = auto()

    character = auto()
    string = auto()
    number = auto()
    float = auto()
    comment = auto()
    space = auto()
    operator = auto()
    logicalOperator = auto()
    semicolon = auto()
    stringLiteral = auto()
    delimiter = auto()

    endOfLine = auto()
    endOfFile = auto()
    processed = auto()

    def __str__(self):
        """Function called if state is used as string such as in print()"""
        return self.name


class Lexer:
    """The Lexical Analyzer class.

    Attributes:
        state : the current State
        symbolTable [] : list containing all lexemes detected.
    """

    # Constructor
    def __init__(self):
        self.state = State.initialized
        # self.symbolTable = [];
        self.lexemeList = []

        self.lineNumber = 0
        self.keywordList = [
            "abyss",
            "absolute",
            "archane",
            "arsenal",
            "attempt",
            "awm",
            "breach",
            "cast",
            "chamber",
            "chunk",
            "avatar",
            "core",
            "do",
            "dispatch",
            "display",
            "else",
            "elseif",
            "enchant",
            "ephemeral",
            "enum",
            "expands",
            "false",
            "figure",
            "for",
            "hero",
            "if",
            "incantation",
            "instanceof",
            "lootbox",
            "midget",
            "pacify",
            "party",
            "persist",
            "point",
            "portal",
            "powerup",
            "plaza",
            "save",
            "shadow",
            "shield",
            "shoot",
            "shoots",
            "spawns",
            "stable",
            "supreme",
            "synchronized",
            "this",
            "true",
            "toggle ",
            "truth",
            "twin",
            "unarmed",
            "unstable",
            "while",
            "truth",
            "true",
            "false",
        ]

    def getTokenBeforeAppend(self, lexeme):
        """Get token based on lexeme and/or current state

        Args:
            lexeme (string): the lexeme used
        """
        token = "INVALID"
        if lexeme == "\n":
            token = Token.NEWLINE
        if self.state == State.character and lexeme.isalpha():
            token = Token.IDENTIFIER
        elif self.state == State.string:
            if lexeme in ["true", "false"]:
                token = Token.BOOLEAN
            elif lexeme in self.keywordList:
                token = Token.KEYWORD
            else:
                token = Token.IDENTIFIER

        elif self.state == State.number:
            token = Token.INTEGER
        elif self.state == State.float:
            token = Token.FLOAT
        elif self.state == State.comment:
            token = Token.COMMENT
        elif self.state == State.operator:
            if lexeme == "+":
                token = Token.ADD
            elif lexeme == "-":
                token = Token.SUBTRACT
            elif lexeme == "*":
                token = Token.MULTIPLY
            elif lexeme == "/":
                token = Token.DIVIDE
            elif lexeme == "%":
                token = Token.MODULO
            elif lexeme == "/_":
                token = Token.DIVFLOOR
            elif lexeme == ">":
                token = Token.GREAT
            elif lexeme == "<":
                token = Token.LESS
            elif lexeme == "==":
                token = Token.EQUAL
            elif lexeme == ">=":
                token = Token.GREATQ
            elif lexeme == "<=":
                token = Token.LESSEQ
            elif lexeme == "=":
                token = Token.ASSIGN
            elif lexeme == "+=":
                token = Token.ASSIGNADD
            elif lexeme == "-=":
                token = Token.ASSIGNSUB
            elif lexeme == "*=":
                token = Token.ASSIGNMULT
            elif lexeme == "/=":
                token = Token.ASSIGNDIV
            elif lexeme == "%=":
                token = Token.ASSIGNMOD
            # Assign Floor Div?

        elif self.state == State.logicalOperator:
            if lexeme == "&&":
                token = Token.AND
            elif lexeme == "||":
                token = Token.OR
            elif lexeme == "!":
                token = Token.NOT

        elif self.state == State.semicolon or lexeme == ";":
            token = Token.SEMICOLON

        elif lexeme == ",":
            token = Token.COMMA

        elif self.state == State.stringLiteral:
            token = Token.STRING

        # elif(self.state == State.delimiter):
        elif lexeme == "{":
            token = Token.CURLYL
        elif lexeme == "}":
            token = Token.CURLYR
        elif lexeme == "[":
            token = Token.BOXLEFT
        elif lexeme == "]":
            token = Token.BOXRIGHT
        elif lexeme == "(":
            token = Token.PARENLEFT
        elif lexeme == ")":
            token = Token.PARENRIGHT

        return token

    def processText(self, inputText):
        # TODO check if inputText is valid ===================
        global lexemeList
        operatorList = ["+", "-", "*", "/", "%", ">", "<", "!", "=", "."]
        logicalOpList = ["&", "|", "!"]

        lexemeList = []

        lexeme = ""

        # TODO
        # print(inputText);
        while self.state != State.endOfFile:
            inputLine = inputText[self.lineNumber]

            colNumber = 0

            # For multi-line
            if self.state == State.endOfLine:
                self.state = State.comment
                if lexeme == "":  # comment has ended
                    self.state = State.character
            else:
                self.state = State.character

            while self.state != State.endOfLine:
                charCurrent = inputLine[colNumber]

                # TODO Display Debug
                # if(charCurrent == '\n'):
                #    print('\\n'+" col: "+str(colNumber)+" - Lexeme:"+repr(lexeme)+"  linelen:"+str(len(inputLine)), end = "") #TODO
                # else:
                #    print(charCurrent+" col: "+str(colNumber)+" - Lexeme:"+repr(lexeme)+"  linelen:"+str(len(inputLine)), end = "") #TODO

                if self.state == State.space:
                    if charCurrent in operatorList:
                        if len(lexeme) > 0:  # true means the end of a lexeme
                            lexemeList.append(
                                [
                                    lexeme,
                                    self.lineNumber + 1,
                                    colNumber,
                                    self.getTokenBeforeAppend(lexeme),
                                ]
                            )  # add the lexeme to list
                            lexeme = ""  # clear lexeme
                        lexeme = lexeme + charCurrent
                        self.state = State.operator
                    elif charCurrent in logicalOpList:
                        if len(lexeme) > 0:  # true means the end of a lexeme
                            lexemeList.append(
                                [
                                    lexeme,
                                    self.lineNumber + 1,
                                    colNumber,
                                    self.getTokenBeforeAppend(lexeme),
                                ]
                            )  # add the lexeme to list
                            lexeme = ""  # clear lexeme
                        lexeme = lexeme + charCurrent
                        self.state = State.logicalOperator
                    elif charCurrent.isnumeric():
                        lexeme = lexeme + charCurrent
                        self.state = State.number
                    elif not charCurrent.isspace():
                        lexeme = lexeme + charCurrent
                        self.state = State.character
                    else:
                        pass
                        # do nothing if space

                elif self.state == State.semicolon:
                    lexemeList.append(
                        [
                            lexeme,
                            self.lineNumber + 1,
                            colNumber,
                            self.getTokenBeforeAppend(lexeme),
                        ]
                    )  # add the lexeme to list
                    lexeme = ""  # clear lexeme
                    lexeme = lexeme + charCurrent
                    if charCurrent in operatorList:
                        self.state = State.operator
                    elif charCurrent in logicalOpList:
                        self.state = State.logicalOperator
                    elif charCurrent.isnumeric():
                        self.state = State.number
                    elif charCurrent.isspace():
                        self.state = State.space
                    else:
                        self.state = State.character

                elif self.state == State.delimiter:
                    lexemeList.append(
                        [
                            lexeme,
                            self.lineNumber + 1,
                            colNumber,
                            self.getTokenBeforeAppend(lexeme),
                        ]
                    )  # add the lexeme to list
                    lexeme = ""  # clear lexeme
                    lexeme = lexeme + charCurrent
                    if charCurrent in operatorList:
                        self.state = State.operator
                    elif charCurrent in logicalOpList:
                        self.state = State.logicalOperator
                    elif charCurrent.isnumeric():
                        self.state = State.number
                    elif charCurrent.isspace():
                        self.state = State.space
                    else:
                        self.state = State.character

                elif self.state == State.string:
                    # identifier
                    # keyword
                    # noiseword
                    if charCurrent.isalpha() or charCurrent.isnumeric():
                        lexeme = lexeme + charCurrent
                    elif charCurrent.isspace():
                        lexemeList.append(
                            [
                                lexeme,
                                self.lineNumber + 1,
                                colNumber,
                                self.getTokenBeforeAppend(lexeme),
                            ]
                        )  # add the lexeme to list
                        lexeme = ""  # clear lexeme
                        self.state = State.space
                    elif charCurrent in operatorList:
                        if len(lexeme) > 0:  # true means the end of a lexeme
                            lexemeList.append(
                                [
                                    lexeme,
                                    self.lineNumber + 1,
                                    colNumber,
                                    self.getTokenBeforeAppend(lexeme),
                                ]
                            )  # add the lexeme to list
                            lexeme = ""  # clear lexeme
                        lexeme = lexeme + charCurrent
                        self.state = State.operator
                    elif charCurrent in logicalOpList:
                        if len(lexeme) > 0:  # true means the end of a lexeme
                            lexemeList.append(
                                [
                                    lexeme,
                                    self.lineNumber + 1,
                                    colNumber,
                                    self.getTokenBeforeAppend(lexeme),
                                ]
                            )  # add the lexeme to list
                            lexeme = ""  # clear lexeme
                        lexeme = lexeme + charCurrent
                        self.state = State.logicalOperator
                    else:
                        if len(lexeme) > 0:  # true means the end of a lexeme
                            lexemeList.append(
                                [
                                    lexeme,
                                    self.lineNumber + 1,
                                    colNumber,
                                    self.getTokenBeforeAppend(lexeme),
                                ]
                            )  # add the lexeme to list
                            lexeme = ""  # clear lexeme
                        lexeme = lexeme + charCurrent
                        self.state = State.character

                elif self.state == State.number:
                    if charCurrent.isnumeric():
                        lexeme = lexeme + charCurrent
                    elif charCurrent == ".":
                        lexeme = lexeme + charCurrent
                        self.state = State.float
                    elif charCurrent in operatorList:
                        if len(lexeme) > 0:  # true means the end of a lexeme
                            lexemeList.append(
                                [
                                    lexeme,
                                    self.lineNumber + 1,
                                    colNumber,
                                    self.getTokenBeforeAppend(lexeme),
                                ]
                            )  # add the lexeme to list
                            lexeme = ""  # clear lexeme
                        lexeme = lexeme + charCurrent
                        self.state = State.operator
                    elif charCurrent in logicalOpList:
                        if len(lexeme) > 0:  # true means the end of a lexeme
                            lexemeList.append(
                                [
                                    lexeme,
                                    self.lineNumber + 1,
                                    colNumber,
                                    self.getTokenBeforeAppend(lexeme),
                                ]
                            )  # add the lexeme to list
                            lexeme = ""  # clear lexeme
                        lexeme = lexeme + charCurrent
                        self.state = State.logicalOperator
                    else:
                        lexemeList.append(
                            [
                                lexeme,
                                self.lineNumber + 1,
                                colNumber,
                                self.getTokenBeforeAppend(lexeme),
                            ]
                        )  # add the lexeme to list
                        lexeme = ""  # clear lexeme
                        self.state = State.character

                elif self.state == State.float:
                    if charCurrent.isnumeric():
                        lexeme = lexeme + charCurrent
                    elif charCurrent in operatorList:
                        if len(lexeme) > 0:  # true means the end of a lexeme
                            lexemeList.append(
                                [
                                    lexeme,
                                    self.lineNumber + 1,
                                    colNumber,
                                    self.getTokenBeforeAppend(lexeme),
                                ]
                            )  # add the lexeme to list
                            lexeme = ""  # clear lexeme
                        lexeme = lexeme + charCurrent
                        self.state = State.operator
                    elif charCurrent in logicalOpList:
                        if len(lexeme) > 0:  # true means the end of a lexeme
                            lexemeList.append(
                                [
                                    lexeme,
                                    self.lineNumber + 1,
                                    colNumber,
                                    self.getTokenBeforeAppend(lexeme),
                                ]
                            )  # add the lexeme to list
                            lexeme = ""  # clear lexeme
                        lexeme = lexeme + charCurrent
                        self.state = State.logicalOperator
                    else:
                        lexemeList.append(
                            [
                                lexeme,
                                self.lineNumber + 1,
                                colNumber,
                                self.getTokenBeforeAppend(lexeme),
                            ]
                        )  # add the lexeme to list
                        lexeme = ""  # clear lexeme
                        self.state = State.character

                elif self.state == State.stringLiteral:
                    # escape character
                    if lexeme[0] == '"' or lexeme[0] == "'":  # if start is ' or "
                        lexeme = lexeme + charCurrent
                    if lexeme[0] == lexeme[-1]:  # if end
                        # TODO print("TRACER ROUND")
                        lexemeList.append(
                            [
                                lexeme,
                                self.lineNumber + 1,
                                colNumber,
                                self.getTokenBeforeAppend(lexeme),
                            ]
                        )  # add the lexeme to list
                        lexeme = ""  # clear lexeme
                        self.state = State.character

                elif self.state == State.comment:
                    if lexeme[0] + lexeme[1] == "//":  # if single comment
                        if charCurrent != "\n":  # if comment is not yet ending
                            lexeme = lexeme + charCurrent
                        else:  # Comment has ended
                            lexemeList.append(
                                [
                                    lexeme,
                                    self.lineNumber + 1,
                                    colNumber,
                                    self.getTokenBeforeAppend(lexeme),
                                ]
                            )  # add the lexeme to list
                            lexeme = ""  # clear lexeme
                            self.state = State.character

                    elif lexeme[0] + lexeme[1] == "/*":  # if multiline comment
                        if lexeme[-2] + lexeme[-1] == "*/":  # comment has ended
                            lexemeList.append(
                                [
                                    lexeme,
                                    self.lineNumber + 1,
                                    colNumber,
                                    self.getTokenBeforeAppend(lexeme),
                                ]
                            )  # add the lexeme to list
                            lexeme = ""  # clear lexeme
                            self.state = State.character
                        else:
                            lexeme = lexeme + charCurrent

                elif self.state == State.operator:
                    # dot operator
                    if lexeme in ["+", "-", "*", "/", "%"]:
                        if charCurrent == "/" or charCurrent == "*":
                            lexeme = lexeme + charCurrent
                            self.state = State.comment
                        else:
                            if charCurrent == "=" or lexeme == "/" and charCurrent == "_":
                                lexeme = lexeme + charCurrent
                            lexemeList.append(
                                [
                                    lexeme,
                                    self.lineNumber + 1,
                                    colNumber,
                                    self.getTokenBeforeAppend(lexeme),
                                ]
                            )  # add the lexeme to list
                            lexeme = ""  # clear lexeme
                            self.state = State.character

                    elif charCurrent == ".":  # if new operator
                        lexemeList.append(
                            [
                                lexeme,
                                self.lineNumber + 1,
                                colNumber,
                                self.getTokenBeforeAppend(lexeme),
                            ]
                        )  # add the lexeme to list
                        lexeme = ""  # clear lexeme
                        lexeme = lexeme + charCurrent
                        # dot operator
                        self.state = State.operator

                    elif lexeme == "." and charCurrent.isnumeric():
                        lexeme = lexeme + charCurrent
                        self.state = State.float
                    elif charCurrent.isspace():
                        lexemeList.append(
                            [
                                lexeme,
                                self.lineNumber + 1,
                                colNumber,
                                self.getTokenBeforeAppend(lexeme),
                            ]
                        )  # add the lexeme to list
                        lexeme = ""  # clear lexeme
                        self.state = State.space
                    elif len(lexeme) > 0:  # true means the end of a lexeme
                        lexemeList.append(
                            [
                                lexeme,
                                self.lineNumber + 1,
                                colNumber,
                                self.getTokenBeforeAppend(lexeme),
                            ]
                        )  # add the lexeme to list
                        lexeme = ""  # clear lexeme
                        self.state = State.character

                elif self.state == State.logicalOperator:
                    if lexeme == "!":
                        lexemeList.append(
                            [
                                lexeme,
                                self.lineNumber + 1,
                                colNumber,
                                self.getTokenBeforeAppend(lexeme),
                            ]
                        )  # add the lexeme to list
                        lexeme = ""  # clear lexeme
                        lexeme = lexeme + charCurrent
                    elif charCurrent == lexeme:
                        lexeme = lexeme + charCurrent
                        lexemeList.append(
                            [
                                lexeme,
                                self.lineNumber + 1,
                                colNumber,
                                self.getTokenBeforeAppend(lexeme),
                            ]
                        )  # add the lexeme to list
                        lexeme = ""  # clear lexeme
                    elif charCurrent in operatorList:
                        if len(lexeme) > 0:  # true means the end of a lexeme
                            lexemeList.append(
                                [
                                    lexeme,
                                    self.lineNumber + 1,
                                    colNumber,
                                    self.getTokenBeforeAppend(lexeme),
                                ]
                            )  # add the lexeme to list
                            lexeme = ""  # clear lexeme
                        lexeme = lexeme + charCurrent
                        self.state = State.operator
                    else:
                        lexemeList.append(
                            [
                                lexeme,
                                self.lineNumber + 1,
                                colNumber,
                                self.getTokenBeforeAppend(lexeme),
                            ]
                        )  # add the lexeme to list
                        lexeme = ""  # clear lexeme
                        lexeme = lexeme + charCurrent
                    self.state = State.character

                elif self.state == State.character:
                    if lexeme == "'" or lexeme == '"' or charCurrent == "'" or charCurrent == '"':
                        if len(lexeme) > 0 and not (lexeme == "'" or lexeme == '"'):  # true means the end of a lexeme
                            lexemeList.append(
                                [
                                    lexeme,
                                    self.lineNumber + 1,
                                    colNumber,
                                    self.getTokenBeforeAppend(lexeme),
                                ]
                            )  # add the lexeme to list
                            lexeme = ""  # clear lexeme
                        lexeme = lexeme + charCurrent
                        self.state = State.stringLiteral

                    elif charCurrent == ";":
                        if len(lexeme) > 0:  # true means the end of a lexeme
                            lexemeList.append(
                                [
                                    lexeme,
                                    self.lineNumber + 1,
                                    colNumber,
                                    self.getTokenBeforeAppend(lexeme),
                                ]
                            )  # add the lexeme to list
                            lexeme = ""  # clear lexeme
                        lexeme = lexeme + charCurrent
                        self.state = State.semicolon

                    elif charCurrent in ["{", "}", "(", ")", "[", "]"]:
                        if len(lexeme) > 0:  # true means the end of a lexeme
                            lexemeList.append(
                                [
                                    lexeme,
                                    self.lineNumber + 1,
                                    colNumber,
                                    self.getTokenBeforeAppend(lexeme),
                                ]
                            )  # add the lexeme to list
                            lexeme = ""  # clear lexeme
                        lexeme = lexeme + charCurrent
                        self.state = State.delimiter

                    elif charCurrent in operatorList:
                        if len(lexeme) > 0:  # true means the end of a lexeme
                            lexemeList.append(
                                [
                                    lexeme,
                                    self.lineNumber + 1,
                                    colNumber,
                                    self.getTokenBeforeAppend(lexeme),
                                ]
                            )  # add the lexeme to list
                            lexeme = ""  # clear lexeme
                        lexeme = lexeme + charCurrent
                        self.state = State.operator

                    elif charCurrent in logicalOpList:
                        if len(lexeme) > 0:  # true means the end of a lexeme
                            lexemeList.append(
                                [
                                    lexeme,
                                    self.lineNumber + 1,
                                    colNumber,
                                    self.getTokenBeforeAppend(lexeme),
                                ]
                            )  # add the lexeme to list
                            lexeme = ""  # clear lexeme
                        lexeme = lexeme + charCurrent
                        self.state = State.logicalOperator

                    elif charCurrent.isnumeric():  # if char is  number
                        if len(lexeme) > 0:  # true means the end of a lexeme
                            lexemeList.append(
                                [
                                    lexeme,
                                    self.lineNumber + 1,
                                    colNumber,
                                    self.getTokenBeforeAppend(lexeme),
                                ]
                            )  # add the lexeme to list
                            lexeme = ""  # clear lexeme
                        lexeme = lexeme + charCurrent
                        self.state = State.number

                    elif charCurrent.isalpha():
                        lexeme = lexeme + charCurrent
                        if lexeme.isalpha():
                            self.state = State.string

                    elif charCurrent.isspace():
                        if len(lexeme) > 0:  # true means the end of a lexeme
                            lexemeList.append(
                                [
                                    lexeme,
                                    self.lineNumber + 1,
                                    colNumber,
                                    self.getTokenBeforeAppend(lexeme),
                                ]
                            )  # add the lexeme to list
                            lexeme = ""  # clear lexeme
                        # else means nothing to append
                        self.state = State.space

                    else:
                        lexeme = lexeme + charCurrent

                # if(charCurrent == '\n'):
                if colNumber + 1 >= len(inputLine):
                    if self.state == State.comment and lexeme[0] + lexeme[1] == "/*":  # Multiline Comment
                        pass
                    elif len(lexeme) > 0:  # true means the end of a lexeme
                        lexemeList.append(
                            [
                                lexeme,
                                self.lineNumber + 1,
                                colNumber,
                                self.getTokenBeforeAppend(lexeme),
                            ]
                        )  # add the lexeme to list
                        lexeme = ""  # clear lexeme
                    self.state = State.endOfLine

                colNumber += 1

                # TODO DISPLAY
                # print(" ", self.state);

                # if (text in self.keywordList):
                #    token = KEYWORD.

            if self.lineNumber + 1 >= len(inputText):
                self.state = State.endOfFile
            else:
                self.lineNumber += 1

        # for i in inputText:
        #    print(i, end="");
        lexemeList.append(
            [
                "",
                0,
                0,
                Token.EOF,
            ]
        )
        self.lexemeList = lexemeList

        self.state = State.activated

    def getOutput(self):

        output = "TOKEN                LINE#  COL#  \tLEXEME\n"
        output = output + "=========================================================\n"
        for i in self.lexemeList:
            a, b, c, d = i
            # a = Token
            # b = Line
            # c = Col
            # d = Lexeme
            # print(i);
            output = output + (
                f"{repr(str(d)):20}"
                + " "
                + f"{repr(str(b)):3}"
                + "   "
                + f"{repr(str(c)):3}"
                + "   \t"
                + repr(str(a))
                + "\n"
            )
        return output
