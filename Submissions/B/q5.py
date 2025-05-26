import json

def phi_delta(tm):
    transitions = tm["transitions"]
    n = len(tm["alphabet"])
    formulas = []
    for t in transitions:
        q, a, q1, b, d = t
        ant = conj([
            f"Q[{q}](x)",
            "C(x,y)",
            f"S[{a}](x,y)"
        ])
        if d == -1:
            cons = left(q1, b, n)
        else:
            cons = right(q1, b, n)
        imp = f">({ant},{cons})"
        formulas.append(f"@x(@y({imp}))")
    return conj(formulas)

def left(q, b, n):
    main = conj([
        f"Q[{q}](s(x))",
        "#v(&(=(s(v),y),C(s(x),v)))",
        f"S[{b}](s(x),y)"
    ])
    pres = conj([
        f">(S[{k}](x,z),S[{k}](s(x),z))" for k in range(n)
    ])
    allz = f"@z(>(!(=(z,y)),{pres}))"
    return f"&({main},{allz})"

def right(q, b, n):
    main = conj([
        f"Q[{q}](s(x))",
        "C(s(x),s(y))",
        f"S[{b}](s(x),y)"
    ])
    pres = conj([
        f">(S[{k}](x,z),S[{k}](s(x),z))" for k in range(n)
    ])
    allz = f"@z(>(!(=(z,y)),{pres}))"
    return f"&({main},{allz})"

def conj(fs):
    if not fs:
        return ""
    if len(fs) == 1:
        return fs[0]
    r = fs[0]
    for f in fs[1:]:
        r = f"&({r},{f})"
    return r

tm = json.loads(input().strip())
print(phi_delta(tm))
