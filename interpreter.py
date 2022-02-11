from tokens import *
from error import Error
class DivideByZeroError(Error):
    def __init__(self):
        raise Exception('Divide by Zero')
    
class No_Name_Error(Error):
    def __init__(self):
        raise Exception('Name Error')

class VarNotDefinedError(Error):
    def __init__(self, name):
        raise Exception (f"{name} not defined")
class Interpreter():
    store = {}
    # Traverses through the AST produced from parser and calculates the result of the input expression
    def __init__(self, ast):
        self.ast = ast

    def interpret(self):
        # self.visit(self.ast)
        return self.visit(self.ast)
        # return self.store_repr()
    
    def store_repr(self):
        result = "{"
        for key, value in sorted(self.store.items()):
            if value[1] == VAL_NOT_INITIALIZED:
                continue
            result += str(key)
            result += " → "
            result += str(value[0])
            result += ", "
        if len(self.store) > 0:
            result = result[:-2]
        result += "}"
        return result        

    def visit(self, node):
        func_name = f'visit_{type(node).__name__}'
        func = getattr(self, func_name, self.no_visit_func)
        return func(node)
    
    def no_visit_func(self, node):
        raise Exception(f'No visit_{type(node).__name__} func defined')
    
    def visit_Binary_op_node(self, node):
        if node.op.type == TT_PLUS:
            return self.visit(node.left_node) + self.visit(node.right_node)
        elif node.op.type == TT_MINUS:
            return self.visit(node.left_node) - self.visit(node.right_node)
        elif node.op.type == TT_MUL:
            return self.visit(node.left_node) * self.visit(node.right_node)
        elif node.op.type == TT_DIVIDE:
            try:
                return self.visit(node.left_node) // self.visit(node.right_node)
            except:
                DivideByZeroError()
        elif node.op.type == TT_EQ:
            return self.visit(node.left_node) == self.visit(node.right_node)
        elif node.op.type == TT_LT: 
            return self.visit(node.left_node) < self.visit(node.right_node)
        elif node.op.type == TT_GT:
            return self.visit(node.left_node) > self.visit(node.right_node)
        elif node.op.type == TT_AND:
            return self.visit(node.left_node) & self.visit(node.right_node)
        elif node.op.type == TT_OR:
            return self.visit(node.left_node) | self.visit(node.right_node)
        elif node.op.type == TT_SEMI:
            return self.execute_statements(node)
        
    def visit_Unary_op_node(self, node):
        op = node.op.type
        if op == TT_PLUS:
            return +self.visit(node.node)
        elif op == TT_MINUS:
            return -self.visit(node.node)
        elif node.op.type == TT_NOT:
            return not(self.visit(node.node))
        
    def visit_Num_node(self, node):
        return node.value
    
    def visit_Assign_node(self, node):
        name = node.name.value
        value = self.visit(node.value)
        self.store[name] = (value, VAL_INITIALIZED)

    def visit_Variable_node(self, node):
        id = node.value
        value = self.store.get(id)
        if not value:
            self.store[id] = (0, VAL_NOT_INITIALIZED)
            value = self.store.get(id)
        return value[0]
        
    def visit_Skip_node(self, node):
        pass

    def visit_If_node(self, node):
        if self.visit(node.condition):
            self.visit(node.true_case)
        else:
            self.visit(node.false_case)
    
    def visit_While_node(self, node):
        while True:
            condition = self.visit(node.condition)

            if not condition:
                break
            self.visit(node.body)
        return None
    
    def visit_Bool_node(self, node):
        if node.token.matches(TT_KEYWORD, 'true'):
            return True
        elif node.token.matches(TT_KEYWORD, 'false'):
            return False
    
    def execute_statements(self, node):
        if node.left_node != None:
            self.visit(node.left_node)
        if node.right_node != None:
            self.visit(node.right_node)
        return None

    def visit_For_node(self, node):
        self.visit(node.initialize)
        while True:
            terminate = self.visit(node.terminate)

            if terminate:
                break
            self.visit(node.body)
            self.visit(node.step)

        return None
