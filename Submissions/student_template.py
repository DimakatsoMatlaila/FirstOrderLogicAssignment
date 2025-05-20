from typing import Literal
import json

class TuringMachine:
    states: list[int]
    alphabet: list[int]
    transitions: list[tuple[int, int, int, int, int]]
    initial_state: int
    accept_state: int
    reject_state: int

    def __init__(self):
        self.states = [ 0, 1, 2 ]
        self.alphabet = [ 0, 1 ] # blank, and end-of-tape
        self.transitions = []
        self.initial_state = 0
        self.accept_state = 1
        self.reject_state = 2

    def from_json(json_string: str) -> 'TuringMachine':
        """
            TODO: Parse the following JSON structure as a string into the TuringMachine 
            {
                // Always will have initial, accept and reject states
                "states": [ 0, 1, 2, ... ],
                // Always will have blank symbol as the first symbol, but does not need to be 0
                // Always will have end-of-tape symbol as the second symbol, but does not need to be 1
                "alphabet": [ 0, 1, ... ], 
                "transitions": [
                    // [ current state, read symbol, next state, write symbol, direction ]
                    // direction: L = -1, R = 1
                    [ 0, 0, 0, 0, 1 ],
                    [ 0, 1, 0, 0, -1 ],
                    ...
                ],
                "initial_state": 0, // Is an index into "states", will always exist in states, but does not need to be 0
                "accept_state": 1,  // Is an index into "states", will always exist in states, but does not need to be 1
                "reject_state": 2,  // Is an index into "states", will always exist in states, but does not need to be 2
            }
        """
        pass

class Model:
    domain: list[object]
    interpretations: dict[str, list[str] | str | dict[str, str]]

    def __init__(self):
        self.domain = []
        self.interpretations = {}

    def from_json(json_string: str) -> 'Model':
        """
            TODO: Parse the following JSON structure as a string into the model
            {
                "domain": [ "0", "1", "2", ... ],
                "interpretations": {
                    "s": { "0":"1", "1":"2", ... } // A function is a JSON map
                    "P": [ "0,1", "0,2", "1,2", ... ] // A predicate is a JSON array
                    // A function / predicate with arity greater than 1
                    // have the different domain elements as one string seperated by a comma
                    // Unary: "a"
                    // Binary: "a,b"
                    // Ternary: "a,b,c"
                    // etc...
                    "0": "0" // A constant is a one-to-one lookup
                }
            }
        """

        pass

class Alphabet:
    equality = "="
    negation = "!"
    conjunction = "&"
    disjunction = "|"
    implication = ">"
    forall = "@"
    exists = "#"
    descend_seperator = "(" # All subexpressions until the ascend seperator are a child of current expression
    ascend_seperator = ")" # All subexpressions from the descend seperator are a child of current expression
    level_seperator = "," # All expressions have the same parent

class ExpressionTree:
    value: str
    children: list['ExpressionTree']
    parent: 'ExpressionTree'

    def __init__(self, value: str, children: list['ExpressionTree'], parent: 'ExpressionTree'):
        self.value = value
        self.children = children
        self.parent = parent

    def equals_expr() -> 'ExpressionTree':
        return ExpressionTree(Alphabet.equality, [None, None], None)
    def not_expr() -> 'ExpressionTree':
        return ExpressionTree(Alphabet.negation, [None], None) 
    def and_expr() -> 'ExpressionTree':
        return ExpressionTree(Alphabet.conjunction, [None, None], None)
    def or_expr() -> 'ExpressionTree':
        return ExpressionTree(Alphabet.disjunction, [None, None], None)
    def imply_expr() -> 'ExpressionTree':
        return ExpressionTree(Alphabet.implication, [None, None], None)
    def forall_expr(variable: str) -> 'ExpressionTree':
        return ExpressionTree(Alphabet.forall + variable, [None], None)
    def exists_expr(variable: str) -> 'ExpressionTree':
        return ExpressionTree(Alphabet.exists + variable, [None], None)

    def arity(self) -> int:
        return len(self.children)

    def add_child(self, new_expr: 'ExpressionTree'):
        self.children.append(new_expr)
        new_expr.parent = self

    # Helper Function
    # Replace Node A with Node B including the subtrees
    def replace(A: 'ExpressionTree', B: 'ExpressionTree'):
        B.parent = A.parent
        A.parent.children[A.parent.children.index(A)] = B

    # Helper Function
    # Only use left if self was created by _expr() methods
    # If you try use .left without populating the children array, it will throw an exception
    def get_left(self) -> 'ExpressionTree':
        return self.children[0]
    def set_left(self, value: 'ExpressionTree'):
        self.children[0] = value
        value.parent = self
    left = property(get_left, set_left)

    # Helper Function
    # Only call if self was created by _expr() methods
    # If you try use .right without populating the children array, it will throw an exception
    def get_right(self) -> 'ExpressionTree':
        return self.children[1]
    def set_right(self, value: 'ExpressionTree'):
        self.children[1] = value
        value.parent = self
    right = property(get_right, set_right)

    # Helper Function
    # Only call if self was created by _expr() methods
    # If you try use .child without populating the children array, it will throw an exception
    def get_child(self) -> 'ExpressionTree':
        return self.children[0]
    def set_child(self, value: 'ExpressionTree'):
        self.children[0] = value
        value.parent = self
    child = property(get_child, set_child)

    def as_tree_str(self, depth = 0) -> str:
        result = depth * "    " +  self.value + "\n"
        if self.arity() > 0:
            for child in self.children:
                result += child.as_tree_str(depth + 1)
        return result 

    def as_prefix_str(self) -> str:
        result = self.value
        if self.arity() > 0:
            result += Alphabet.descend_seperator
            for child in self.children[:-1]:
                result += child.as_prefix_str() + Alphabet.level_seperator
            result += self.children[-1].as_prefix_str() + Alphabet.ascend_seperator
        return result 
        
    def as_postfix_str(self) -> str:
        result = ""
        if self.arity() > 0:
            result += Alphabet.descend_seperator
            for child in self.children[:-1]:
                result += child.as_postfix_str() + Alphabet.level_seperator + " "
            result += self.children[-1].as_postfix_str() + Alphabet.ascend_seperator
        result += self.value
        return result 

    def as_standard_str(self) -> str:
        if self.value in [ Alphabet.equality, Alphabet.conjunction, Alphabet.disjunction, Alphabet.implication ]:
            result = Alphabet.descend_seperator + self.left.as_standard_str()
            result += " " + self.value + " "
            result += self.right.as_standard_str() + Alphabet.ascend_seperator
        else:
            result = self.value
            if self.arity() > 0:
                result += Alphabet.descend_seperator
                for child in self.children[:-1]:
                    result += child.as_standard_str() + Alphabet.level_seperator + " "
                result +=  self.children[-1].as_standard_str() + Alphabet.ascend_seperator

        return result

def expression_examples():
    forall_x = ExpressionTree.forall_expr("x")
    forall_y = ExpressionTree.forall_expr("y")
    forall_z = ExpressionTree.forall_expr("z")

    implication = ExpressionTree.imply_expr()

    top_and = ExpressionTree.and_expr()
    top_R = ExpressionTree("R", [], None)

    top_R_x = ExpressionTree("x", [], None)
    top_R_z = ExpressionTree("z", [], None)

    left_and = ExpressionTree.and_expr()
    left_R = ExpressionTree("R", [], None)
    left_R_x = ExpressionTree("x", [], None)
    left_R_y = ExpressionTree("y", [], None)

    right_R = ExpressionTree("R", [], None)
    right_R_x = ExpressionTree("y", [], None)
    right_R_y = ExpressionTree("z", [], None)

    right_and = ExpressionTree.and_expr()
    right_and_left_not = ExpressionTree.not_expr()
    right_and_left_equal = ExpressionTree.equals_expr()
    right_and_left_equal_x = ExpressionTree("x", [], None)
    right_and_left_equal_y = ExpressionTree("y", [], None)

    right_and_right_not = ExpressionTree.not_expr()
    right_and_right_equal = ExpressionTree.equals_expr()
    right_and_right_equal_y = ExpressionTree("x", [], None)
    right_and_right_equal_z = ExpressionTree("z", [], None)

    # forall_x.add_child(forall_y)
    forall_x.child = forall_y
    forall_y.child  = forall_z
    forall_z.child = implication
    implication.left = top_and
    implication.right = top_R

    top_R.add_child(top_R_x)
    top_R.add_child(top_R_z)

    top_and.left = left_and
    top_and.right = right_and

    left_and.left = left_R
    left_and.right = right_R

    left_R.add_child(left_R_x)
    left_R.add_child(left_R_y)

    right_R.add_child(right_R_x)
    right_R.add_child(right_R_y)

    right_and.left = right_and_left_not
    right_and_left_not.child = right_and_left_equal
    right_and_left_equal.left = right_and_left_equal_x
    right_and_left_equal.right = right_and_left_equal_y

    right_and.right = right_and_right_not
    right_and_right_not.child = right_and_right_equal
    right_and_right_equal.left = right_and_right_equal_y
    right_and_right_equal.right = right_and_right_equal_z

    print(forall_x.as_standard_str())
    print(forall_x.as_prefix_str())
    print(forall_x.as_postfix_str())
    # print(forall_x.as_tree_str())

# TODO: Part A
# ========================================================================================================================

def parse_prefix_string(prefix_str: str) -> ExpressionTree:
    """
        TODO: Part A 
    """
    pass

def well_formed_expression_type(expression_str: str) -> Literal["Formula", "Term", "None"]:
    """
        TODO: Part A Question 1
    """
    pass

def get_expression_signature_and_variables(expression: ExpressionTree, signature_and_vars: dict[str, set[str]]):
    """
        TODO: Part A Question 2
    """
    pass

def nnf_simplify(expression: ExpressionTree):
    """
        Convert expression into its negation-normal-form
        TODO: Part A Question 3
    """
    pass
    
def evaluate_expression(model: Model, expression: ExpressionTree, assignments: dict[str, object] = {}) -> object:
    """
        Evaluate expression with model and assignments
        TODO: Part A Question 4
    """
    pass

# TODO: Part B
# ========================================================================================================================

def construct_empty_formula(M: TuringMachine) -> ExpressionTree:
    """
        TODO: Part B Question 1
    """
    pass


def construct_state_formula(M: TuringMachine) -> ExpressionTree:
    """
        TODO: Part B Question 2
    """
    pass

def construct_symbol_formula(M: TuringMachine) -> ExpressionTree:
    """
        TODO: Part B Question 3
    """
    pass

def construct_cell_formula(M: TuringMachine) -> ExpressionTree:
    """
        TODO: Part B Question 4
    """
    pass

def construct_transitions_formula(M: TuringMachine) -> ExpressionTree:
    """
        TODO: Part B Question 5
    """
    pass

def construct_halt_formula(M: TuringMachine) -> ExpressionTree:
    """
        TODO: Part B Question 6
    """
    pass

def construct_machine_formula(M: TuringMachine) -> ExpressionTree:
    """
        TODO: Part B Question 7
    """
    pass