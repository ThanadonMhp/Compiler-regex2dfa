def thompson(regex_str):
    def helper(i, start_state, accepting):
        if i == len(regex_str):
            return start_state, accepting
        if regex_str[i] in 'ab':
            end_state = len(states)
            states.append([(start_state, regex_str[i])])
            return end_state, accepting
        elif regex_str[i] == '.':
            end_state = len(states)
            states.append([(q, symbol) for q in start_state for symbol in alphabet])
            return end_state, accepting
        elif regex_str[i] == '|':
            end_state1, accepting1 = helper(i + 1, start_state, accepting)
            end_state2, accepting2 = helper(i + 1, start_state, False)
            states.append(states[start_state] + states[end_state1] + states[end_state2])
            return max(end_state1, end_state2) + 1, accepting1 or accepting2
        elif regex_str[i] == '*':
            start_state2 = len(states)
            end_state, accepting = helper(i + 1, start_state2, accepting)
            states.append(states[start_state] + states[end_state] + [(end_state, '')])
            return max(start_state2, end_state) + 1, accepting
        elif regex_str[i] == '^':
            end_state, accepting = helper(i + 1, start_state, accepting and len(start_state) == 1 and start_state[0] == (0, ''))
            return end_state, accepting
        else:
            raise ValueError("Invalid character")

    states = []
    alphabet = set(c for c in regex_str if c not in '.*|^')
    start_state, accepting = helper(0, 0, False)

    # Create DFA table
    alphabet_list = list(alphabet)  # Create a list from the set
    dfa_table = []
    for state in range(len(states)):
        row = [-1] * len(alphabet_list)
        for transition in states[state]:
            symbol, char = transition
            if char in alphabet_list:
                row[alphabet_list.index(char)] = symbol
        dfa_table.append(row)

    return dfa_table, accepting

# Example usage
regex_str = "ab|ba*"
dfa_table, accepting = thompson(regex_str)

print("DFA Table:")
for row in dfa_table:
    print(row)

print("Accepting state:", accepting)
