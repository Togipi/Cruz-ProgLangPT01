class Token:
    # Token types
    INTEGER, MUL, DIV, EOF = 'INTEGER', 'MUL', 'DIV', 'EOF'

    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {self.value})'


class Interpreter:
    def __init__(self, text):
        self.text = text  # Input text
        self.pos = 0  # Current position in the text
        self.current_token = None  # Current token instance

    def error(self):
        # Error handling for invalid syntax
        raise Exception('Invalid syntax')

    def get_next_token(self):
        """
        Lexical analyzer (tokenizer):
        Breaks input into tokens (INTEGER, MUL, DIV, EOF)
        """
        text = self.text
        if self.pos >= len(text):
            return Token(Token.EOF, None)

        current_char = text[self.pos]
        
        if current_char.isdigit():
            # Extract multi-digit integer
            num_value = ''
            while self.pos < len(text) and text[self.pos].isdigit():
                num_value += text[self.pos]
                self.pos += 1
            return Token(Token.INTEGER, int(num_value))

        if current_char == '*':
            self.pos += 1
            return Token(Token.MUL, '*')

        if current_char == '/':
            self.pos += 1
            return Token(Token.DIV, '/')
        
        self.error()

    def eat(self, token_type):
        """
        Verify token type and move to next token
        """
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def factor(self):
        """
        factor : INTEGER
        """
        token = self.current_token
        self.eat(Token.INTEGER)
        return token.value

    def expr(self):
        """
        expr : factor ((MUL | DIV) factor)*
        """
        self.current_token = self.get_next_token()
        result = self.factor()

        while self.current_token.type in (Token.MUL, Token.DIV):
            token = self.current_token
            if token.type == Token.MUL:
                self.eat(Token.MUL)
                result *= self.factor()
            elif token.type == Token.DIV:
                self.eat(Token.DIV)
                result /= self.factor()
        
        return result


def main():
    """
    Function to take user input and evaluate expressions
    """
    while True:
        try:
            text = input("Enter an expression (or type 'exit' to end session.): ")
            if text.lower() == 'exit':
                break
            interpreter = Interpreter(text.replace(' ', ''))
            result = interpreter.expr()
            print(f'Result: {result}')
        except Exception as e:
            print(f'Error: {e}')


if __name__ == "__main__":
    main()
