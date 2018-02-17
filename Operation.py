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

class Operation:
    def __init__(self, op_type, item_one = None, item_two = None):
        self.op = op_type
        self.left = item_one
        self.right = item_two
