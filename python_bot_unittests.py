import unittest
import python_bot

class get_command_and_args_tests(unittest.TestCase):

    def test_simple_command(self):
        self.assertEqual(python_bot.get_command_and_args('exit'), ('exit', None))

    def test_trims_white_space(self):
        self.assertEqual(python_bot.get_command_and_args(' exit '), ('exit', None))

class robot_controller_tests(unittest.TestCase):

    def test_returns_false_on_exit(self):
        result = python_bot.robot_controller('exit')
        self.assertEqual(result, False)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
