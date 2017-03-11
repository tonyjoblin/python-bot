import sys

STATE_START = 0
STATE_PLACED = 1
STATE_EXIT = 2

def get_command_and_args(input):
    input = input.strip()
    pos = input.find(' ')
    if pos == -1:
        return (input, None)
    command = input[:pos]
    args = input[pos:]
    return (command, args)

def robot_controller(initial_state, input, outputs = None):
    command, args = get_command_and_args(input)
    if command == 'exit':
        return (STATE_EXIT,)
    return initial_state

def robot_command_loop(inputs, outputs):
    state = (STATE_START,)
    for command in inputs:
        next_state = robot_controller(state, command, outputs)
        if next_state[0] == STATE_EXIT: # exit state
            break
        state = next_state

def main():
    robot_command_loop(sys.stdin, sys.stdout)

if __name__ == '__main__':
    main()
