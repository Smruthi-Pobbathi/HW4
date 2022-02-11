
TT_NUM = 'NUM'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIVIDE = 'DIVIDE'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_IDENTIFIER = 'IDENTIFIER'
TT_EQ = 'EQ'
TT_ASGN = 'ASGN'
TT_LT = 'LT'
TT_GT = 'GT'
TT_NOT = 'NOT'
TT_OR = 'OR'
TT_AND = 'AND'
TT_SEMI = 'SEMI'
TT_LBRACE = 'LBRACE'
TT_RBRACE = 'RBRACE'
TT_KEYWORD = 'KEYWORD'
VAL_INITIALIZED = 'INIT'
VAL_NOT_INITIALIZED = 'NOT_INIT'

KEYWORDS = [
    'skip', 'if', 'then', 'else', 'do', 'while', 'true', 'false', 'for'
]
class Token:
    def __init__(self, type, value = None):
        self.type = type
        self.value: any = value
    
    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self) -> str:
        return self.type + (f":{self.value}" if self.value != None else "")