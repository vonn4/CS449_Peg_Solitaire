import unittest
from solitaire.game import SolitaireGame


class AIGeneratedLegalMoveTest(unittest.TestCase):

    def test_english_legal_move_updates_board_and_peg_count(self):
        """AC 4.1: A valid jump changes exactly three positions."""

        game = SolitaireGame("English", 7)

        source = (3, 1)
        jumped = (3, 2)
        destination = (3, 3)

        self.assertIn(source, game.pegs)
        self.assertIn(jumped, game.pegs)
        self.assertNotIn(destination, game.pegs)

        initial_count = game.remaining_pegs()
        initial_board = set(game.pegs)

        self.assertTrue(game.is_valid_move(source, destination))
        self.assertTrue(game.make_move(source, destination))

        self.assertNotIn(source, game.pegs)
        self.assertNotIn(jumped, game.pegs)
        self.assertIn(destination, game.pegs)

        self.assertEqual(game.remaining_pegs(), initial_count - 1)

        expected_board = (initial_board - {source, jumped}) | {destination}
        self.assertEqual(game.pegs, expected_board)


if __name__ == "__main__":
    unittest.main()
