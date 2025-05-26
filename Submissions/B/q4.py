import json
def build_phi_C(tm):
    implication = ">(C(x,z),=(z,y))"
    forall_z = f"@z({implication})"
    conj = f"&(C(x,y),{forall_z})"
    exists_y = f"#y({conj})"
    phi_C = f"@x({exists_y})"
    return phi_C 
tm = json.loads(input().strip())
print(build_phi_C(tm))