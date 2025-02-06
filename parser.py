class Token:
    # Let's define our basic token types
    INTEGER = 'INTEGER'
    STRING = "STRING"
    VALUE = 'VALUE'
    LESS_THAN = 'LESS_THAN'
    OPERATOR = "OPERATOR"
    IDENTIFIER = 'IDENTIFIER'
    ARROW = 'ARROW'      # for ->
    COLON = 'COLON'      # for :
    INDENT = 'INDENT'    # for tracking indentation
    EOF = 'EOF'          # end of file
    NL = 'NEW_LINE'      # end of line
    ASSIGN = 'ASSIGN'
    DEREF = 'DEREFERENCE'
    INSTRUCTIONS = [
        "PUSH" , "POP" , "SET" , "MOV" , "LDA" , "STA",
        "MOD" , "ADD" , "SUB" , "MLT" , "DV", "JMP" , "CMP"
    ]

    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __str__(self):
        if self.value:
            return f"{self.type}({self.value})"
        return f"{self.type}"

    def __repr__(self):
        if self.value:
            return f"{self.type}({self.value})"
        return f"{self.type}"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char:str | None = self.text[self.pos] if text else None
        self.current_indent = 0  # Track indentation level
    
    def error(self, reason = None):
        if reason:
            raise Exception(f'Invalid character {self.current_char}, at {self.pos}. Reason: {reason}')
        raise Exception(f'Invalid character {self.current_char}, at {self.pos}')
    
    def advance(self):
        """Move to next character"""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def skip_whitespace(self):
        """Skip spaces and tabs"""
        while self.current_char and self.current_char in (' ', '\t'):
            self.advance()

    def skip_comment(self):
        """Skip spaces and tabs"""
        while self.current_char and self.current_char != "\n":
            self.advance()
    def parse_string(self):
        out = ""
        while self.current_char != '"':
            if self.current_char is not None:
                out += self.current_char
            else:
                self.error()
        self.advance()
        return out

    def get_next_token(self) :
        while self.current_char is not None: # while file not finished
            print("parsing:", self.current_char, "pos:", self.pos)
            if not self.current_char:
                raise Exception("Failed to get next char/token")
            # skip whitespaces
            # do not skip new line
            if self.current_char.isspace() and self.current_char != "\n":
                self.skip_whitespace()
                continue

            # parse comments
            if self.current_char == "-" and self.peek() == "-":
                self.skip_comment()

            # parse strings
            if self.current_char == '"':
                return Token(Token.STRING, self.parse_string())

            # parse identifier (instructions, functions, n shi..)
            if self.current_char.isalpha():
                return Token(Token.IDENTIFIER, self.get_identifier())

            # check if it's an arrow - function
            if self.current_char == "-" and self.peek() == ">":
                self.advance() # skip "-"
                self.advance() # skip ">"
                return Token(Token.ARROW)
            # check for colon - function/lable
            if self.current_char == ':':
                self.advance()
                return Token(Token.COLON)

            # parse asigntment operator
            if self.current_char == '=':
                self.advance()
                return Token(Token.ASSIGN)

            # parse less than operator
            if self.current_char == '<':
                self.advance()
                return Token(Token.LESS_THAN)

            # parse dereference operator
            if self.current_char == '*':
                self.advance()
                return Token(Token.DEREF)

            # parse number
            if self.current_char.isnumeric():
                return Token(Token.IDENTIFIER, self.get_number())

            # parse new line
            if self.current_char == "\n":
                self.advance()
                return Token(Token.NL, "")
            self.error()
        return Token(Token.EOF)
    
    def peek(self):
        pos = self.pos + 1
        if pos > len(self.text):
            return None
        return self.text[pos]

    def get_number(self):
        res = ''
        while self.current_char :
            if self.current_char.isnumeric():
                res += self.current_char
                self.advance()
                continue
            elif self.current_char == "e" and "e" not in res:
                res += self.current_char
                self.advance()
                continue
            elif self.current_char == "." and "." not in res:
                res += self.current_char
                self.advance()
                continue
            break
        return res

    def get_identifier(self):
        res = ''
        while self.current_char and (self.current_char.isalnum() or self.current_char in ('_')):
            res += self.current_char
            self.advance()
        return res

class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer: Lexer = lexer
        self.tokens = self.tokenize()  # Store all tokens
        # print(self.tokens, self.tokens[0])
        self.token_index = 0  # Current position in the token list
    
    def tokenize(self):
        tokens = []
        while True:
            token = self.lexer.get_next_token()
            tokens.append(token)
            if token.type == Token.EOF:
                break
        # print(tokens)
        return tokens


    def eat(self, expected_type):
        """Consume a token if it matches the expected type."""
        if self.tokens[self.token_index].type == expected_type:
            self.token_index += 1
        else:
            self.error(f"Expected {expected_type}, got {self.tokens[self.token_index]}")
    def program(self):
        """Parse a program, which consists of operations and procedures."""
        operations = []
        while self.tokens[self.token_index].type != Token.EOF:
            operations.append(self.operation())
        return operations
    def operation(self):
        """Parse an operation, which can be an instruction or an identifier definition."""
        token = self.tokens[self.token_index]

        if token.type == Token.IDENTIFIER:
            # Identifier definition (e.g., "label: push 3")
            self.eat(Token.IDENTIFIER)

            if self.tokens[self.token_index].type == Token.COLON:
                self.eat(Token.COLON)
                instr_token = self.tokens[self.token_index]
                if instr_token.value in Token.INSTRUCTIONS:
                    return self.instruction()
                else:
                    self.error(f"Invalid instruction after identifier: {instr_token}")

        elif token.value in Token.INSTRUCTIONS:
            # Direct instruction
            return self.instruction()

        self.error(f"Unexpected token: {token}")

    def instruction(self):
        """Parse an instruction and its arguments."""
        instr_token = self.tokens[self.token_index]
        self.eat(Token.IDENTIFIER)  # Consume instruction

        if self.tokens[self.token_index].type in [Token.INTEGER, Token.IDENTIFIER]:
            return (instr_token.value, self.expression())  # Support expressions

        return (instr_token.value,)


    def expression(self):
        """Parse an expression (a single value or a math operation)."""
        left = self.tokens[self.token_index]
        self.eat(left.type)

        if self.tokens[self.token_index].type == Token.OPERATOR:
            op = self.tokens[self.token_index]
            self.eat(Token.OPERATOR)
            right = self.tokens[self.token_index]
            self.eat(right.type)
            return (op.value, left.value, right.value)  # Example: ('+', 'identifier', 3)

        return left.value  # Just a single value





    def error(self, reason=None):
        if reason:
            print(f"Error: invalid syntax at token index: {self.token_index}. {reason}")
        else:
            print(f"Error: invalid syntax at token index: {self.token_index}. {reason}")
        quit()


def parse(text):
    lexer = Lexer(text)
    p = Parser(lexer)
    import shutil
    columns, rows = shutil.get_terminal_size()
    print(f"Width: {columns} chars, Height: {rows} chars")

    tpc = columns // 25 # tokens per column
    for t in p.tokens:
        print(f"{str(t): <25}", end="")
    print()

    i = 0
    while i < len(p.tokens):
        for _ in range(tpc):
            if i < len(p.tokens):
                print(f"{str(p.tokens[i]): <25}", end="")
                i += 1
        print()
        i += 1
        
    return p

# Example usage:
if __name__ == "__main__":
    sample = """push 3 push 4 add """
    with open("testfile") as f:
        test = f.read();
        ast = parse(test)
    # import json
    # print(json.dumps(ast, indent=2))
