import json

def encode_phi_epsilon(machine):
    init = machine["initial_state"]
    s0 = s1 = None
    for state, read, _, write, _ in machine["transitions"]:
        if state == init:
            if read == 0:
                s0 = f"S[{write}]"
            elif read == 1:
                s1 = f"S[{write}]"
    s0 = s0 or "S[0]"
    s1 = s1 or "S[1]"
    q0 = f"Q[{init}]"
    return f"&(&({q0}(0),C(0,1)),&({s1}(0,0),@x(>(!(=(x,0)),{s0}(0,x)))))"

print(encode_phi_epsilon(json.loads(input())))
