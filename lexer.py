from tokens import *
from error import Error
import string

DIGITS = '0123456789'
WHITESPACE = ' \t\n'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS
class IllegalCharError(Error):
    def __init__(self):
        raise Exception('Illegal character')
class Lexer():
    # From the given input ArithLexer generates list of objects which holds value and type
    def __init__(self, input_text):
        self.input_text = input_text
        self.pos = 0
        self.current_char = input_text[0]
    
    def next_char(self):
        self.pos += 1
        if self.pos < len(self.input_text):
            self.current_char = self.input_text[self.pos]
        else:
            self.current_char = None

    def generate_tokens(self):
        tokens = [Token]
        self.current_char = self.input_text[0]
    
        while self.current_char != None:
            if self.current_char in WHITESPACE:
                self.next_char()

            elif self.current_char in DIGITS:
                number = self.generate_number()
                tokens.append(Token(TT_NUM, number))
            
            elif self.current_char in LETTERS:
                token_type, id = self.generate_identifier()
                tokens.append(Token(token_type, id))

            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.next_char()

            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.next_char()
            
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.next_char()
                
            elif self.current_char == '/':
                tokens.append(Token(TT_DIVIDE))
                self.next_char()
            
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.next_char()

            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.next_char()
            
            elif self.current_char == '{':
                tokens.append(Token(TT_LBRACE))
                self.next_char()
            
            elif self.current_char == '}':
                tokens.append(Token(TT_RBRACE))
                self.next_char()

            elif self.current_char == ':':
                self.next_char()
                if self.current_char == '=':
                    tokens.append(Token(TT_ASGN))
                    self.next_char()
                else:
                    return IllegalCharError()

            elif self.current_char == '=':
                self.next_char()
                tokens.append(Token(TT_EQ))
            
            elif self.current_char == ';':
                self.next_char()
                tokens.append(Token(TT_SEMI))

            elif self.current_char == '¬':
                self.next_char()
                tokens.append(Token(TT_NOT))
            
            elif self.current_char == '<':
                self.next_char()
                tokens.append(Token(TT_LT))
            
            elif self.current_char == '>':
                self.next_char()
                tokens.append(Token(TT_GT))
            
            elif self.current_char == '∨':
                self.next_char()
                tokens.append(Token(TT_OR))
            
            elif self.current_char == '∧':
                self.next_char()
                tokens.append(Token(TT_AND))
                
            else:
                self.next_char()
                return IllegalCharError()

        return tokens, None

    def generate_number(self):
        num_str = ""
        while self.current_char in DIGITS:
            num_str += self.current_char
            self.next_char()
            if self.current_char == None:
                break
        return (int(num_str))

    def generate_identifier(self):
        id_str = ''

        while self.current_char != None and self.current_char in LETTERS_DIGITS:
            id_str += self.current_char
            self.next_char()
        token_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return (token_type, id_str)