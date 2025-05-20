import re

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

def parse_prefix_string(prefix_str: str) -> ExpressionTree:
    i = 0

    def parse():
        nonlocal i
        while i < len(prefix_str) and prefix_str[i] == " ":
            i += 1

        # Read value
        start = i
        while i < len(prefix_str) and prefix_str[i] not in "(),":
            i += 1
        value = prefix_str[start:i]

        node = ExpressionTree(value, [], None)

        while i < len(prefix_str) and prefix_str[i] == " ":
            i += 1

        if i < len(prefix_str) and prefix_str[i] == '(':
            i += 1
            while True:
                child = parse()
                node.add_child(child)
                while i < len(prefix_str) and prefix_str[i] == " ":
                    i += 1
                if i < len(prefix_str) and prefix_str[i] == ',':
                    i += 1
                elif i < len(prefix_str) and prefix_str[i] == ')':
                    i += 1
                    break
        return node

    return parse()

def get_expression_signature_and_variables(expression: ExpressionTree, signature_and_vars: dict[str, set[str]]):
    value = expression.value

    # Variable: ^[a-z]+(\[\d+\])?$
    if re.fullmatch(r"^[a-z]+(\[\d+\])?$", value):
        if expression.arity() == 0:
            signature_and_vars["variables"].add(value)
        else:
            signature_and_vars["functions"].add(value)
    # Constant: ^(?<!\[)[0-9]+(?!\[)$
    elif re.fullmatch(r"^(?<!\[)[0-9]+(?!\[)$", value):
        signature_and_vars["constants"].add(value)
    # Predicate: ^[A-Z]+(\[\d+\])?$
    elif re.fullmatch(r"^[A-Z]+(\[\d+\])?$", value):
        signature_and_vars["predicates"].add(value)

    for child in expression.children:
        get_expression_signature_and_variables(child, signature_and_vars)

def nnf_simplify(expression: ExpressionTree) -> ExpressionTree:
    # Apply recursively to children first
    for i in range(len(expression.children)):
        expression.children[i] = nnf_simplify(expression.children[i])
        expression.children[i].parent = expression

    # === Implication (d): A → B → (!A | B)
    if expression.value == Alphabet.implication:
        not_A = ExpressionTree.not_expr()
        not_A.child = expression.left
        new_or = ExpressionTree.or_expr()
        new_or.left = not_A
        new_or.right = expression.right
        return nnf_simplify(new_or)

    # === Double Negation (a): !(!(A)) → A
    if expression.value == Alphabet.negation:
        inner = expression.child
        if inner.value == Alphabet.negation:
            return nnf_simplify(inner.child)

        # === De Morgan’s Laws
        # (b): !(A | B) → (!A & !B)
        if inner.value == Alphabet.disjunction:
            left = ExpressionTree.not_expr()
            left.child = inner.left
            right = ExpressionTree.not_expr()
            right.child = inner.right
            new_and = ExpressionTree.and_expr()
            new_and.left = nnf_simplify(left)
            new_and.right = nnf_simplify(right)
            return new_and

        # (c): !(A & B) → (!A | !B)
        if inner.value == Alphabet.conjunction:
            left = ExpressionTree.not_expr()
            left.child = inner.left
            right = ExpressionTree.not_expr()
            right.child = inner.right
            new_or = ExpressionTree.or_expr()
            new_or.left = nnf_simplify(left)
            new_or.right = nnf_simplify(right)
            return new_or

        # === Quantifier negation (e) and (f)
        if inner.value.startswith(Alphabet.forall):
            var = inner.value[1:]
            not_inner = ExpressionTree.not_expr()
            not_inner.child = inner.child
            exists_expr = ExpressionTree.exists_expr(var)
            exists_expr.child = nnf_simplify(not_inner)
            return exists_expr

        if inner.value.startswith(Alphabet.exists):
            var = inner.value[1:]
            not_inner = ExpressionTree.not_expr()
            not_inner.child = inner.child
            forall_expr = ExpressionTree.forall_expr(var)
            forall_expr.child = nnf_simplify(not_inner)
            return forall_expr

    return expression
def main():
    t = input()

    
    expr = parse_prefix_string(t)
    simplified = nnf_simplify(expr)
    print(simplified.as_prefix_str())

if __name__ == "__main__":
    main()
