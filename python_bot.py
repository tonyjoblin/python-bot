import sys

def get_command_and_args(input):
    input = input.strip()
    pos = input.find(' ')
    if pos == -1:
        return (input, None)
    command = input[:pos]
    args = input[pos:]
    return (command, args)

def robot_controller(input):
    command, args = get_command_and_args(input)
    if command == 'exit':
        return False
    return True

def robot_command_loop(inputs, outputs):
    for command in inputs:
        if not robot_controller(command):
            break

def main():
    robot_command_loop(sys.stdin, sys.stdout)

if __name__ == '__main__':
    main()
