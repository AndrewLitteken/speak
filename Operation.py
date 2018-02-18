from enum import Enum

class OpType:
    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 3
    MOD = 4
    RND = 5
    GT = 6
    GEQ = 7
    LT = 8
    LEQ = 9
    EQ = 10
    NEQ = 11

class Operation:
    def __init__(self, op_type=None, item_one = None, item_two = None):
        self.op = op_type
        self.left = item_one
        self.right = item_two
    
    def set_type(self, op_type, inverse):
        if op_type == "less" or op_type == "smaller":
            if not inverse:
                self.op = OpType.LT
            else:
                self.op = OpType.GT
        elif op_type == "more" or op_type == "larger" or op_type == "greater":
            if inverse:
                self.op = OpType.LT
            else:
                self.op = OpType.GT
        elif op_type == "plus":
            self.op = OpType.ADD 
        elif op_type == "minus":
            self.op = OpType.SUB
        elif op_type == "multiply":
            self.op = OpType.MUL 
        elif op_type == "divide":
            self.op = OpType.DIV 
        elif op_type == "equals":
            if inverse:
                self.op = OpType.EQ
            else:
                self.op = OpType.NEQ
