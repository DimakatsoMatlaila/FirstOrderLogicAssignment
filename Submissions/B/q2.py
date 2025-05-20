import json

def construct_phi_Q(machine):
    states = sorted(machine["states"])  # Sort the states to ensure consistent order
    n = len(states)
    terms = []
    for k in states:
        other_states = [j for j in states if j != k]
        neg_terms = [f"!Q[{j}](x)" for j in other_states]
        if not neg_terms:
            term = f"Q[{k}](x)"
        else:
            conj = create_conjunction(neg_terms)
            term = f"&(Q[{k}](x),{conj})"
        terms.append(term)
    disj = create_disjunction(terms)
    return f"@x({disj})" if disj else ""

def create_conjunction(terms):
    if not terms:
        return ""
    conj = terms[0]
    for term in terms[1:]:
        conj = f"&({conj},{term})"
    return conj

def create_disjunction(terms):
    if not terms:
        return ""
    disj = terms[0]
    for term in terms[1:]:
        disj = f"|({disj},{term})"
    return disj

if __name__ == "__main__":
    input_json = input().strip()
    machine = json.loads(input_json)
    print(construct_phi_Q(machine))