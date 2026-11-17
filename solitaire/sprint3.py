"""Game sessions and validated JSON recording/replay, independent of Qt."""
import json
import random
from pathlib import Path
from solitaire.game import SolitaireGame

class GameSession:
    def __init__(self, board_type="English", size=7, mode="Manual", rng=None):
        self.rng = rng if rng is not None else random.Random()
        self.start(board_type, size, mode)

    def start(self, board_type="English", size=7, mode="Manual"):
        if mode not in ("Manual", "Automated"):
            raise ValueError("Unsupported mode")
        game = SolitaireGame(board_type, size)
        self.game, self.mode = game, mode
        self.initial = sorted(map(list, game.pegs))
        self.history = []

    def _record(self, action, source, destination):
        self.history.append({"action": action, "source": list(source),
                             "destination": list(destination),
                             "after": sorted(map(list, self.game.pegs))})

    def move(self, source, destination):
        if self.mode != "Manual" or self.game.is_game_over():
            return False
        if not self.game.make_move(tuple(source), tuple(destination)):
            return False
        self._record("move", source, destination)
        return True

    def automated_step(self):
        if self.mode != "Automated":
            return False
        moves = self.game.legal_moves()
        if not moves:
            return False
        source, destination = self.rng.choice(moves)
        if not self.game.make_move(source, destination):
            raise RuntimeError("Legal move unexpectedly rejected")
        self._record("move", source, destination)
        return True

    def autoplay(self):
        steps = 0
        while self.automated_step():
            steps += 1
        return steps

    def randomize(self):
        """Choose one random legal jump, preserving reachable board states."""
        if self.mode != "Manual":
            return False
        moves = self.game.legal_moves()
        if not moves:
            return False
        source, destination = self.rng.choice(moves)
        if not self.game.make_move(source, destination):
            raise RuntimeError("Legal random move rejected")
        self._record("randomize", source, destination)
        return True

    def to_dict(self):
        return {"format": "cs449-solitaire-session", "version": 1,
                "board_type": self.game.board_type, "size": self.game.size,
                "mode": self.mode, "initial": self.initial, "events": self.history}

    def save(self, path):
        Path(path).write_text(json.dumps(self.to_dict(), indent=2) + "\n", encoding="utf-8")

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict) or data.get("format") != "cs449-solitaire-session" or data.get("version") != 1:
            raise ValueError("Unsupported recording format")
        try:
            session = cls(data["board_type"], data["size"], data["mode"])
            if data["initial"] != session.initial or not isinstance(data["events"], list):
                raise ValueError("Invalid initial board or events")
            for event in data["events"]:
                if not isinstance(event, dict) or event["action"] not in ("move", "randomize"):
                    raise ValueError("Unknown recording action")
                if event["action"] == "randomize" and session.mode != "Manual":
                    raise ValueError("Randomization requires manual mode")
                source, destination = tuple(event["source"]), tuple(event["destination"])
                if not session.game.make_move(source, destination):
                    raise ValueError("Recording contains illegal move")
                if sorted(map(list, session.game.pegs)) != event["after"]:
                    raise ValueError("Recording state mismatch")
                session.history.append(event)
        except (KeyError, TypeError, IndexError, AttributeError) as exc:
            raise ValueError("Malformed recording") from exc
        return session

    @classmethod
    def load(cls, path):
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON recording") from exc
        return cls.from_dict(data)

    def replay_states(self):
        return [set(map(tuple, self.initial))] + [
            set(map(tuple, event["after"])) for event in self.history]
