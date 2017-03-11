import unittest
import python_bot

class get_command_and_args_tests(unittest.TestCase):

    def test_simple_command(self):
        self.assertEqual(python_bot.get_command_and_args('exit'), ('exit', None))

    def test_trims_white_space(self):
        self.assertEqual(python_bot.get_command_and_args(' exit '), ('exit', None))

class robot_controller_tests(unittest.TestCase):

    def test_enters_exit_state_on_exit_cmd(self):
        initial_state = (python_bot.STATE_START)
        next_state = python_bot.robot_controller(initial_state, 'exit')
        self.assertEqual(python_bot.STATE_EXIT, next_state[0])


def main():
    unittest.main()

if __name__ == '__main__':
    main()
