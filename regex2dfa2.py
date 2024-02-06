class State:
    def __init__(self, name):
        self.name = name
        self.transitions = {}

    def add_transition(self, symbol, state):
        if symbol in self.transitions:
            self.transitions[symbol].add(state)
        else:
            self.transitions[symbol] = {state}

def regex_to_dfa(regex):
    # Parse the regular expression and generate NFA
    # (We assume that the input regex is valid for simplicity)
    nfa_start, nfa_final = parse_regex(regex)

    # Convert NFA to DFA
    dfa_start = epsilon_closure({nfa_start})
    dfa_states = [dfa_start]
    unprocessed_states = [dfa_start]
    dfa_final = set()

    while unprocessed_states:
        current_state = unprocessed_states.pop()

        for symbol in get_alphabet(nfa_start, nfa_final):
            next_states = epsilon_closure(move(current_state, symbol, nfa_start))
            
            if next_states not in dfa_states:
                dfa_states.append(next_states)
                unprocessed_states.append(next_states)
            
            if nfa_final in next_states:
                dfa_final.add(next_states)

    # Generate DFA table
    dfa_table = []
    alphabet = get_alphabet(nfa_start, nfa_final)

    for state_set in dfa_states:
        row = [state_set]
        for symbol in alphabet:
            next_state_set = epsilon_closure(move(state_set, symbol, nfa_start))
            row.append(next_state_set)
        dfa_table.append(row)

    # Return the relevant values
    return dfa_table, dfa_start, dfa_final



def epsilon_closure(states):
    closure = set(states)
    stack = list(states)

    while stack:
        current_state = stack.pop()

        if epsilon in current_state.transitions:
            for next_state in current_state.transitions[epsilon]:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)

    return frozenset(closure)


def move(states, symbol, nfa_start):
    result = set()

    for state in states:
        if symbol in state.transitions:
            result.update(state.transitions[symbol])

    return result


def get_alphabet(states, nfa_final):
    alphabet = set()

    def collect_symbols(states):
        if isinstance(states, State):
            states = {states}

        for state in states:
            if state not in visited_states:
                visited_states.add(state)

                for symbol in state.transitions:
                    alphabet.add(symbol)

                    for next_state in state.transitions[symbol]:
                        collect_symbols({next_state})


    visited_states = set()
    collect_symbols(states)

    if epsilon in alphabet:
        alphabet.remove(epsilon)

    return sorted(list(alphabet))



def parse_regex(regex):
    # Placeholder logic, replace with your actual regex to NFA conversion
    # For simplicity, returning two placeholder states
    start_state = State("start")
    final_state = State("final")
    start_state.add_transition(regex, final_state)
    return start_state, final_state



# Constants
epsilon = "ε"

# Example usage
regex = "a.(b|c)*"
dfa_table, dfa_start, dfa_final = regex_to_dfa(regex)

# Print DFA table
print("\nDFA Table:")
alphabet = get_alphabet(dfa_start, dfa_final)
print("State\t", "\t".join(alphabet))

for i, row in enumerate(dfa_table):
    state_str = ", ".join(str(list(state)[0].name) if state else "Empty" for state in row)
    print(f"{i}\t{state_str}")

print("\nStart State:", dfa_start)
print("Final States:", ", ".join(map(str, dfa_final)))