import unittest
import python_bot
from python_bot import *
import io

class get_command_and_args_tests(unittest.TestCase):

    def test_simple_command(self):
        self.assertEqual(python_bot.get_command_and_args('exit'), ('exit', None))

    def test_trims_white_space(self):
        self.assertEqual(python_bot.get_command_and_args(' exit '), ('exit', None))

    def test_returns_args(self):
        self.assertEqual(
            python_bot.get_command_and_args('place 1,2,north'),
            ('place','1,2,north')
            )

class robot_controller_tests(unittest.TestCase):

    def test_enters_exit_state_on_exit_cmd(self):
        initial_state = Robot()
        
        next_state = robot_controller(initial_state, 'exit')
        
        self.assertEqual(STATE_EXIT, next_state.state)

    def test_valid_place_puts_robot_on_table(self):
        initial_state = Robot()
        
        next_state = robot_controller(initial_state, 'place 1,2,north')
        
        self.assertEqual(STATE_PLACED, next_state.state)
        self.assertEqual(1, next_state.x)
        self.assertEqual(2, next_state.y)
        self.assertEqual('north', next_state.facing)

    def test_cannot_place_robot_off_table(self):
        initial_state = Robot()
        
        next_state = robot_controller(initial_state, 'place -1,2,north')
        
        self.assertEqual(STATE_START, next_state.state)
        

    def test_cannot_take_robot_off_table(self):
        initial_state = Robot(STATE_PLACED, 1, 2, 'north')
        
        next_state = robot_controller(initial_state, 'place -1,2,north')
        
        self.assertEqual(STATE_PLACED, next_state.state)
        self.assertEqual(1, next_state.x)
        self.assertEqual(2, next_state.y)
        self.assertEqual('north', next_state.facing)

    def test_place_args_may_contain_ws(self):
        initial_state = Robot()
        
        next_state = robot_controller(initial_state, 'place 1 , 2,  north')
        
        self.assertEqual(STATE_PLACED, next_state.state)
        self.assertEqual(1, next_state.x)
        self.assertEqual(2, next_state.y)
        self.assertEqual('north', next_state.facing)

    def test_move_north(self):
        initial_state = Robot(STATE_PLACED, 1, 2, 'north')
        
        next_state = robot_controller(initial_state, 'move')
        
        self.assertEqual(STATE_PLACED, next_state.state)
        self.assertEqual(1, next_state.x)
        self.assertEqual(3, next_state.y)
        self.assertEqual('north', next_state.facing)

    def test_move_south(self):
        initial_state = Robot(STATE_PLACED, 1, 2, 'south')
        
        next_state = robot_controller(initial_state, 'move')
        
        self.assertEqual(STATE_PLACED, next_state.state)
        self.assertEqual(1, next_state.x)
        self.assertEqual(1, next_state.y)
        self.assertEqual('south', next_state.facing)
    
    def test_move_east(self):
        initial_state = Robot(STATE_PLACED, 1, 2, 'east')
        
        next_state = robot_controller(initial_state, 'move')
        
        self.assertEqual(STATE_PLACED, next_state.state)
        self.assertEqual(2, next_state.x)
        self.assertEqual(2, next_state.y)
        self.assertEqual('east', next_state.facing)

    def test_move_west(self):
        initial_state = Robot(STATE_PLACED, 1, 2, 'west')
        
        next_state = robot_controller(initial_state, 'move')
        
        self.assertEqual(STATE_PLACED, next_state.state)
        self.assertEqual(0, next_state.x)
        self.assertEqual(2, next_state.y)
        self.assertEqual('west', next_state.facing)

    def test_cannot_move_north_off_table(self):
        initial_state = Robot(STATE_PLACED, 1, 4, 'north')
        
        next_state = robot_controller(initial_state, 'move')
        
        self.assertEqual(STATE_PLACED, next_state.state)
        self.assertEqual(1, next_state.x)
        self.assertEqual(4, next_state.y)
        self.assertEqual('north', next_state.facing)

    def test_cannot_move_south_off_table(self):
        initial_state = Robot(STATE_PLACED, 1, 0, 'south')
        
        next_state = robot_controller(initial_state, 'move')
        
        self.assertEqual(STATE_PLACED, next_state.state)
        self.assertEqual(1, next_state.x)
        self.assertEqual(0, next_state.y)
        self.assertEqual('south', next_state.facing)
    
    def test_cannot_move_east_off_table(self):
        initial_state = Robot(STATE_PLACED, 4, 2, 'east')
        
        next_state = robot_controller(initial_state, 'move')
        
        self.assertEqual(STATE_PLACED, next_state.state)
        self.assertEqual(4, next_state.x)
        self.assertEqual(2, next_state.y)
        self.assertEqual('east', next_state.facing)

    def test_cannot_move_west_off_table(self):
        initial_state = Robot(STATE_PLACED, 0, 2, 'west')
        
        next_state = robot_controller(initial_state, 'move')
        
        self.assertEqual(STATE_PLACED, next_state.state)
        self.assertEqual(0, next_state.x)
        self.assertEqual(2, next_state.y)
        self.assertEqual('west', next_state.facing)

    def test_cannot_move_while_off_table(self):
        initial_state = Robot(STATE_START)
        
        next_state = robot_controller(initial_state, 'move')
        
        self.assertEqual(STATE_START, next_state.state)

    def test_facing_north_turn_left(self):
        initial_state = Robot(STATE_PLACED, 2, 2, 'north')
        
        next_state = robot_controller(initial_state, 'left')
        
        self.assertEqual(STATE_PLACED, next_state.state)
        self.assertEqual(2, next_state.x)
        self.assertEqual(2, next_state.y)
        self.assertEqual('west', next_state.facing)

    def test_facing_north_turn_right(self):
        initial_state = Robot(STATE_PLACED, 2, 2, 'north')
        
        next_state = robot_controller(initial_state, 'right')
        
        self.assertEqual(STATE_PLACED, next_state.state)
        self.assertEqual(2, next_state.x)
        self.assertEqual(2, next_state.y)
        self.assertEqual('east', next_state.facing)

    def test_facing_west_turn_left(self):
        initial_state = Robot(STATE_PLACED, 2, 2, 'west')
        
        next_state = robot_controller(initial_state, 'left')
        
        self.assertEqual(STATE_PLACED, next_state.state)
        self.assertEqual(2, next_state.x)
        self.assertEqual(2, next_state.y)
        self.assertEqual('south', next_state.facing)

    def test_facing_west_turn_right(self):
        initial_state = Robot(STATE_PLACED, 2, 2, 'west')
        
        next_state = robot_controller(initial_state, 'right')
        
        self.assertEqual(STATE_PLACED, next_state.state)
        self.assertEqual(2, next_state.x)
        self.assertEqual(2, next_state.y)
        self.assertEqual('north', next_state.facing)

    def test_facing_east_turn_left(self):
        initial_state = Robot(STATE_PLACED, 2, 2, 'east')
        
        next_state = robot_controller(initial_state, 'left')
        
        self.assertEqual(STATE_PLACED, next_state.state)
        self.assertEqual(2, next_state.x)
        self.assertEqual(2, next_state.y)
        self.assertEqual('north', next_state.facing)

    def test_facing_east_turn_right(self):
        initial_state = Robot(STATE_PLACED, 2, 2, 'east')
        
        next_state = robot_controller(initial_state, 'right')
        
        self.assertEqual(STATE_PLACED, next_state.state)
        self.assertEqual(2, next_state.x)
        self.assertEqual(2, next_state.y)
        self.assertEqual('south', next_state.facing)

    def test_facing_south_turn_left(self):
        initial_state = Robot(STATE_PLACED, 2, 2, 'south')
        
        next_state = robot_controller(initial_state, 'left')
        
        self.assertEqual(STATE_PLACED, next_state.state)
        self.assertEqual(2, next_state.x)
        self.assertEqual(2, next_state.y)
        self.assertEqual('east', next_state.facing)

    def test_facing_south_turn_right(self):
        initial_state = Robot(STATE_PLACED, 2, 2, 'south')
        
        next_state = robot_controller(initial_state, 'right')
        
        self.assertEqual(STATE_PLACED, next_state.state)
        self.assertEqual(2, next_state.x)
        self.assertEqual(2, next_state.y)
        self.assertEqual('west', next_state.facing)

    def test_ignore_left_when_off_table(self):
        initial_state = Robot(STATE_START)
        
        next_state = robot_controller(initial_state, 'left')
        
        self.assertEqual(STATE_START, next_state.state)
        self.assertEqual(None, next_state.x)
        self.assertEqual(None, next_state.y)
        self.assertEqual(None, next_state.facing)

    def test_ignore_right_when_off_table(self):
        initial_state = Robot(STATE_START)
        
        next_state = robot_controller(initial_state, 'right')
        
        self.assertEqual(STATE_START, next_state.state)
        self.assertEqual(None, next_state.x)
        self.assertEqual(None, next_state.y)
        self.assertEqual(None, next_state.facing)

    def test_report_when_off_table(self):
        initial_state = Robot(STATE_START)
        output = io.StringIO()
        
        robot_controller(initial_state, 'report', output)

        self.assertEqual('in toy box', output.getvalue())

    def test_report_when_on_table(self):
        initial_state = Robot(STATE_PLACED, 2, 2, 'east')
        output = io.StringIO()
        
        robot_controller(initial_state, 'report', output)

        self.assertEqual('2, 2, east', output.getvalue())

class robot_command_loop_tests(unittest.TestCase):

    def test_place_on_table_and_report(self):
        inputs = io.StringIO('place 2,2,north\nreport')
        outputs = io.StringIO()
        
        next_state = robot_command_loop(inputs, outputs)
        
        self.assertEqual('2, 2, north', outputs.getvalue())

    def test_example_a(self):
        inputs = io.StringIO('place 0,0,north\nmove\nreport')
        outputs = io.StringIO()
        
        next_state = robot_command_loop(inputs, outputs)
        
        self.assertEqual('0, 1, north', outputs.getvalue())

    def test_example_b(self):
        inputs = io.StringIO('place 0,0,north\nleft\nreport')
        outputs = io.StringIO()
        
        next_state = robot_command_loop(inputs, outputs)
        
        self.assertEqual('0, 0, west', outputs.getvalue())

    def test_example_c(self):
        inputs = io.StringIO('place 1,2,east\nmove\nmove\nleft\nmove\nreport')
        outputs = io.StringIO()
        
        next_state = robot_command_loop(inputs, outputs)
        
        self.assertEqual('3, 3, north', outputs.getvalue())

def main():
    unittest.main()

if __name__ == '__main__':
    main()
