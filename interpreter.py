from tokens import Doubloon, Piece8, Reserved

class Interpreter:
    def __init__(self, tree, base):
        self.tree = tree
        self.data = base

    def read_DOUBLOON(self, value):
        return int(value)
    
    def read_PIECE8(self, value):
        return float(value)
    
    def read_BOOTY(self, id):
        variable = self.data.read(id)
        variable_type = variable.type

        return getattr(self, f"read_{variable_type}")(variable.value)

    def compute_bin(self, left, op, right):
        left_type = "BOOTY" if str(left.type).startswith("BOOTY") else str(left.type)
        right_type = "BOOTY" if str(right.type).startswith("BOOTY") else str(right.type)
        if op.value == "=":
            left.type = f"BOOTY({right_type})"
            self.data.write(left, right)
            return self.data.read_all()

        left = getattr(self, f"read_{left_type}")(left.value)
        right = getattr(self, f"read_{right_type}")(right.value)

        if op.value == "+":
            output = left + right
        elif op.value == "-":
            output = left - right
        elif op.value == "*":
            output = left * right
        elif op.value == "/":
            output = left / right
        elif op.value == ">":
            output = 1 if left > right else 0
        elif op.value == ">=":
            output = 1 if left >= right else 0
        elif op.value == "<":
            output = 1 if left < right else 0
        elif op.value == "<=":
            output = 1 if left <= right else 0
        elif op.value == "?=":
            output = 1 if left == right else 0
        elif op.value == "and":
            output = 1 if left and right else 0
        elif op.value == "or":
            output = 1 if left or right else 0

        return Doubloon(output) if (left_type == "DOUBLOON" and right_type == "DOUBLOON") else Piece8(output)
        

    def compute_unary(self, operator, operand):
        operand_type = "BOOTY" if str(operand.type).startswith("BOOTY") else str(operand.type)

        operand = getattr(self, f"read_{operand_type}")(operand.value)

        if operator.value == "+":
            output = +operand
        elif operator.value == "-":
            output = -operand
        elif operator.value == "not":
            output = 1 if not operand else 0
        
        return Doubloon(output) if (operand_type == "DOUBLOON") else Piece8(output)

    def interpret(self, tree=None):
        if tree is None:
            tree = self.tree

        if isinstance(tree, list):
            if isinstance(tree[0], Reserved):
                if tree[0].value == "if":
                    for idx, condition in enumerate(tree[1][0]):
                        evaluation = self.interpret(condition)
                        if evaluation.value == 1:
                            return self.interpret(tree[1][1][idx])
                    
                    if len(tree[1]) == 3:
                        return self.interpret(tree[1][2])
                    
                    else:
                        return
                elif tree[0].value == "while":
                    condition = self.interpret(tree[1][0])
                    
                    while condition.value == 1:
                        # Doing the action
                        print(self.interpret(tree[1][1]))

                        # Checking the condition
                        condition = self.interpret(tree[1][0])
                    
                    return
                elif tree[0].value == "parley":
                    result = self.interpret(tree[1])
                    print(f"Ahoy! {result}")
                    return result

        # Unary operation            
        if isinstance(tree, list) and len(tree) == 2:
            expression = tree[1]
            if isinstance(expression, list):
                expression = self.interpret(expression)
            return self.compute_unary(tree[0], expression)
        
        # No operation
        elif not isinstance(tree, list):
            return tree
        
        else:
            # Post order traversal

            # Evaluating left subtree
            left_node = tree[0]
            if isinstance(left_node, list):
                left_node = self.interpret(left_node)

            # Evaluating right subtree
            right_node = tree[2]
            if isinstance(right_node, list):
                right_node = self.interpret(right_node)

            # Evaluating root node
            operator = tree[1]
            return self.compute_bin(left_node, operator, right_node)

