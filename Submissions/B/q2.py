import json
def phi_Q(tm):
    n = len(tm["states"])
    def conj(xs):
        r = xs[0]
        for x in xs[1:]:
            r = f"&({r},{x})"
        return r
    def disj(xs):
        r = xs[0]
        for x in xs[1:]:
            r = f"|({r},{x})"
        return r
    terms = []
    for i in range(n):
        negs = [f"!(Q[{j}](x))" for j in range(n) if j != i]
        q = f"Q[{i}](x)"
        t = q if not negs else f"&({q},{conj(negs)})"
        terms.append(t)
    return f"@x({disj(terms)})"

tm = json.loads(input())
print(phi_Q(tm))