import os
from Lexer import Token


class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.index = 0

    # Helper methods
    def get_lexeme(self):
        return self.tokens[self.index][0]

    def get_line_no(self):
        return self.tokens[self.index][1]

    def get_column_no(self):
        return self.tokens[self.index][2]

    def get_token(self):
        return self.tokens[self.index][3]

    def consume(self, token: Token | None = None):
        # just advance to the next token
        if token is None:
            self.index += 1
            return True

        # if true, move to the next token
        if self.index < len(self.tokens) and self.get_token() == token:
            self.index += 1
            return True
        return False

    def print_error(self, message):
        # raise Exception(f"Syntax Error at line {self.get_line_no()} column {self.get_column_no()}: {message}")
        print(f"Syntax Error at line {self.get_line_no()} column {self.get_column_no()}: {message}")
        os._exit(1)

    # end of helper methods

    # expression
    def expression(self):
        self.and_expression()
        while self.consume(Token.OR):
            self.and_expression()

    def and_expression(self):
        self.not_expression()
        if self.consume(Token.AND):
            self.not_expression()

    def not_expression(self):
        self.consume(Token.NOT)
        self.comparison()

    def comparison(self):
        comp_ops = [
            Token.LESS,
            Token.GREAT,
            Token.EQUAL,
            Token.NOTEQUAL,
            Token.GREATQ,
            Token.LESSEQ,
        ]
        self.add_subtract()
        # if there are multiple comparisons
        while self.get_token() in comp_ops:
            self.consume()
            self.add_subtract()

    def add_subtract(self):
        self.multiply_div_mod()
        while self.get_token() in [Token.ADD, Token.SUBTRACT]:
            self.consume()
            self.multiply_div_mod()

    def multiply_div_mod(self):
        self.value()
        while self.get_token() in [Token.MULTIPLY, Token.DIVIDE, Token.MODULO]:
            self.consume()
            self.value()

    def value(self):
        token = self.get_token()
        if token in [
            Token.IDENTIFIER,
            Token.INTEGER,
            Token.FLOAT,
            Token.STRING,
            Token.BOOLEAN,
        ]:
            self.consume()
        # expression
        elif self.consume(Token.PARENLEFT):
            self.expression()
            if not self.consume(Token.PARENRIGHT):
                self.print_error("Expected closing parenthesis ')' after the expression")
        else:
            self.print_error(f"Invalid value '{self.get_lexeme()}'")
            os._exit(1)

    # end expression

    def output_statement(self):
        self.consume(Token.KEYWORD)
        if not self.consume(Token.PARENLEFT):
            self.print_error("Expected '(' after the 'display' keyword")

        # execute the optional expression inside display function
        if self.get_token() != Token.PARENRIGHT:
            self.expression()

        if not self.consume(Token.PARENRIGHT):
            self.print_error("Expected ')' after the expression")

    def in_statement(self):
        if not self.get_lexeme() == "input":
            self.print_error("Expected 'input' keyword after the identifier")
        self.consume()

        if not self.consume(Token.PARENLEFT):
            self.print_error("Expected '(' after the 'display' keyword")

        if not self.consume(Token.PARENRIGHT):
            self.print_error("Expected ')' after the expression")

    def ass_statement(self):
        ass_ops = [Token.ASSIGNADD, Token.ASSIGNDIV, Token.ASSIGNMOD, Token.ASSIGNMULT, Token.ASSIGNSUB]
        if self.get_token() not in ass_ops + [Token.ASSIGN]:
            self.print_error("Available assignment operators are (=, +=, -=, *=, /=. %=)")

        if self.consume(Token.ASSIGN):
            if self.get_lexeme() == "input":
                self.in_statement()
                return
        elif self.get_token() in ass_ops:
            self.consume()

        self.expression()

    def call_statement(self):
        self.consume(Token.PARENLEFT)

        # optional arguments
        while self.get_token() != Token.PARENRIGHT:
            self.expression()
            if not self.consume(Token.COMMA):
                break

        if not self.consume(Token.PARENRIGHT):
            self.print_error("Expected ')' after the function name")

    def dec_statement(self):
        # optional assignment declaration
        if self.consume(Token.ASSIGN):
            # input statement found
            if self.get_lexeme() == "input":
                self.in_statement()
                return
            self.expression()

        # more identifiers
        while self.consume(Token.COMMA):
            if not self.consume(Token.IDENTIFIER):
                self.print_error("Expected identifier after the comma")

            # optional assignment declaration
            if self.consume(Token.ASSIGN):
                self.expression()

    def simple_statement(self):
        if self.get_token() in [Token.ASSIGN, Token.COMMA]:
            self.dec_statement()
        elif self.get_lexeme() == "display":
            self.output_statement()
        elif self.get_lexeme() == "dispatch":
            self.consume(Token.KEYWORD)
            self.expression()
        else:
            self.consume(Token.IDENTIFIER)
            if self.get_token() == Token.PARENLEFT:
                self.call_statement()
            else:
                self.ass_statement()

        if not self.consume(Token.SEMICOLON):
            self.print_error("Expected semicolon after the statement")
        self.consume(Token.NEWLINE)

    def if_statement(self):
        # if statement
        self.consume(Token.KEYWORD)
        if not self.consume(Token.PARENLEFT):
            self.print_error("Expected '(' after the 'if' keyword")

        self.expression()
        if not self.consume(Token.PARENRIGHT):
            self.print_error("Expected ')' after the expression")
        self.consume(Token.NEWLINE)

        if not self.consume(Token.CURLYL):
            self.print_error("Expected opening curly brace '{' after the expression")

        while self.get_token() != Token.CURLYR:
            self.consume(Token.NEWLINE)
            self.statement()

        if not self.consume(Token.CURLYR):
            self.print_error("Expected closing curly brace '}' after the statement")
        self.consume(Token.NEWLINE)

        # optional zero or more elseif statements
        while self.get_lexeme() == "elseif":
            self.consume(Token.KEYWORD)
            if not self.consume(Token.PARENLEFT):
                self.print_error("Expected '(' after the 'elseif' keyword")

            self.expression()
            if not self.consume(Token.PARENRIGHT):
                self.print_error("Expected ')' after the expression")
            self.consume(Token.NEWLINE)

            if not self.consume(Token.CURLYL):
                self.print_error("Expected opening curly brace '{' after the expression")

            while self.get_token() != Token.CURLYR:
                self.consume(Token.NEWLINE)
                self.statement()

            if not self.consume(Token.CURLYR):
                self.print_error("Expected closing curly brace '}' after the statement")
            self.consume(Token.NEWLINE)

        # optional else statement
        if self.get_lexeme() == "else":
            self.consume(Token.KEYWORD)
            if not self.consume(Token.CURLYL):
                self.print_error("Expected opening curly brace '{' after the 'else' keyword")

            while self.get_token() != Token.CURLYR:
                self.consume(Token.NEWLINE)
                self.statement()

            if not self.consume(Token.CURLYR):
                self.print_error("Expected closing curly brace '}' after the statement")
            self.consume(Token.NEWLINE)

    def for_statement(self):
        self.consume(Token.KEYWORD)
        if not self.consume(Token.PARENLEFT):
            self.print_error("Expected '(' after the 'for' keyword")

        if not self.get_lexeme() == "point":
            self.print_error("Expected data type for initialization of the variable in the for loop")
        self.consume(Token.KEYWORD)

        # initialize the variable
        identifier = self.get_lexeme()
        if not self.consume(Token.IDENTIFIER):
            self.print_error("Expected identifier after the data type")
        if not self.consume(Token.ASSIGN):
            self.print_error("Expected '=' after the identifier")
        if not self.consume(Token.INTEGER):
            self.print_error(f"Expected integer value for variable {identifier}")
        if not self.consume(Token.SEMICOLON):
            self.print_error("Expected semicolon after the initialization")

        # condition
        self.expression()
        if not self.consume(Token.SEMICOLON):
            self.print_error("Expected semicolon after the condition")

        # increment
        if not self.consume(Token.IDENTIFIER):
            self.print_error(f"Expected the variable {identifier} for increment")
        if not self.consume(Token.ADD):
            self.print_error(f"Expected '++' unary for increment after the variable {identifier}")

        if not self.consume(Token.PARENRIGHT):
            self.print_error("Expected closing ')' of the loop condition")
        self.consume(Token.NEWLINE)

        if not self.consume(Token.CURLYL):
            self.print_error("Expected opening curly brace '{' after the loop condition")

        while self.get_token() != Token.CURLYR:
            self.consume(Token.NEWLINE)
            self.statement()

        if not self.consume(Token.CURLYR):
            self.print_error("Expected closing curly brace '}' after the statement")

    def while_statement(self):
        self.consume(Token.KEYWORD)
        if not self.consume(Token.PARENLEFT):
            self.print_error("Expected '(' after the 'for' keyword")

        self.expression()
        if not self.consume(Token.PARENRIGHT):
            self.print_error("Expected ')' after the expression")
        self.consume(Token.NEWLINE)

        if not self.consume(Token.CURLYL):
            self.print_error("Expected opening curly brace '{' after the loop condition")

        while self.get_token() != Token.CURLYR:
            self.consume(Token.NEWLINE)
            self.statement()

        if not self.consume(Token.CURLYR):
            self.print_error("Expected closing curly brace '}' after the statement")

    def do_while_statement(self):
        self.consume(Token.KEYWORD)
        if not self.consume(Token.CURLYL):
            self.print_error("Expected opening curly brace '{' after the loop condition")

        while self.get_token() != Token.CURLYR:
            self.consume(Token.NEWLINE)
            self.statement()

        if not self.consume(Token.CURLYR):
            self.print_error("Expected closing curly brace '}' after the statement")

        if self.get_lexeme != "while" and not self.consume(Token.KEYWORD):
            self.print_error("Expected 'while' keyword after the statement")

        if not self.consume(Token.PARENLEFT):
            self.print_error("Expected '(' after the 'for' keyword")

        self.expression()
        if not self.consume(Token.PARENRIGHT):
            self.print_error("Expected ')' after the expression")

        if not self.consume(Token.SEMICOLON):
            self.print_error("Expected semicolon after the statement")

    def function_statement(self):
        if not self.consume(Token.PARENLEFT):
            self.print_error("Expected '(' after the function name")

        # optional parameters
        data_types = ["point", "party", "truth", "avatar", "figure"]
        while self.get_token() != Token.PARENRIGHT:
            if self.get_lexeme() not in data_types:
                self.print_error("Expected data type for the function parameter")
            self.consume(Token.KEYWORD)
            if not self.consume(Token.IDENTIFIER):
                self.print_error("Expected identifier after the data type")
            if not self.consume(Token.COMMA):
                break

        if not self.consume(Token.PARENRIGHT):
            self.print_error("Expected closing ')' after the function name")

        # function body
        if not self.consume(Token.CURLYL):
            self.print_error("Expected opening curly brace '{' after the function name")

        while self.get_token() != Token.CURLYR:
            self.consume(Token.NEWLINE)
            self.statement()

        if not self.consume(Token.CURLYR):
            self.print_error("Expected closing curly brace '}' after the statement")
        self.consume(Token.NEWLINE)

    def compound_statement(self):
        lexeme = self.get_lexeme()
        if lexeme == "if":
            self.if_statement()
        elif lexeme == "for":
            self.for_statement()
        elif lexeme == "while":
            self.while_statement()
        elif lexeme == "do":
            self.do_while_statement()

    def statement(self):
        lexeme = self.get_lexeme()
        data_types = ["point", "party", "truth", "avatar", "figure", "abyss"]
        modifiers = ["plaza", "incantation", "absolute"]

        if lexeme in ["display", "dispatch"] or self.get_token() == Token.IDENTIFIER:
            self.simple_statement()
            return

        if lexeme in ["if", "for", "while", "do"]:
            self.compound_statement()
        # data type begins
        elif lexeme in data_types:
            # consume data type
            self.consume(Token.KEYWORD)
            if not self.consume(Token.IDENTIFIER):
                self.print_error("Expected identifier after the data type or return type")
            if self.get_token() in [Token.ASSIGN, Token.COMMA]:
                self.simple_statement()
            elif self.get_token() == Token.PARENLEFT:
                self.function_statement()
            else:
                self.print_error("Invalid statement")
        elif lexeme in modifiers:
            # consume data type
            self.consume(Token.KEYWORD)
            if self.get_lexeme() in data_types:
                # consume data type
                self.consume(Token.KEYWORD)
                if not self.consume(Token.IDENTIFIER):
                    self.print_error("Expected identifier after the data type or return type")
                if self.get_token() in [Token.ASSIGN, Token.COMMA]:
                    self.simple_statement()
                elif self.get_token() == Token.PARENLEFT:
                    self.function_statement()
                else:
                    self.print_error("Invalid statement")
            else:
                self.print_error("Invalid statement")
        else:
            self.print_error("Statements should start with a keyword or an identifier")

    def pytme_pl(self):
        while self.get_token() != Token.EOF:
            self.statement()
            self.consume(Token.NEWLINE)

    def parse(self):
        self.pytme_pl()
        print("Parsing successful")
