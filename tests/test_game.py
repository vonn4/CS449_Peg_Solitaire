"""Sprint 2 unit tests matching Sprint 1 gameplay acceptance criteria."""
import unittest

from solitaire.game import SolitaireGame


class SolitaireGameTest(unittest.TestCase):
    def test_each_supported_board_has_center_vacancy(self):
        expected = {"English": {7: 33, 9: 45}, "Hexagon": {7: 37, 9: 61}, "Diamond": {7: 25, 9: 41}}
        for board_type, sizes in expected.items():
          for size, holes in sizes.items():
            with self.subTest(board_type=board_type, size=size):
                game = SolitaireGame(board_type, size)
                self.assertEqual(len(game.positions), holes)
                self.assertEqual(game.remaining_pegs(), holes - 1)
                center = (0, 0) if board_type == "Hexagon" else (size // 2, size // 2)
                self.assertIn(center, game.positions)
                self.assertNotIn(center, game.pegs)
                self.assertFalse(game.is_game_over())

    def test_invalid_configuration_does_not_mutate_game(self):
        game = SolitaireGame()
        snapshot = (game.board_type, game.size, game.positions, set(game.pegs))
        for config in (("English", 6), ("Diamond", 11), ("Hexagon", 8), ("Nope", 7)):
            with self.subTest(config=config), self.assertRaises(ValueError):
                game.new_game(*config)
            self.assertEqual((game.board_type, game.size, game.positions, game.pegs), snapshot)

    def test_legal_move_changes_exactly_three_holes(self):
        """AC 4.1: model-based valid English move from initial center vacancy."""
        game = SolitaireGame()
        source, destination = (3, 1), (3, 3)
        self.assertTrue(game.is_valid_move(source, destination))
        self.assertTrue(game.make_move(source, destination))
        self.assertNotIn(source, game.pegs)
        self.assertNotIn((3, 2), game.pegs)
        self.assertIn(destination, game.pegs)
        self.assertEqual(game.remaining_pegs(), 31)

    def test_invalid_moves_leave_board_unchanged(self):
        game = SolitaireGame()
        for source, destination in [
            ((3, 1), (3, 2)),  # adjacent, occupied
            ((3, 1), (3, 5)),  # too far
            ((3, 1), (1, 3)),  # diagonal in English geometry
            ((3, 3), (3, 1)),  # empty source
            ((0, 2), (-2, 2)), # off board
        ]:
            with self.subTest(source=source, destination=destination):
                before = set(game.pegs)
                self.assertFalse(game.make_move(source, destination))
                self.assertEqual(game.pegs, before)

    def test_jump_requires_occupied_middle_cell(self):
        game = SolitaireGame()
        game.pegs = {(3, 1)}
        before = set(game.pegs)
        self.assertFalse(game.make_move((3, 1), (3, 3)))
        self.assertEqual(game.pegs, before)

    def test_game_over_when_no_legal_move_remains(self):
        """AC 5.2: two separated pegs cannot jump."""
        game = SolitaireGame()
        game.pegs = {(0, 2), (6, 4)}
        self.assertEqual(game.legal_moves(), [])
        self.assertTrue(game.is_game_over())
        self.assertEqual(game.remaining_pegs(), 2)

    def test_game_not_over_while_moves_exist(self):
        game = SolitaireGame()
        self.assertTrue(game.legal_moves())
        self.assertFalse(game.is_game_over())

    def test_reset_restores_configuration(self):
        game = SolitaireGame()
        game.make_move((3, 1), (3, 3))
        game.new_game()
        self.assertEqual(game.remaining_pegs(), 32)
        self.assertNotIn((3, 3), game.pegs)
        self.assertIn((3, 1), game.pegs)

    def test_hexagon_direction_is_not_square_grid_direction(self):
        game = SolitaireGame("Hexagon", 7)
        self.assertTrue(game.make_move((-2, 0), (0, 0)))
        game.new_game()
        self.assertFalse(game.make_move((-2, -2), (0, 0)))

    def test_size_options_available_for_all_board_types(self):
        for board_type in SolitaireGame.board_types():
            self.assertEqual(SolitaireGame.sizes_for(board_type), (7, 9))

    def test_diamond_four_square_grid_directions(self):
        game = SolitaireGame("Diamond", 9)
        self.assertTrue(game.make_move((4, 2), (4, 4)))
        game.new_game()
        self.assertFalse(game.make_move((2, 2), (4, 4)))


if __name__ == "__main__":
    unittest.main()
