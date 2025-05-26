import json
#Custom Code for Question 3
def build_formula(data):
    syms = data["alphabet"]
    count = len(syms)
    exprs = []
    for idx in range(count):
        neg_exprs = [f"!(S[{j}](x,y))" for j in range(count) if j != idx]#expressions for j != idx
        # Base expression for S[idx](x,y)
        base_expr = f"S[{idx}](x,y)"
        if neg_exprs:
            base_expr = f"&({base_expr},{conj_nested(neg_exprs)})"
        exprs.append(base_expr)
    return f"@x(@y({disj_nested(exprs)}))"

def conj_nested(lst):
    if not lst:
        return ""
    acc = lst[0]
    for elem in lst[1:]:
        acc = f"&({acc},{elem})"
    return acc

def disj_nested(lst):
    if not lst:
        return ""
    acc = lst[0]
    for elem in lst[1:]:
        acc = f"|({acc},{elem})"
    return acc

tm = json.loads(input())
print(build_formula(tm))