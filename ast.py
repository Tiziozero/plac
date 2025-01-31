# chatGPT 3.5/4/4o
class AST:
    def __init__(self):
        self.nodes = []  # Root node list for the program

class Node:
    def __init__(self, node_type):
        self.node_type = node_type

class PushNode(Node):
    def __init__(self, value):
        super().__init__("push")
        self.value = value  # Value being pushed to the stack

class PopNode(Node):
    def __init__(self):
        super().__init__("pop")

class AddNode(Node):
    def __init__(self, reference):
        super().__init__("add")
        self.reference = reference  # Reference to a variable

class PrintNode(Node):
    def __init__(self):
        super().__init__("print")

class CallNode(Node):
    def __init__(self, function_name):
        super().__init__("call")
        self.function_name = function_name  # Name of the function being called

class ProcedureNode(Node):
    def __init__(self, name, return_type, body):
        super().__init__("procedure")
        self.name = name
        self.return_type = return_type
        self.body = body  # List of statements inside the function

class ReturnNode(Node):
    def __init__(self, value=None):
        super().__init__("return")
        self.value = value  # Optional return value

