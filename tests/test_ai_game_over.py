import unittest

from solitaire.game import SolitaireGame


class AIGeneratedGameOverTest(unittest.TestCase):

    def test_game_over_with_multiple_pegs_remaining(self):
        """AC 5.2: End the game when no legal moves remain."""

        game = SolitaireGame("English", 7)

        self.assertTrue(game.legal_moves())
        self.assertFalse(game.is_game_over())

        while game.legal_moves():
            source, destination = game.legal_moves()[0]
            self.assertTrue(game.make_move(source, destination))

        self.assertEqual(game.legal_moves(), [])
        self.assertTrue(game.is_game_over())
        self.assertEqual(game.remaining_pegs(), 7)
        self.assertGreater(game.remaining_pegs(), 1)


if __name__ == "__main__":
    unittest.main()
