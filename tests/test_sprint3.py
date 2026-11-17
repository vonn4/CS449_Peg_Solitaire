"""Sprint 3 tests for manual, automated, randomization, and replay."""
import json
import random
import tempfile
import unittest
from pathlib import Path
from solitaire.sprint3 import GameSession

class ManualSessionTests(unittest.TestCase):
    def test_manual_move_is_recorded(self):
        s = GameSession()
        self.assertTrue(s.move((3, 1), (3, 3)))
        self.assertEqual(s.game.remaining_pegs(), 31)
        self.assertEqual(s.history[0]["action"], "move")

    def test_invalid_move_does_not_change_state_or_history(self):
        s = GameSession()
        before = set(s.game.pegs)
        self.assertFalse(s.move((3, 3), (3, 1)))
        self.assertEqual(s.game.pegs, before)
        self.assertEqual(s.history, [])

    def test_manual_randomize_preserves_legal_state(self):
        s = GameSession(rng=random.Random(2))
        self.assertTrue(s.randomize())
        self.assertEqual(s.game.remaining_pegs(), 31)
        self.assertEqual(s.history[0]["action"], "randomize")

    def test_manual_mode_blocks_automated_step(self):
        self.assertFalse(GameSession().automated_step())

    def test_manual_game_over(self):
        s = GameSession()
        s.game.pegs = {(0, 2), (6, 4)}
        self.assertTrue(s.game.is_game_over())
        self.assertFalse(s.randomize())

class AutomatedSessionTests(unittest.TestCase):
    def test_automated_mode_blocks_manual_move(self):
        s = GameSession(mode="Automated")
        self.assertFalse(s.move((3, 1), (3, 3)))
        self.assertFalse(s.randomize())

    def test_automated_game_terminates(self):
        s = GameSession(mode="Automated", rng=random.Random(4))
        count = s.autoplay()
        self.assertGreater(count, 0)
        self.assertTrue(s.game.is_game_over())
        self.assertEqual(len(s.history), count)

    def test_hexagon_automated_game_terminates(self):
        s = GameSession("Hexagon", 7, "Automated", random.Random(4))
        self.assertGreater(s.autoplay(), 0)
        self.assertTrue(s.game.is_game_over())

class RecordingTests(unittest.TestCase):
    def test_round_trip_manual_with_randomization(self):
        s = GameSession(rng=random.Random(2))
        self.assertTrue(s.move((3, 1), (3, 3)))
        self.assertTrue(s.randomize())
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "game.json"
            s.save(path)
            restored = GameSession.load(path)
        self.assertEqual(restored.game.pegs, s.game.pegs)
        self.assertEqual(restored.replay_states()[-1], s.game.pegs)
        self.assertEqual(len(restored.replay_states()), 3)

    def test_round_trip_automated(self):
        s = GameSession(mode="Automated", rng=random.Random(3))
        s.autoplay()
        self.assertEqual(GameSession.from_dict(s.to_dict()).game.pegs, s.game.pegs)

    def test_corrupt_recording_is_rejected(self):
        s = GameSession()
        s.move((3, 1), (3, 3))
        data = s.to_dict()
        data["events"][0]["after"] = []
        with self.assertRaises(ValueError):
            GameSession.from_dict(data)

    def test_invalid_json_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text("{not json", encoding="utf-8")
            with self.assertRaises(ValueError):
                GameSession.load(path)

    def test_invalid_mode_is_rejected(self):
        with self.assertRaises(ValueError):
            GameSession(mode="Unknown")

if __name__ == "__main__":
    unittest.main()
