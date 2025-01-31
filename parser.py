class Token:
    # Let's define our basic token types
    INTEGER = 'INTEGER'
    VALUE = 'VALUE'
    IDENTIFIER = 'IDENTIFIER'
    ARROW = 'ARROW'      # for ->
    COLON = 'COLON'      # for :
    INDENT = 'INDENT'    # for tracking indentation
    EOF = 'EOF'          # end of file

    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __str__(self):
        if self.value:
            return f"{self.type}({self.value})"
        return str(self.type)

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if text else None
        self.current_indent = 0  # Track indentation level
    
    def error(self):
        raise Exception(f'Invalid character {self.current_char}')
    
    def advance(self):
        """Move to next character"""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def skip_whitespace(self):
        """Skip spaces and tabs"""
        while self.current_char and self.current_char.isspace():
            self.advance()

    def get_next_token(self) :
        while self.current_char is not None: # while file not finished
            # skip whitespaces
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            # get identifier
            if self.current_char.isalpha():
                return Token(Token.IDENTIFIER, self.get_identifier())

            # check if it's an arrow
            if self.current_char == "-" and self.peek() == ">":
                self.advance() # skip "-"
                self.advance() # skip ">"
                return Token(Token.ARROW)
            # check for colon
            if self.current_char == ':':
                self.advance()
                return Token(Token.COLON)
            self.error()
        return Token(Token.EOF)
    def peek(self):
        pos = self.pos + 1
        if pos > len(self.text):
            return None
        return self.text[pos]
    def  get_identifier(self):
        res = ''
        while self.current_char and self.current_char.isalnum():
            res += self.current_char
            self.advance()
        return res

class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer: Lexer = lexer
        self.token_index = 0

    def program(self):
        # expect IDENTIFIER + COLON | ARROW
        while True:
            token = self.lexer.get_next_token()
            self.token_index += 1
            if token.type != Token.IDENTIFIER:
                self.error(f"expected identifier, found {token}")

            token = self.lexer.get_next_token()
            # if it's a colon then it should be a variable
            if token.type == Token.COLON:
                value_token = self.lexer.get_next_token()
                if value_token.type != Token.VALUE:
                    self.error(f"expected value, found {value_token.type}")
                

            


    def error(self, reason=None):
        if reason:
            print(f"Error: invalid syntax at token index: {self.token_index}. {reason}")
        else:
            print(f"Error: invalid syntax at token index: {self.token_index}. {reason}")
        quit()


def parse(text):
    lexer = Lexer(text)
    # parser = Parser(lexer)
    # return parser.program()

# Example usage:
if __name__ == "__main__":
    lexer = Lexer("main -> int:")
    token = lexer.get_next_token()  # should get IDENTIFIER(main)
    print(token)
    token = lexer.get_next_token()  # should get ARROW
    print(token)
    token = lexer.get_next_token()  # should get IDENTIFIER(int)
    print(token)
    token = lexer.get_next_token()  # should get COLON
    print(token)
    token = lexer.get_next_token()  # should get EOF
    print(token)
    exit()
    sample = """
    main -> int:
        var1: push 3    -- push to stack and save reference
        var2: push 5    -- push to stack
        pop             -- pop var2
        return var1     -- return var1
    
    print_char -> char:
        push "A"
        return
    """
    
    ast = parse(sample)
    import json
    print(json.dumps(ast, indent=2))
