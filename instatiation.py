class Instantiation(Statement):
    def __init__(self, obj = None, definition = None):
        self.object = obj
        self.definition = definition
        self.next = None
