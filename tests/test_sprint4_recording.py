"""Sprint 4 end-to-end recording and replay checks."""
import random
import tempfile
import unittest
from pathlib import Path

from solitaire.sprint3 import GameSession


class Sprint4RecordingRoundTripTests(unittest.TestCase):
    @staticmethod
    def replay_states_match_recording(original, restored):
        expected = [set(map(tuple, original.initial))]
        expected.extend(
            set(map(tuple, event["after"])) for event in original.history
        )
        return restored.replay_states() == expected

    def test_manual_game_without_randomization_round_trips_from_file(self):
        session = GameSession(rng=random.Random(10))
        chooser = random.Random(11)

        while not session.game.is_game_over():
            moves = session.game.legal_moves()
            if not moves:
                break
            source, destination = chooser.choice(moves)
            self.assertTrue(session.move(source, destination))

        self.assertGreater(len(session.history), 0)
        self.assertTrue(all(event["action"] == "move" for event in session.history))

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manual_no_randomization.json"
            session.save(path)
            restored = GameSession.load(path)

        self.assertEqual(restored.initial, session.initial)
        self.assertEqual(restored.history, session.history)
        self.assertTrue(self.replay_states_match_recording(session, restored))
        self.assertEqual(restored.game.pegs, session.game.pegs)
        self.assertTrue(restored.game.is_game_over())

    def test_manual_game_with_randomization_round_trips_exact_action_sequence(self):
        session = GameSession(rng=random.Random(12))
        chooser = random.Random(13)

        while not session.game.is_game_over():
            moves = session.game.legal_moves()
            if not moves:
                break

            # Include periodic randomization while preserving legal play.
            if len(session.history) % 5 == 2:
                succeeded = session.randomize()
                if not succeeded:
                    source, destination = chooser.choice(moves)
                    succeeded = session.move(source, destination)
            else:
                source, destination = chooser.choice(moves)
                succeeded = session.move(source, destination)

            self.assertTrue(succeeded)

        actions = [event["action"] for event in session.history]
        self.assertIn("randomize", actions)

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manual_with_randomization.json"
            session.save(path)
            restored = GameSession.load(path)

        self.assertEqual(restored.initial, session.initial)
        self.assertEqual(restored.history, session.history)
        self.assertTrue(self.replay_states_match_recording(session, restored))
        self.assertEqual(restored.game.pegs, session.game.pegs)
        self.assertTrue(restored.game.is_game_over())

    def test_automated_game_round_trips_from_file_and_replays_saved_states(self):
        session = GameSession(mode="Automated", rng=random.Random(14))
        self.assertGreater(session.autoplay(), 0)
        self.assertTrue(session.game.is_game_over())

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "automated.json"
            session.save(path)
            restored = GameSession.load(path)

        self.assertEqual(restored.initial, session.initial)
        self.assertEqual(restored.history, session.history)
        self.assertTrue(self.replay_states_match_recording(session, restored))
        self.assertEqual(restored.game.pegs, session.game.pegs)
        self.assertTrue(restored.game.is_game_over())


if __name__ == "__main__":
    unittest.main()
