from enum import Enum

class StmtType:
    INST = 0
    INST_DEF = 1
    OP = 2
    LOOP = 3
    PRINT = 4
    

class Statement():
    def __init__(self, obj = None, definition = None):
        self.type = None
        self.instantiation = None
        self.action = None
        self.condition = None
        self.operation = None
        self.next = None
