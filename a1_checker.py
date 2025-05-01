"""A simple checker for functions in game_functions.py."""

from typing import Any, Dict
import unittest
import checker_generic
import game_functions as gf

FILENAME = 'game_functions.py'
PYTA_CONFIG = 'pyta/a1_pyta.txt'
TARGET_LEN = 79
SEP = '='

CONSTANTS = {
    'POINTS_PER_GUESS': 1, 'COST_OF_VOWEL': 1, 'BONUS_POINTS': 2,
    'PLAYER_ONE': 'Player One', 'PLAYER_TWO': 'Player Two',
    'GUESS': 'G', 'BUY': 'B', 'SOLVE': 'S', 'QUIT': 'Q',
    'SINGLE_PLAYER': 'SP', 'PVP': 'PVP', 'PVE': 'PVE',
    'EASY': 'E', 'HARD': 'H', 'ALL_CONSONANTS': 'bcdfghjklmnpqrstvwxyz',
    'ALL_VOWELS': 'aeiou', 'PRIORITY_CONSONANTS': 'tnrslhdcmpfygbwvkqxjz',
    'MYSTERY_CHAR': '^'
}


class CheckTest(unittest.TestCase):
    """Sanity checker for assignment functions."""

    def test_winning(self) -> None:
        """Function winning."""

        self._check(gf.winning, ['banana', 'banana'], bool)

    def test_game_over(self) -> None:
        """Function game_over."""

        self._check(gf.game_over, ['abc', 'abc', 'G'], bool)

    def test_is_player(self) -> None:
        """Function is_player."""

        self._check(gf.is_player, ['Player One', 'PVP'], bool)

    def test_one_player(self) -> None:
        """Function one_player."""

        self._check(gf.one_player, ['PVE'], bool)

    def test_current_player_score(self) -> None:
        """Function current_player_score."""

        self._check(gf.current_player_score, [1, 2, 'Player One'], int)

    def test_adds_points(self) -> None:
        """Function adds_points."""

        self._check(gf.adds_points, ['a', 'apple', '^^^le'], bool)

    def test_update_view(self) -> None:
        """"Function update_view."""

        self._check(gf.update_view, ['apple', '^^^le', 0, 'a'], str)

    def test_compute_score(self) -> None:
        """Function compute_score."""

        self._check(gf.compute_score, [4, 3, 'G'], int)

    def test_next_turn(self) -> None:
        """Function next_turn."""

        self._check(gf.next_turn, ['Player One', 0, 'PVP'], str)

    def test_is_mystery_char(self) -> None:
        """Function is_mystery_char."""

        self._check(gf.is_mystery_char, [1, 'apple', '^^^le'], bool)

    def test_environment_solves(self) -> None:
        """Function environment_solves."""

        self._check(gf.environment_solves, ['a^^le', 'H', 'pgh'], bool)

    def test_delete(self) -> None:
        """Function delete."""

        self._check(gf.delete, ['abc', 1], str)

    def test_check_constants(self) -> None:
        """Values of constants."""

        print('\nChecking that constants refer to their original values')
        self._check_constants(CONSTANTS, gf)
        print('  check complete')

    def _check(self, func: callable, args: list, ret_type: type) -> None:
        """Check that func called with arguments args returns a value of type
        ret_type. Display the progress and the result of the check.

        """

        print('\nChecking {}...'.format(func.__name__))
        result = checker_generic.check(func, args, ret_type)
        self.assertTrue(result[0], result[1])
        print('  check complete')

    def _check_constants(self, name2value: Dict[str, object], mod: Any) -> None:
        """Check that, for each (name, value) pair in name2value, the value of
        a variable named name in module mod is value.
        """

        for name, expected in name2value.items():
            actual = getattr(mod, name)
            msg = 'The value of constant {} should be {} but is {}.'.format(
                name, expected, actual)
            self.assertEqual(expected, actual, msg)


print(''.center(TARGET_LEN, SEP))
print(' Start: checking coding style '.center(TARGET_LEN, SEP))
checker_generic.run_pyta(FILENAME, PYTA_CONFIG)
print(' End checking coding style '.center(TARGET_LEN, SEP))

print(' Start: checking type contracts '.center(TARGET_LEN, SEP))
unittest.main(exit=False)
print(' End checking type contracts '.center(TARGET_LEN, SEP))

print('\nScroll up to see ALL RESULTS:')
print('  - checking coding style')
print('  - checking type contract\n')
