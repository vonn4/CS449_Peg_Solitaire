"""Sprint 3 PySide6 interface. Run: python -m solitaire.sprint3_gui"""
import sys
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QPushButton, QLabel, QComboBox, QFileDialog, QMessageBox)
from solitaire.game import SolitaireGame
from solitaire.sprint3 import GameSession

class SolitaireWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CS 449 Peg Solitaire — Sprint 3")
        self.resize(960, 760)
        self.session = GameSession()
        self.selected = None
        self.playback = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        outer = QVBoxLayout(self)
        outer.addWidget(QLabel("PEG SOLITAIRE  |  SPRINT 3"))
        controls = QHBoxLayout()
        self.board_type = QComboBox()
        self.board_type.addItems(SolitaireGame.board_types())
        self.size = QComboBox()
        self.mode = QComboBox()
        self.mode.addItems(["Manual", "Automated"])
        for title, widget in (("Board type", self.board_type), ("Board size", self.size), ("Mode", self.mode)):
            controls.addWidget(QLabel(title))
            controls.addWidget(widget)
        outer.addLayout(controls)
        self.board_type.currentTextChanged.connect(self.refresh_sizes)
        actions = QHBoxLayout()
        for title, fn in (("New Game", self.new_game), ("Autoplay", self.autoplay),
                          ("Randomize", self.randomize), ("Save Recording", self.save),
                          ("Load & Replay", self.load_replay), ("Stop", self.stop)):
            button = QPushButton(title)
            button.clicked.connect(fn)
            actions.addWidget(button)
        outer.addLayout(actions)
        self.status = QLabel()
        outer.addWidget(self.status)
        self.board = QGridLayout()
        self.board.setSpacing(3)
        outer.addLayout(self.board)
        outer.addStretch()
        self.setStyleSheet("""
            QWidget { font-family: 'Segoe UI'; font-size: 13px; background-color: #f8fafc; color: #0f172a; }
            QPushButton { padding: 8px; background-color: #e2e8f0; border: 1px solid #94a3b8; border-radius: 5px; }
            QPushButton:hover { background-color: #bfdbfe; }
            QComboBox { padding: 5px; }
        """)
        self.refresh_sizes()
        self.draw()

    def refresh_sizes(self, *_):
        previous = self.size.currentText()
        self.size.clear()
        self.size.addItems([str(n) for n in SolitaireGame.sizes_for(self.board_type.currentText())])
        if self.size.findText(previous) >= 0:
            self.size.setCurrentText(previous)

    def stop(self):
        self.timer.stop()
        self.playback = None

    def new_game(self):
        self.stop()
        self.session.start(self.board_type.currentText(), int(self.size.currentText()), self.mode.currentText())
        self.selected = None
        self.draw()

    def draw(self, pegs=None):
        while self.board.count():
            item = self.board.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        game = self.session.game
        visible_pegs = game.pegs if pegs is None else pegs
        min_row = min(row for row, _ in game.positions)
        min_col = min(col for _, col in game.positions)
        for position in sorted(game.positions):
            filled = position in visible_pegs
            button = QPushButton("●" if filled else "○")
            button.setFixedSize(46, 46)
            bg = "#bfdbfe" if position == self.selected else "#ffffff"
            fg = "#1d4ed8" if filled else "#94a3b8"
            button.setStyleSheet(
                f"QPushButton {{ background-color: {bg}; color: {fg}; font-size: 24px; border: 1px solid #94a3b8; }}"
            )
            button.clicked.connect(lambda checked=False, p=position: self.click_hole(p))
            self.board.addWidget(button, position[0] - min_row, position[1] - min_col)
        state = "Replaying" if self.playback is not None else (
            "Game over" if game.is_game_over() else "In progress")
        self.status.setText(
            f"{game.board_type} | {game.size} | {self.session.mode} | "
            f"Pegs: {len(visible_pegs)} | Recorded actions: {len(self.session.history)} | {state}"
        )

    def click_hole(self, position):
        if self.timer.isActive() or self.session.mode != "Manual":
            return
        if self.selected is None:
            if position in self.session.game.pegs:
                self.selected = position
        elif position == self.selected:
            self.selected = None
        elif self.session.move(self.selected, position):
            self.selected = None
        elif position in self.session.game.pegs:
            self.selected = position
        else:
            self.selected = None
        self.draw()

    def autoplay(self):
        if self.session.mode != "Automated":
            QMessageBox.information(self, "Mode", "Select Automated and click New Game first.")
            return
        self.stop()
        self.timer.start(85)

    def randomize(self):
        if self.timer.isActive():
            return
        if not self.session.randomize():
            QMessageBox.information(self, "Randomize", "Requires a manual game with a legal move.")
        self.selected = None
        self.draw()

    def save(self):
        if self.timer.isActive():
            QMessageBox.information(self, "Recording", "Stop playback or autoplay before saving.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Save recording", "solitaire_recording.json", "JSON files (*.json)")
        if path:
            try:
                self.session.save(path)
            except OSError as exc:
                QMessageBox.warning(self, "Save failed", str(exc))

    def load_replay(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load recording", "", "JSON files (*.json)")
        if not path:
            return
        try:
            loaded = GameSession.load(path)
        except (OSError, ValueError) as exc:
            QMessageBox.warning(self, "Invalid recording", str(exc))
            return
        self.stop()
        self.session = loaded
        self.selected = None
        self.board_type.setCurrentText(loaded.game.board_type)
        self.size.setCurrentText(str(loaded.game.size))
        self.mode.setCurrentText(loaded.mode)
        self.playback = iter(loaded.replay_states())
        self.timer.start(240)

    def tick(self):
        if self.playback is not None:
            try:
                self.draw(next(self.playback))
            except StopIteration:
                self.stop()
                self.draw()
        elif not self.session.automated_step():
            self.stop()
            self.draw()
        else:
            self.draw()

def main():
    app = QApplication(sys.argv)
    window = SolitaireWindow()
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
