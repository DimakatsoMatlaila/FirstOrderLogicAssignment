import json
import sys

def encode_phi_epsilon(machine):
    initial_state = machine["initial_state"]

    # Find which symbol is written by the initial state in its transition
    first_write = None
    S0 = None
    S1 = None

    for trans in machine["transitions"]:
        cur_state, read_sym, next_state, write_sym, direction = trans
        if cur_state == initial_state:
            if first_write is None:
                first_write = write_sym
            if read_sym == 0:
                S0 = f"S[{write_sym}]"
            elif read_sym == 1:
                S1 = f"S[{write_sym}]"

    # Default fallback if we somehow missed a symbol
    if S0 is None:
        S0 = "S[0]"
    if S1 is None:
        S1 = "S[1]"

    Q0 = f"Q[{initial_state}]"

    # Construct φε
    # φε := (Q0(0) ∧ C(0, 1)) ∧ (S1(0, 0) ∧ ∀x((¬(x = 0)) → S0(0, x)))
    phi_epsilon = f"&(&({Q0}(0),C(0,1)),&({S1}(0,0),@x(>(!(=(x,0)),{S0}(0,x)))))"
    return phi_epsilon

if __name__ == "__main__":
    input_json = input()
    machine = json.loads(input_json)
    print(encode_phi_epsilon(machine))
