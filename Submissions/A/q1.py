import re

class Parser:
    def __init__(self, input_str):
        self.tokens = self.tokenize(input_str.replace(" ", ""))
        self.pos = 0

    def tokenize(self, s):
        tokens = []
        i = 0
        while i < len(s):
            if s[i] in ['@', '#', '&', '|', '!', '>', '=', '(', ')', ',', '[', ']']:
                tokens.append(s[i])
                i += 1
            elif s[i].isalpha():
                j = i
                while j < len(s) and (s[j].isalnum() or s[j] == '_'):
                    j += 1
                tokens.append(s[i:j])
                i = j
            elif s[i].isdigit():
                j = i
                while j < len(s) and s[j].isdigit():
                    j += 1
                tokens.append(s[i:j])
                i = j
            else:
                return []  
        return tokens

    def parse(self):
        if not self.tokens:
            return "None"
        try:
            result = self.parse_formula()
            if result and self.pos == len(self.tokens):
                return "Formula"
        except:
            pass

        self.pos = 0
        try:
            result = self.parse_term()
            if result and self.pos == len(self.tokens):
                return "Term"
        except:
            pass

        return "None"

    def parse_formula(self):
        if self.pos >= len(self.tokens):
            return None

        token = self.tokens[self.pos]

        if token in ['@', '#']:
            self.pos += 1
            if not self.expect_variable():
                return None
            if not self.match('('):
                return None
            sub = self.parse_formula()
            if sub is None or not self.match(')'):
                return None
            return ('quantifier', token, sub)

        elif token == '!':
            self.pos += 1
            if not self.match('('): return None
            sub = self.parse_formula()
            if sub is None or not self.match(')'): return None
            return ('not', sub)

        elif token in ['&', '|', '>', '=']:
            self.pos += 1
            if not self.match('('): return None
            left = self.parse_formula_or_term()
            if left is None: return None
            if not self.match(','): return None
            right = self.parse_formula_or_term()
            if right is None: return None
            if not self.match(')'): return None
            return ('binary', token, left, right)

        elif token == '(':
            self.pos += 1
            sub = self.parse_formula()
            if sub is None or not self.match(')'):
                return None
            return sub

        elif self.is_predicate():
            name = self.tokens[self.pos]
            self.pos += 1
            if self.pos < len(self.tokens) and self.tokens[self.pos] == '(':
                args = self.parse_args()
                if args is None:
                    return None
                return ('predicate', name, args)
            else:
                return ('predicate', name, [])

        elif re.fullmatch(r'^[A-Z]$', token):  
            self.pos += 1
            return ('predicate', token, [])

        return None

    def parse_formula_or_term(self):
        pos_backup = self.pos
        res = self.parse_formula()
        if res is not None:
            return res
        self.pos = pos_backup
        return self.parse_term()

    def parse_term(self):
        if self.pos >= len(self.tokens):
            return None

        token = self.tokens[self.pos]

        if token.isdigit():
            self.pos += 1
            return ('const', token)

        if re.fullmatch(r'^[a-z][a-z0-9]*$', token):
            name = token
            self.pos += 1
            if self.pos < len(self.tokens) and self.tokens[self.pos] == '(':
                args = self.parse_args()
                if args is None:
                    return None
                return ('func', name, args)
            else:
                return ('var', name)

        return None

    def parse_args(self):
        if not self.match('('):
            return None
        args = []
        if self.match(')'):
            return args  
        while True:
            if self.pos >= len(self.tokens):
                return None
            arg = self.parse_formula_or_term()
            if arg is None:
                return None
            args.append(arg)
            if self.match(','):
                continue
            elif self.match(')'):
                break
            else:
                return None
        return args

    def match(self, symbol):
        if self.pos < len(self.tokens) and self.tokens[self.pos] == symbol:
            self.pos += 1
            return True
        return False

    def expect_variable(self):
        if self.pos < len(self.tokens) and re.fullmatch(r'^[a-z]$', self.tokens[self.pos]):
            self.pos += 1
            return True
        return False

    def is_predicate(self):
        return self.pos < len(self.tokens) and re.fullmatch(r'^[A-Z][A-Z0-9]*$', self.tokens[self.pos])


def check_well_formed(input_str):
    parser = Parser(input_str)
    return parser.parse()


print(check_well_formed(input().strip()))