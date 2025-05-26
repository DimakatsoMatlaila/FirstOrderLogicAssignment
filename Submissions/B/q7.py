import json

def phi_epsilon(tm):
    initial_state = tm["initial_state"]
    first_write = None
    S0 = None
    S1 = None

    for trans in tm["transitions"]:
        cur_state, read_sym, next_state, write_sym, direction = trans
        if cur_state == initial_state:
            if first_write is None:
                first_write = write_sym
            if read_sym == 0:
                S0 = f"S[{write_sym}]"
            elif read_sym == 1:
                S1 = f"S[{write_sym}]"

    if S0 is None:
        S0 = "S[0]"
    if S1 is None:
        S1 = "S[1]"

    Q0 = f"Q[{initial_state}]"
    phi_epsilon = f"&(&({Q0}(0),C(0,1)),&({S1}(0,0),@x(>(!(=(x,0)),{S0}(0,x)))))"
    return phi_epsilon

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

def phi_delta(tm):
    syms = tm["alphabet"]
    count = len(syms)
    exprs = []
    for idx in range(count):
        neg_exprs = [f"!(S[{j}](x,y))" for j in range(count) if j != idx]
        base_expr = f"S[{idx}](x,y)"
        if neg_exprs:
            base_expr = f"&({base_expr},{conj_nested(neg_exprs)})"
        exprs.append(base_expr)
    return f"@x(@y({disj_nested(exprs)}))"

def phi_C(tm):
    implication = ">(C(x,z),=(z,y))"
    forall_z = f"@z({implication})"
    conj = f"&(C(x,y),{forall_z})"
    exists_y = f"#y({conj})"
    phi_C = f"@x({exists_y})"
    return phi_C

def phi_transitions(tm):
    transitions = tm["transitions"]
    alphabet_size = len(tm["alphabet"])
    phi_I_list = []
    for transition in transitions:
        current_state, read_symbol, next_state, write_symbol, direction = transition
        antecedent_parts = [
            f"Q[{current_state}](x)",
            "C(x,y)",
            f"S[{read_symbol}](x,y)"
        ]
        antecedent = build_conjunction(antecedent_parts)
        if direction == -1:
            consequent = build_left_consequent(next_state, write_symbol, alphabet_size)
        else:
            consequent = build_right_consequent(next_state, write_symbol, alphabet_size)
        implication = f">({antecedent},{consequent})"
        phi_I = f"@x(@y({implication}))"
        phi_I_list.append(phi_I)
    return build_conjunction(phi_I_list)

def build_left_consequent(next_state, write_symbol, alphabet_size):
    main_parts = [
        f"Q[{next_state}](s(x))",
        "#v(&(=(s(v),y),C(s(x),v)))",
        f"S[{write_symbol}](s(x),y)"
    ]
    main_conjunction = build_conjunction(main_parts)
    preservation_implications = []
    for k in range(alphabet_size):
        preservation_implications.append(f">(S[{k}](x,z),S[{k}](s(x),z))")
    preservation_conjunction = build_conjunction(preservation_implications)
    preservation_implication = f">(!(=(z,y)),{preservation_conjunction})"
    preservation_forall = f"@z({preservation_implication})"
    return f"&({main_conjunction},{preservation_forall})"

def build_right_consequent(next_state, write_symbol, alphabet_size):
    main_parts = [
        f"Q[{next_state}](s(x))",
        "C(s(x),s(y))",
        f"S[{write_symbol}](s(x),y)"
    ]
    main_conjunction = build_conjunction(main_parts)
    preservation_implications = []
    for k in range(alphabet_size):
        preservation_implications.append(f">(S[{k}](x,z),S[{k}](s(x),z))")
    preservation_conjunction = build_conjunction(preservation_implications)
    preservation_implication = f">(!(=(z,y)),{preservation_conjunction})"
    preservation_forall = f"@z({preservation_implication})"
    return f"&({main_conjunction},{preservation_forall})"

def phi_halt(tm):
    num_states = len(tm.get("states", []))
    if num_states > 2:
        return "#x(|(Q[1](x),Q[2](x)))"
    if num_states > 1:
        return "#x(Q[1](x))"
    return "#x(Q[0](x))"

def build_conjunction(formulas):
    if not formulas:
        return ""
    if len(formulas) == 1:
        return formulas[0]
    result = formulas[0]
    for formula in formulas[1:]:
        result = f"&({result},{formula})"
    return result

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

def phi_M(tm):
    phi_eps = phi_epsilon(tm)
    phi_q = phi_Q(tm)
    phi_del = phi_delta(tm)
    phi_c = phi_C(tm)
    phi_trans = phi_transitions(tm)
    phi_h = phi_halt(tm)
    premises = build_conjunction([phi_eps, phi_q, phi_del, phi_c, phi_trans])
    return f">({premises},{phi_h})"

tm = json.loads(input().strip())
print(phi_M(tm))
