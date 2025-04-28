import json
f=open('regex.json')
reg=json.load(f)
f.close()
def postfix(expresie):
    priority={"|":0,".":1,"?":2,"+":3,"*":4}
    stack=[]
    output=[]
    for c in expresie:
        if c=="(":
            stack.append(c)
        elif c==")":
            while stack[-1]!="(":
                output.append(stack.pop())
            stack.pop()
        elif c in priority.keys():
            while stack and stack[-1]!="(" and priority[c]<=priority[stack[-1]]:
                output.append(stack.pop())
            stack.append(c)
        else:
            output.append(c)
    while stack:
        output.append(stack.pop())
    return "".join(output)

counter=0
def thompson(postfix):
    global counter
    counter=0
    stack = []

    def new_state():
        global counter
        s = f"q{counter}"
        counter += 1
        return s

    for c in postfix:
        if c == '.':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            transitions = {}
            for state in nfa1["transitions"]:
                transitions[state] = {}
                for simb in nfa1["transitions"][state]:
                    transitions[state][simb] = set(nfa1["transitions"][state][simb])
            for state in nfa2["transitions"]:
                if state not in transitions:
                    transitions[state] = {}
                for simb in nfa2["transitions"][state]:
                    if simb not in transitions[state]:
                        transitions[state][simb] = set()
                    transitions[state][simb].update(nfa2["transitions"][state][simb])
            if nfa1["accept"] not in transitions:
                transitions[nfa1["accept"]] = {}
            if None not in transitions[nfa1["accept"]]:
                transitions[nfa1["accept"]][None] = set()
            transitions[nfa1["accept"]][None].add(nfa2["start"])
            stack.append({
                "start": nfa1["start"],
                "accept": nfa2["accept"],
                "states": nfa1["states"] | nfa2["states"],
                "alphabet": nfa1["alphabet"] | nfa2["alphabet"],
                "transitions": transitions
            })
        elif c == '|':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            start = new_state()
            accept = new_state()
            transitions = {}
            for nfa in [nfa1, nfa2]:
                for state in nfa["transitions"]:
                    if state not in transitions:
                        transitions[state] = {}
                    for simb in nfa["transitions"][state]:
                        if simb not in transitions[state]:
                            transitions[state][simb] = set()
                        transitions[state][simb].update(nfa["transitions"][state][simb])
            transitions[start] = {None: {nfa1["start"], nfa2["start"]}}
            for old_accept in [nfa1["accept"], nfa2["accept"]]:
                if old_accept not in transitions:
                    transitions[old_accept] = {}
                if None not in transitions[old_accept]:
                    transitions[old_accept][None] = set()
                transitions[old_accept][None].add(accept)
            stack.append({
                "start": start,
                "accept": accept,
                "states": nfa1["states"] | nfa2["states"] | {start, accept},
                "alphabet": nfa1["alphabet"] | nfa2["alphabet"],
                "transitions": transitions
            })
        elif c == '*':
            nfa1 = stack.pop()
            start = new_state()
            accept = new_state()
            transitions = {}
            for state in nfa1["transitions"]:
                transitions[state] = {}
                for simb in nfa1["transitions"][state]:
                    transitions[state][simb] = set(nfa1["transitions"][state][simb])
            transitions[start] = {None: {nfa1["start"], accept}}
            if nfa1["accept"] not in transitions:
                transitions[nfa1["accept"]] = {}
            if None not in transitions[nfa1["accept"]]:
                transitions[nfa1["accept"]][None] = set()
            transitions[nfa1["accept"]][None].update({nfa1["start"], accept})
            stack.append({
                "start": start,
                "accept": accept,
                "states": nfa1["states"] | {start, accept},
                "alphabet": nfa1["alphabet"],
                "transitions": transitions
            })
        elif c == '+':
            nfa1 = stack.pop()
            start = new_state()
            accept = new_state()
            transitions = {}
            for state in nfa1["transitions"]:
                transitions[state] = {}
                for simb in nfa1["transitions"][state]:
                    transitions[state][simb] = set(nfa1["transitions"][state][simb])
            transitions[start] = {None: {nfa1["start"]}}
            if nfa1["accept"] not in transitions:
                transitions[nfa1["accept"]] = {}
            if None not in transitions[nfa1["accept"]]:
                transitions[nfa1["accept"]][None] = set()
            transitions[nfa1["accept"]][None].update({nfa1["start"], accept})
            stack.append({
                "start": start,
                "accept": accept,
                "states": nfa1["states"] | {start, accept},
                "alphabet": nfa1["alphabet"],
                "transitions": transitions
            })
        elif c == '?':
            nfa1 = stack.pop()
            start = new_state()
            accept = new_state()
            transitions = {}
            for state in nfa1["transitions"]:
                transitions[state] = {}
                for simb in nfa1["transitions"][state]:
                    transitions[state][simb] = set(nfa1["transitions"][state][simb])
            transitions[start] = {None: {nfa1["start"], accept}}
            if nfa1["accept"] not in transitions:
                transitions[nfa1["accept"]] = {}
            if None not in transitions[nfa1["accept"]]:
                transitions[nfa1["accept"]][None] = set()
            transitions[nfa1["accept"]][None].add(accept)
            stack.append({
                "start": start,
                "accept": accept,
                "states": nfa1["states"] | {start, accept},
                "alphabet": nfa1["alphabet"],
                "transitions": transitions
            })
        else:
            start = new_state()
            accept = new_state()
            transitions = {}
            transitions[start] = {c: {accept}}

            stack.append({
                "start": start,
                "accept": accept,
                "states": {start, accept},
                "alphabet": {c},
                "transitions": transitions
            })

    nfa = stack.pop()
    return {
        "states": nfa["states"],
        "alphabet": nfa["alphabet"],
        "transitions": nfa["transitions"],
        "start": nfa["start"],
        "accept": {nfa["accept"]}
    }

def epsilon(transitions, states):
    stack = list(states)
    nep = set(states)
    while stack:
        state = stack.pop()
        if state in transitions and None in transitions[state]:
            for next_state in transitions[state][None]:
                if next_state not in nep:
                    nep.add(next_state)
                    stack.append(next_state)
    return nep

def convert_nfa_to_dfa(nfa_config):
    alphabet = nfa_config["alphabet"]
    transitions = nfa_config["transitions"]
    start = nfa_config["start"]
    accept = nfa_config["accept"]

    dfa_start = frozenset(epsilon(transitions, {start}))

    dfa_states = []
    dfa_transitions = {}
    dfa_accept = set()

    unprocessed = [dfa_start]
    while unprocessed:
        current = unprocessed.pop(0)
        if current not in dfa_states:
            dfa_states.append(current)

        if any(state in accept for state in current):
            dfa_accept.add(current)

        for simbol in alphabet:
            move_result = set()
            for state in current:
                if state in transitions and simbol in transitions[state]:
                    move_result.update(transitions[state][simbol])

            if not move_result:
                continue

            nep = epsilon(transitions, move_result)
            nep = frozenset(nep)

            if current not in dfa_transitions:
                dfa_transitions[current] = {}
            dfa_transitions[current][simbol] = nep

            if nep not in dfa_states and nep not in unprocessed:
                unprocessed.append(nep)

    dfa = {
        "states": dfa_states,
        "alphabet": alphabet,
        "transitions": dfa_transitions,
        "start": dfa_start,
        "accept": dfa_accept
    }
    return dfa

def dfa_accept(dfa, cuv):
    stc = dfa["start"]
    for lit in cuv:
        if lit not in dfa["transitions"][stc]:
            return False
        else:
            stc = dfa["transitions"][stc][lit]
    if stc in dfa["accept"]:
        return True
    else:
        return False


for re in reg:
    regex=""
    pc=""
    for c in re['regex']:
        if pc!="" and (pc.isalnum() or pc in ")*+?") and (c=="(" or c.isalnum()):
            regex += "."
        regex+=c
        pc=c

    post = postfix(regex)
    nfa = thompson(post)
    dfa = convert_nfa_to_dfa(nfa)

    print(f"Regex {re['name']}:")
    for test in re["test_strings"]:
        input = test["input"]
        expected = test["expected"]
        result = dfa_accept(dfa, input)
        print(f"     Input: '{input}'   Expected: {expected}   Result: {result}",end="   ")
        if result == expected:
            print("OK")
        else:
            print("GRESIT")
