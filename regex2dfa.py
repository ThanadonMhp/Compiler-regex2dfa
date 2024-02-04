import regex as re
import graphviz

def regex_to_dfa(regex):
    # Compile the regular expression
    regex_obj = re.compile(regex)

    # Get the pattern from the compiled regex
    pattern = regex_obj.pattern
    print("Pattern:", pattern)

    # Create a stack to build the DFA
    stack = []

    for token in re.finditer(r'\X', pattern):
        symbol = token.group()
        print("Processing symbol:", symbol)

        if symbol.isalnum():
            # If it's a literal symbol, create a new state and push it onto the stack
            stack.append({'label': symbol, 'transitions': {}})
        elif symbol == '.':
            # Concatenation operation
            if len(stack) >= 2:
                second_operand = stack.pop()
                first_operand = stack.pop()
                # Connect the end state of the first operand to the start state of the second operand
                first_operand['transitions'][''] = second_operand
                # Push the concatenated expression onto the stack
                stack.append(first_operand)
            else:
                raise ValueError("Insufficient operands for concatenation")
        elif symbol == '|':
            # Union operation
            while len(stack) >= 2 and stack[-2].get('type') == 'subpattern':
                second_operand = stack.pop()
                first_operand = stack.pop()
                # Create a new start state connected to the start states of the operands
                new_start_state = {'label': '', 'transitions': {'': first_operand, '': second_operand}}
                # Create a new end state connected to the end states of the operands
                new_end_state = {'label': '', 'transitions': {}}
                first_operand['transitions'][''] = new_end_state
                second_operand['transitions'][''] = new_end_state
                # Push the union expression onto the stack
                stack.append(new_start_state)
            if len(stack) >= 2:
                second_operand = stack.pop()
                first_operand = stack.pop()
                # Create a new start state connected to the start states of the operands
                new_start_state = {'label': '', 'transitions': {'': first_operand, '': second_operand}}
                # Create a new end state connected to the end states of the operands
                new_end_state = {'label': '', 'transitions': {}}
                first_operand['transitions'][''] = new_end_state
                second_operand['transitions'][''] = new_end_state
                # Push the union expression onto the stack
                stack.append(new_start_state)
            else:
                raise ValueError("Insufficient operands for union")
        elif symbol == '*':
            # Kleene star operation
            if len(stack) >= 1:
                operand = stack.pop()
                # Create a new start state connected to the operand's start state
                new_start_state = {'label': '', 'transitions': {'': operand}}
                # Create a new end state connected to the operand's start and end states
                new_end_state = {'label': '', 'transitions': {'': operand, '': new_start_state}}
                operand['transitions'][''] = new_end_state
                # Push the Kleene star expression onto the stack
                stack.append(new_start_state)
            else:
                raise ValueError("Insufficient operand for Kleene star")
        elif symbol == '(':
            # Mark the beginning of a subpattern
            stack.append({'type': 'subpattern'})

    # The final DFA is on top of the stack
    dfa = stack.pop()

    return dfa

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
