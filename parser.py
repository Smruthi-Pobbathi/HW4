# stmt       : comp-expr SEMI compr-expr
# expr       : IDENTIFIER EQ expr
#            : comp-expr((AND|OR)comp-expr)*

# comp-expr  : NOT comp-expr
#            : arith-expr((EQ|LT|GT) arith-expr*)

# arith-expr : term((Plus|Minus) term)*

# term       : factor((Mul|Div) factor)*

# factor     : Int | +Int | -Int
#            : LPAREN | RPAREN
#            : if-expr
#            : while-expr

# if-expr    : KEYWORD: if expr KEYWORD: then expr
#            : KEYWORD else expr?
# while-expr : KEYWORD: while expr KEYWORD: do expr

from tokens import *
from error import Error

class Num_node:
    # Creates a single node which holds Int values
    def __init__(self, token):
        self.token = token
        self.value = token.value
    
class Binary_op_node:
    # Creates a node which has left and right nodes also op node which holds operator
    def __init__(self, left_node, op, right_node):
        self.left_node = left_node
        self.op = op
        self.right_node = right_node

class Unary_op_node:
    # Creates a node which has a node also op node which holds operator
    def __init__(self, op, node):
        self.op = op
        self.node = node

class Assign_node:
    # Assign value to variable from only constant or from expression
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Variable_node:
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Skip_node:
    pass

class If_node:
    # if stmt has 3 children, 
    # test if the condition is true
    # then execute stmt_1
    # else execute stmt_2
    def __init__(self, condition, true_case, false_case):
        self.condition = condition
        self.true_case = true_case
        self.false_case = false_case

class While_node:
    # While has condition and body
    # condition will be expression 
    # Body can be any other node or [statement]
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class For_node:
    def __init__(self, initialize, terminate, step, body):
        self.initialize = initialize
        self.terminate = terminate
        self.step = step
        self.body = body

class Bool_node:
    def __init__(self, token):
        self.token = token

class Invalid_syntax_error(Error):
    def __init__(self):
        raise Exception('Invalid Syntax')

class Parser:
    # Parses the tokens genetrted from the tokenizer and generates an AST.
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.pos = 0
        self.next()
    
    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.tokens) - 1:
            return None
        else:
            return self.tokens[peek_pos]

    def next(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current = self.tokens[self.pos]
        return self.current

    def error(self):
        return [], Invalid_syntax_error()

    def parse(self):
        result = self.stmt()
        return result

    def factor(self):
        token = self.current
        if token.type == TT_MINUS:
            self.next()
            node = Unary_op_node(token, self.factor())
            return node 
        elif token.type == TT_PLUS:
            self.next()
            node = Unary_op_node(token, self.factor())
            return node
        elif token.type == TT_NUM:
            self.next()
            return Num_node(token)
        elif token.type == TT_IDENTIFIER:
            self.next()
            return Variable_node(token)
        elif token.type == TT_LPAREN:
            self.next()
            node = self.stmt()
            if self.current.type == TT_RPAREN:
                self.next()
                return node
            else:
                return Invalid_syntax_error()
        elif token.type == TT_LBRACE:
            self.next()
            body = self.stmt()
            if self.current.type == TT_RBRACE:
                self.next()
                return body
            else:
                return Invalid_syntax_error()

        elif token.matches(TT_KEYWORD, 'if'):
            if_expr = self.if_expr()
            return if_expr

        elif token.matches(TT_KEYWORD, 'skip'):
            return self.skip()

        elif token.matches(TT_KEYWORD, 'while'):
            while_expr = self.while_expr()
            return while_expr
        
        elif token.matches(TT_KEYWORD, 'false'):
            self.next()
            return Bool_node(token)
        
        elif token.matches(TT_KEYWORD, 'true'):
            self.next()
            return Bool_node(token)
        
        elif token.matches(TT_KEYWORD, 'for'):
            for_expr = self.for_expr()
            return for_expr
        
        else:
            node = self.variable()
            return node

    def term(self):
        return self.binary_operation(self.factor, (TT_MUL, TT_DIVIDE))

    def expression(self):
        if self.current.type == TT_IDENTIFIER:
            peek = self.peek()
            if peek is not None and peek.type == TT_ASGN:
                var_name = self.current
                self.next()
                self.next()
                expr = self.expression()
                return Assign_node(var_name, expr)
        node = self.binary_operation(self.comparision_expr, (TT_AND, TT_OR))
        return node
    
    def stmt(self):
        return self.binary_operation(self.expression, (TT_SEMI))

    def binary_operation(self, fun, operators):
        left = fun()
        while self.current.type in operators:
            op = self.current
            self.next()
            right = fun()
            left = Binary_op_node(left, op, right)
        return left
    
    def comparision_expr(self):
        if self.current.type == (TT_NOT):
            op = self.current
            self.next()
            node = self.comparision_expr()
            return Unary_op_node(op, node)
        
        node = self.binary_operation(self.arith_expr, (TT_EQ, TT_GT, TT_LT))
        return node
    
    def arith_expr(self):
        return self.binary_operation(self.term, (TT_PLUS, TT_MINUS))
    
    def variable(self):
        node = Variable_node(self.current)
        self.next()
        return node
    
    def skip(self):
        return Skip_node()
    
    def if_expr(self):
        if not self.current.matches(TT_KEYWORD, 'if'):
            return Invalid_syntax_error
        self.next()
        condition = self.expression()

        if not self.current.matches(TT_KEYWORD, 'then'):
            return Invalid_syntax_error
        self.next()
        true_case = self.stmt()

        false_case = Skip_node
        if self.current.matches(TT_KEYWORD, 'else'):
            self.next()
            false_case = self.stmt()
        return If_node(condition, true_case, false_case)
    
    def while_expr(self):
        if not self.current.matches(TT_KEYWORD, 'while'):
            return Invalid_syntax_error
        self.next()
        condition = self.expression()

        if not self.current.matches(TT_KEYWORD, 'do'):
            return Invalid_syntax_error
        self.next()
        body = self.expression()
        return While_node(condition, body)

    def for_expr(self):
        if not self.current.matches(TT_KEYWORD, 'for'):
            return Invalid_syntax_error
        self.next()
        initialize = self.expression()
        
        self.next()
        terminate = self.expression()
        
        self.next()
        step = self.expression()
        
        if not self.current.matches(TT_KEYWORD, 'do'):
            return Invalid_syntax_error
        self.next()
        body = self.expression()

        return For_node(initialize, terminate, step, body)









            


