import json
def phi_HALT(tm):
    num_states = len(tm.get("states", []))
    if num_states > 2:
        return "#x(|(Q[1](x), Q[2](x)))"
    if num_states > 1:
        return "#x(Q[1](x))"
    return "#x(Q[0](x))" 
tm = json.loads(input())
print(phi_HALT(tm))
   

   
