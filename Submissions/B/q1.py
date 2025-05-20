import json
import sys

class ExpressionTree:
    value: str
    children: list['ExpressionTree']
    parent: 'ExpressionTree'

    def __init__(self, value: str, children: list['ExpressionTree'], parent: 'ExpressionTree'):
        self.value = value
        self.children = children
        self.parent = parent

    def add_child(self, new_expr: 'ExpressionTree'):
        self.children.append(new_expr)
        new_expr.parent = self

    def as_prefix_str(self) -> str:
        result = self.value
        if self.children:
            result += "("
            for i, child in enumerate(self.children):
                if i > 0:
                    result += ","
                result += child.as_prefix_str()
            result += ")"
        return result

class TuringMachine:
    states: list[int]
    alphabet: list[int]
    transitions: list[tuple[int, int, int, int, int]]
    initial_state: int
    accept_state: int
    reject_state: int

    @staticmethod
    def from_json(json_string: str) -> 'TuringMachine':
        data = json.loads(json_string)
        tm = TuringMachine()
        tm.states = data['states']
        tm.alphabet = data['alphabet']
        tm.transitions = [tuple(t) for t in data['transitions']]
        tm.initial_state = data['initial_state']
        tm.accept_state = data['accept_state']
        tm.reject_state = data['reject_state']
        return tm

def construct_phi_epsilon(tm: TuringMachine) -> ExpressionTree:
    # Q_initial(0)
    q_initial = tm.initial_state
    q_pred = ExpressionTree(f"Q[{q_initial}]", [], None)
    q_pred.add_child(ExpressionTree("0", [], None))

    # C(0,1)
    c_pred = ExpressionTree("C", [], None)
    c_pred.add_child(ExpressionTree("0", [], None))
    c_pred.add_child(ExpressionTree("1", [], None))

    # S_1(0,0) - using the second symbol (end-of-tape)
    s1_pred = ExpressionTree("S[1]", [], None)
    s1_pred.add_child(ExpressionTree("0", [], None))
    s1_pred.add_child(ExpressionTree("0", [], None))

    # S_0(0,x) - using the first symbol (blank)
    s0_pred = ExpressionTree("S[0]", [], None)
    s0_pred.add_child(ExpressionTree("0", [], None))
    s0_pred.add_child(ExpressionTree("x", [], None))

    # x=0
    equals = ExpressionTree("=", [], None)
    equals.add_child(ExpressionTree("x", [], None))
    equals.add_child(ExpressionTree("0", [], None))

    # ¬(x=0)
    not_equals = ExpressionTree("!", [], None)
    not_equals.add_child(equals)

    # Implication: ¬(x=0) → S_0(0,x)
    implication = ExpressionTree(">", [], None)
    implication.add_child(not_equals)
    implication.add_child(s0_pred)

    # ∀x(...)
    forall_x = ExpressionTree("@x", [], None)
    forall_x.add_child(implication)

    # Combine parts
    and1 = ExpressionTree("&", [], None)
    and1.add_child(q_pred)
    and1.add_child(c_pred)

    and2 = ExpressionTree("&", [], None)
    and2.add_child(s1_pred)
    and2.add_child(forall_x)

    top_and = ExpressionTree("&", [], None)
    top_and.add_child(and1)
    top_and.add_child(and2)

    return top_and

def main():
    json_str = sys.stdin.read()
    tm = TuringMachine.from_json(json_str)
    phi_epsilon = construct_phi_epsilon(tm)
    print(phi_epsilon.as_prefix_str())

if __name__ == "__main__":
    main()