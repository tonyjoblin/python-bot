import sys

STATE_START = 0
STATE_PLACED = 1
STATE_EXIT = 2

class Robot:        
    def __init__(self, state = None, x = None, y = None, facing = None):
        self.state = state
        if self.state is None:
            self.state = STATE_START
        self.x = x
        self.y = y
        self.facing = facing

def copy_robot(robot):
    new_robot = Robot(robot.state, robot.x, robot.y, robot.facing)
    return new_robot

def is_valid_state(robot):
    if robot.state == STATE_PLACED:
        if robot.x < 0:
            return False
        if robot.y < 0:
            return False
        if robot.x > 4:
            return False
        if robot.y > 4:
            return False
    return True

def handle_place(initial_state, args, outputs):
    next_state = copy_robot(initial_state)
    try:
        arg_list = args.split(',')
        x = int(arg_list[0])
        y = int(arg_list[1])
        facing = arg_list[2].strip()
        next_state.state = STATE_PLACED
        next_state.x = x
        next_state.y = y
        next_state.facing = facing
        if not is_valid_state(next_state):
            return initial_state
    except:
        pass
    return next_state

def handle_move(initial_state, args, outputs):
    if initial_state.state != STATE_PLACED:
        return initial_state

    next_state = copy_robot(initial_state)
    if next_state.facing == 'north':
        next_state.y += 1
    if next_state.facing == 'south':
        next_state.y -= 1
    if next_state.facing == 'east':
        next_state.x += 1
    if next_state.facing == 'west':
        next_state.x -= 1
    
    if not is_valid_state(next_state):
        return initial_state
    return next_state

def handle_left(initial_state, args, outputs):
    if initial_state.state != STATE_PLACED:
        return initial_state

    next_state = copy_robot(initial_state)
    if next_state.facing == 'north':
        next_state.facing = 'west'
    elif next_state.facing == 'west':
        next_state.facing = 'south'
    elif next_state.facing == 'south':
        next_state.facing = 'east'
    elif next_state.facing == 'east':
        next_state.facing = 'north'
    
    if not is_valid_state(next_state):
        return initial_state
    return next_state

def handle_right(initial_state, args, outputs):
    if initial_state.state != STATE_PLACED:
        return initial_state

    next_state = copy_robot(initial_state)
    if next_state.facing == 'north':
        next_state.facing = 'east'
    elif next_state.facing == 'east':
        next_state.facing = 'south'
    elif next_state.facing == 'south':
        next_state.facing = 'west'
    elif next_state.facing == 'west':
        next_state.facing = 'north'
    
    if not is_valid_state(next_state):
        return initial_state
    return next_state

def get_command_and_args(input):
    input = input.strip()
    pos = input.find(' ')
    if pos == -1:
        return input, None
    command = input[:pos]
    args = input[pos + 1:]
    return command, args

def robot_controller(initial_state, input, outputs = None):
    command, args = get_command_and_args(input)
    next_state = initial_state
    if initial_state.state == STATE_START:
        if command == 'exit':
            next_state = Robot(STATE_EXIT)
        elif command == 'place':
            next_state = handle_place(initial_state, args, outputs)
    elif initial_state.state == STATE_PLACED:
        if command == 'exit':
            next_state = Robot(STATE_EXIT)
        elif command == 'place':
            next_state = handle_place(initial_state, args, outputs)
        elif command == 'move':
            next_state = handle_move(initial_state, args, outputs)
        elif command == 'left':
            next_state = handle_left(initial_state, args, outputs)
        elif command == 'right':
            next_state = handle_right(initial_state, args, outputs)
    return next_state

def robot_command_loop(inputs, outputs):
    state = Robot()
    for command in inputs:
        next_state = robot_controller(state, command, outputs)
        if next_state.state == STATE_EXIT: # exit state
            break
        state = next_state

def main():
    robot_command_loop(sys.stdin, sys.stdout)

if __name__ == '__main__':
    main()
