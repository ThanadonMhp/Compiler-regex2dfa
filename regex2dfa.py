import regex as re
import graphviz

def regex_to_dfa(regex):
    regex_obj = re.compile(regex)
    pattern = regex_obj.pattern
    print("Pattern:", pattern)

    stack = []

    for token in re.finditer(r'\X', pattern):
        symbol = token.group()
        print("Processing symbol:", symbol)

        if symbol.isalnum():
            stack.append({'label': symbol, 'transitions': {}})
        elif symbol == '.':
            if len(stack) >= 2:
                second_operand = stack.pop()
                first_operand = stack.pop()
                first_operand['transitions'][''] = second_operand
                stack.append(first_operand)
            else:
                raise ValueError("Insufficient operands for concatenation")
        elif symbol == '|':
            if len(stack) >= 2:
                second_operand = stack.pop()
                first_operand = stack.pop()
                new_start_state = {'label': '', 'transitions': {'': first_operand, '': second_operand}}
                new_end_state = {'label': '', 'transitions': {}}
                first_operand['transitions'][''] = new_end_state
                second_operand['transitions'][''] = new_end_state
                stack.append(new_start_state)
            else:
                raise ValueError("Insufficient operands for union")
        elif symbol == '*':
            if len(stack) >= 1:
                operand = stack.pop()
                new_start_state = {'label': '', 'transitions': {'': operand}}
                new_end_state = {'label': '', 'transitions': {'': operand, '': new_start_state}}
                operand['transitions'][''] = new_end_state
                stack.append(new_start_state)
            else:
                raise ValueError("Insufficient operand for Kleene star")
        elif symbol == '(':
            stack.append({'type': 'subpattern', 'label': '', 'transitions': {}})
        elif symbol == ')':
            # Ensure there are enough operands for union when encountering ')'
            if len(stack) >= 2 and stack[-2].get('type') == 'subpattern':
                second_operand = stack.pop()
                first_operand = stack.pop()
                new_start_state = {'label': '', 'transitions': {'': first_operand, '': second_operand}}
                new_end_state = {'label': '', 'transitions': {}}
                first_operand['transitions'][''] = new_end_state
                second_operand['transitions'][''] = new_end_state
                stack.append(new_start_state)
            else:
                raise ValueError("Insufficient operands for union")

    if len(stack) != 1:
        raise ValueError("Invalid regular expression")

    dfa = stack.pop()

    return dfa

# The rest of the code remains the same


def draw_dfa(dfa, filename='dfa'):
    dot = graphviz.Digraph(format='png')
    visited_states = set()

    def add_states_and_transitions(state):
        if id(state) not in visited_states:
            visited_states.add(id(state))
            dot.node(str(id(state)), label=state['label'], shape='circle')
            for label, next_state in state['transitions'].items():
                dot.edge(str(id(state)), str(id(next_state)), label=label)
                add_states_and_transitions(next_state)

    add_states_and_transitions(dfa)
    dot.render(filename, cleanup=True)

# Example usage:
regex_input = "(a|b)*abb"
dfa_result = regex_to_dfa(regex_input)
draw_dfa(dfa_result, filename='example_dfa')
