"""Unit tests for the game's rating policy."""

import unittest

from solitaire.rating import RatingPolicy


class RatingPolicyTest(unittest.TestCase):
    """Verify rating boundaries and invalid-input handling."""

    def setUp(self):
        self.policy = RatingPolicy()

    def test_one_peg_is_outstanding(self):
        self.assertEqual(self.policy.rate(1), "Outstanding")

    def test_two_pegs_is_very_good(self):
        self.assertEqual(self.policy.rate(2), "Very Good")

    def test_three_pegs_is_good(self):
        self.assertEqual(self.policy.rate(3), "Good")

    def test_four_or_more_pegs_is_average(self):
        for count in (4, 5, 32, 100):
            with self.subTest(remaining_pegs=count):
                self.assertEqual(self.policy.rate(count), "Average")

    def test_nonpositive_counts_are_rejected(self):
        for count in (0, -1):
            with self.subTest(remaining_pegs=count):
                with self.assertRaises(ValueError):
                    self.policy.rate(count)

    def test_noninteger_counts_are_rejected(self):
        for value in (1.0, "1", None, True, False):
            with self.subTest(remaining_pegs=value):
                with self.assertRaises(TypeError):
                    self.policy.rate(value)


if __name__ == "__main__":
    unittest.main()