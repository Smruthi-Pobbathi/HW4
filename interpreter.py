from tokens import *
from error import Error
from enum import Enum, unique
@unique
class LoopPos(Enum):
    NO_LOOP = 0
    LOOP_BEGIN = 1
    LOOP_MID = 2
    LOOP_END = 3
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
    loop_pos = LoopPos.NO_LOOP
    # repr_result = ""
    # Traverses through the AST produced from parser and calculates the result of the input expression
    def __init__(self, ast):
        self.ast = ast

    def interpret(self):
        # self.visit(self.ast)
        return self.visit(self.ast)
        # return self.store_repr()
    
    def store_repr(self):
        result = "{"
        uninitialized = 0
        for key, value in sorted(self.store.items()):
            if value[1] == VAL_NOT_INITIALIZED:
                uninitialized += 1
                continue
            result += str(key)
            result += " → "
            result += str(value[0])
            result += ", "
        if len(self.store) - uninitialized > 0:
            # and len(self.store) != 1:
            result = result[:-2]
        # elif len(self.store) == 1:
        #     result = result
        result += "}"
        return result        

    def visit(self, node, from_loop = False):
        func_name = f'visit_{type(node).__name__}'
        func = getattr(self, func_name, self.no_visit_func)
        return func(node, from_loop)
    
    def no_visit_func(self, node, from_loop = False):
        raise Exception(f'No visit_{type(node).__name__} func defined')

    def show(self, node):
    #  prt):
        func_name = f'show_{type(node).__name__}'
        func = getattr(self, func_name, self.no_show_func)
        return func(node)
    
    def no_show_func(self, node, from_loop = False):
    #  prt):
        raise Exception(f'No show_{type(node).__name__} func defined')
    
    def visit_Binary_op_node(self, node, from_loop = False):
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
        
        # self.repr_result + "⇒ skip, " + self.store_repr()
        # print("⇒ skip, ", self.store_repr())

    def show_Binary_op_node(self, node):
        # self.repr_result + "⇒ skip, " + self.store_repr()
        # print("⇒ skip, " + self.store_repr())
        if node.op.type == TT_PLUS:
            return str("(" + self.show(node.left_node) + "+" + self.show(node.right_node) + ")")
            # print("(" + self.show(node.left_node) + "+" + self.show(node.right_node) + ")")
            # return ""
        elif node.op.type == TT_MINUS:
            return str("(" + self.show(node.left_node) + "-" + self.show(node.right_node) + ")")
            # print("(" + self.show(node.left_node) + "-" + self.show(node.right_node) + ")")
            # return ""
        elif node.op.type == TT_MUL:
            return str("(" + self.show(node.left_node) + "*" + self.show(node.right_node) + ")")
            # print("(" + self.show(node.left_node) + "*" + self.show(node.right_node) + ")")
            # return ""
        elif node.op.type == TT_DIVIDE:
            return str("(" + self.show(node.left_node) + "/" + self.show(node.right_node) + ")")
            # print("(" + self.show(node.left_node) + "/" + self.show(node.right_node) + ")")
            # return ""
        elif node.op.type == TT_EQ:
            return str("(" + self.show(node.left_node) + "=" + self.show(node.right_node) + ")")
            # print("(" + self.show(node.left_node) + "=" + self.show(node.right_node) + ")")
            # return ""
        elif node.op.type == TT_LT: 
            return str("(" + self.show(node.left_node) + "<" + self.show(node.right_node) + ")")
            # print("(" + self.show(node.left_node) + "<" + self.show(node.right_node) + ")")
            # return 
        elif node.op.type == TT_GT:
            return str("(" + self.show(node.left_node) + ">" + self.show(node.right_node) + ")")
            # print("(" + self.show(node.left_node) + ">" + self.show(node.right_node) + ")")
            # return
        elif node.op.type == TT_AND:
            return str("(" + self.show(node.left_node) + "∧" + self.show(node.right_node) + ")")
            # print ("(" + self.show(node.left_node) + "∧" + self.show(node.right_node) + ")")
            # return ""
        elif node.op.type == TT_OR:
            return str("(" + self.show(node.left_node) + "∨" + self.show(node.right_node) + ")")
            # print("(" + self.show(node.left_node) + "∨" + self.show(node.right_node) + ")")
            # return ""
        elif node.op.type == TT_SEMI:
            return self.execute_statements(node)
    
    def visit_Unary_op_node(self, node, from_loop = False):
        op = node.op.type
        if op == TT_PLUS:
            return +self.visit(node.node)
        elif op == TT_MINUS:
            return -self.visit(node.node)
        elif node.op.type == TT_NOT:
            return not(self.visit(node.node))
    
    def show_Unary_op_node(self, node):
        # , prt):
        op = node.op.type
        # if prt:
        if op == TT_PLUS:
            # self.repr_result + "+" + self.show(node.node)
            return ("+" + self.show(node.node))
        elif op == TT_MINUS:
            # self.repr_result + "-" + self.show(node.node)
            return ("-" + self.show(node.node))
        elif op == TT_NOT:
            # self.repr_result + "¬" + self.show(node.node)
            return ("¬" + self.show(node.node))
        
    def visit_Num_node(self, node, from_loop = False):
        return node.value
    
    def show_Num_node(self, node):
    # , prt):
        # self.repr_result + node.value
        # if prt:
        # print(node.value)
        return str(node.value)
    
    def visit_Assign_node(self, node, from_loop=False):
        name = node.name.value
        value = self.visit(node.value)
        self.store[name] = (value, VAL_INITIALIZED)
        if from_loop:
            return str(node.name.value + " := " + str(self.show(node.value)))
        else:
            self.show_store()
        # self.prt_assign(node)

    # def prt_assign(self, node):
    #     print(node.name.value + " := " + str(self.show(node.value)) + ", " + self.store_repr())


    def show_Assign_node(self, node):
    # , prt):
        name = node.name.value
        value = self.show(node.value)
        if self.loop_pos is LoopPos.LOOP_BEGIN:
            return str("⇒ " + name + " := " + str(value) + ";")
        elif self.loop_pos is LoopPos.LOOP_MID:
            return str(name + " := " + str(value))
        elif self.loop_pos is LoopPos.NO_LOOP:
            return str("⇒ " + name + " := " + str(value) + ", " + self.store_repr())
        # if prt:
        # return str(name + " := " + str(value))
        
        # print( "⇒ " + name + " := " + str(value) + ", " + self.store_repr())
        
    def visit_Variable_node(self, node, from_loop = False):
        id = node.value
        value = self.store.get(id)
        if not value:
            self.store[id] = (0, VAL_NOT_INITIALIZED)
            value = self.store.get(id)
        return value[0]
    
    def show_Variable_node(self, node):
    # , prt):
        # self.repr_result + self.show(node.value)
        # if prt:
        # print(node.value)
        return str(node.value)
        
    def visit_Skip_node(self, node, from_loop = False):
        pass

    def show_Skip_node(self, node):
    # , prt):
        print("")

    def visit_If_node(self, node, from_loop = False):
        if self.visit(node.condition):
            print(self.show(node.true_case))
            self.visit(node.true_case)
            # self.show_store()
            
        else:
            print(self.show(node.false_case))
            self.visit(node.false_case)
            # self.show_store()
    def show_If_node(self, node):
        # , prt):
        # if prt:
            # self.repr_result + "⇒ if (" + self.show(node.condition, True) + ") then { " + self.show(node.true_case, True) + "} else { " + self.show(node.false_condition, True) +" } "  + self.store_repr())
        print("⇒ if " + self.show(node.condition) + " then { " + self.show(node.true_case) + "} else { " + self.show(node.false_case) + " } "  + self.store_repr())

    def visit_While_node(self, node, from_loop = False):
        counter = 10000
        while self.visit(node.condition):
            self.loop_pos = LoopPos.LOOP_BEGIN
            print(self.show(node.body), end="")
            self.loop_pos = LoopPos.LOOP_MID
            print(" while " + self.show(node.condition) + " do { "+ self.show(node.body) + " }, " + self.store_repr())
            counter -= 1
            if counter == 0:
                break
            self.visit(node.body, from_loop = True)
            print("⇒ skip; " + "while " + self.show(node.condition) + " do { "+ self.show(node.body) + " }, " + self.store_repr())
            counter -= 1
            if counter == 0:
                break
            print("⇒ while " + self.show(node.condition) + " do { "+ self.show(node.body) + " }, " + self.store_repr())
            counter -= 1
            if counter == 0:
                break
        if counter > 0:
            self.show_store()
        self.loop_pos = LoopPos.NO_LOOP
        return None

    def show_While_node(self, node):
        # , prt):
        # if prt:
            #  self.repr_result + "while " + self.show(node.body, True)
            #  self.show(node.condition, True) + " do { " +  self.show(node.body, True) + " }, " + self.store_repr   
            print("⇒ while " + self.show(node.condition) + " do { "+ self.show(node.body) + " }, " + self.store_repr())

    def visit_Bool_node(self, node, from_loop = False):
        if node.token.matches(TT_KEYWORD, 'true'):
            return True
        elif node.token.matches(TT_KEYWORD, 'false'):
            return False
    
    def show_Bool_node(self, node):
    # , prt):
        # if prt:
        if node.token.matches(TT_KEYWORD, 'true'):
            return ("true")
        elif node.token.matches(TT_KEYWORD, 'false'):
            return ("false")
    
    def execute_statements(self, node):
        if node.left_node != None:
            print("⇒ skip; ")
            self.visit(node.left_node)
            self.show(node.right_node)
        if node.right_node != None:
            self.visit(node.right_node)
            self.show_store()
        return None

    def show_store(self):
        print("⇒ skip,",self.store_repr())

    # def visit_For_node(self, node, from_loop = False):
    #     self.visit(node.initialize)
    #     while True:
    #         terminate = self.visit(node.terminate)

    #         if terminate:
    #             break
    #         self.visit(node.body)
    #         self.visit(node.step)

    #     return None
