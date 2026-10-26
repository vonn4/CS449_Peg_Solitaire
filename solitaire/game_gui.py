"""Minimal Sprint 2 PySide6 interface; all rules live in SolitaireGame."""

from __future__ import annotations

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QComboBox, QHBoxLayout, QLabel, QPushButton,
    QVBoxLayout, QWidget,
)

from solitaire.game import Position, SolitaireGame


class SolitaireWindow(QWidget):
    """Show the board and translate clicks into engine operations."""

    def __init__(self) -> None:
        super().__init__()
        self.game = SolitaireGame()
        self.selected: Position | None = None
        self.cells: dict[Position, QPushButton] = {}
        self.setWindowTitle("Peg Solitaire | CS449 Sprint 2")
        self.resize(680, 660)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(14)
        title = QLabel("Peg Solitaire")
        title.setStyleSheet("font-size: 25px; font-weight: bold;")
        layout.addWidget(title)

        controls = QHBoxLayout()
        controls.addWidget(QLabel("Board type:"))
        self.board_type = QComboBox()
        self.board_type.addItems(SolitaireGame.board_types())
        self.board_type.currentTextChanged.connect(self.update_available_sizes)
        controls.addWidget(self.board_type)
        controls.addWidget(QLabel("Board size:"))
        self.board_size = QComboBox()
        controls.addWidget(self.board_size)
        self.new_game_button = QPushButton("New Game")
        self.new_game_button.clicked.connect(self.start_new_game)
        controls.addWidget(self.new_game_button)
        layout.addLayout(controls)

        self.board_area = QWidget()
        self.board_area.setMinimumHeight(465)
        self.board_area.setStyleSheet("background: #f2f5fa; border-radius: 10px;")
        layout.addWidget(self.board_area, stretch=1)
        self.status = QLabel()
        self.status.setWordWrap(True)
        self.status.setAccessibleName("Game status")
        layout.addWidget(self.status)
        self.update_available_sizes(self.board_type.currentText())
        self.render_board()

    def update_available_sizes(self, board_type: str) -> None:
        """Show only board sizes supported by the chosen board configuration."""
        current = self.board_size.currentData()
        self.board_size.clear()
        for size in SolitaireGame.sizes_for(board_type):
            self.board_size.addItem(str(size), size)
        if current in SolitaireGame.sizes_for(board_type):
            self.board_size.setCurrentIndex(self.board_size.findData(current))

    def start_new_game(self) -> None:
        try:
            self.game.new_game(self.board_type.currentText(), self.board_size.currentData())
        except ValueError as error:
            self.status.setText(str(error))
            return
        self.selected = None
        self.render_board()

    def on_cell_clicked(self, position: Position) -> None:
        if self.game.is_game_over():
            self.update_status()
            return
        if self.selected is None:
            if position not in self.game.pegs:
                self.status.setText("Choose an occupied peg first.")
                return
            self.selected = position
            self.render_board()
            return
        if position == self.selected:
            self.selected = None
            self.render_board()
            return
        if position in self.game.pegs:
            self.selected = position
            self.render_board()
            return
        moved = self.game.make_move(self.selected, position)
        self.selected = None
        self.render_board()
        if not moved:
            self.status.setText("Invalid move. Jump over one adjacent peg into an empty hole.")

    def render_board(self) -> None:
        """Render the model's playable positions without duplicating move rules."""
        for cell in self.cells.values():
            cell.deleteLater()
        self.cells.clear()
        positions = self.game.positions
        # Translate axial hex coordinates into a triangular lattice on screen.
        if self.game.board_type == "Hexagon":
            coordinates = {p: (p[0] + p[1] / 2, p[1] * 0.86) for p in positions}
        else:
            coordinates = {p: (p[1], p[0]) for p in positions}
        min_x = min(x for x, y in coordinates.values())
        max_x = max(x for x, y in coordinates.values())
        min_y = min(y for x, y in coordinates.values())
        max_y = max(y for x, y in coordinates.values())
        unit = 47
        diameter = 38
        content_width = (max_x - min_x) * unit + diameter
        content_height = (max_y - min_y) * unit + diameter
        canvas_width = max(self.board_area.width(), 600)
        canvas_height = max(self.board_area.height(), 465)
        left = (canvas_width - content_width) / 2
        top = (canvas_height - content_height) / 2
        for position, (x, y) in coordinates.items():
            button = QPushButton(self.board_area)
            button.setFixedSize(diameter, diameter)
            button.move(round(left + (x - min_x) * unit), round(top + (y - min_y) * unit))
            button.setText("●" if position in self.game.pegs else "○")
            button.setAccessibleName(f"Hole {position}, {'occupied' if position in self.game.pegs else 'empty'}")
            if position == self.selected:
                background, color = "#FBBF24", "#111827"
            elif position in self.game.pegs:
                background, color = "#1D4ED8", "white"
            else:
                background, color = "white", "#64748B"
            button.setStyleSheet(
                f"QPushButton {{ background: {background}; color: {color}; "
                "font-size: 20px; font-weight: bold; border: 2px solid #64748B; "
                "border-radius: 19px; }} QPushButton:hover { border-color: #F59E0B; }"
            )
            button.clicked.connect(lambda checked=False, p=position: self.on_cell_clicked(p))
            self.cells[position] = button
            button.show()
        self.update_status()

    def update_status(self) -> None:
        count = self.game.remaining_pegs()
        if self.game.is_game_over():
            self.status.setText(f"Game over — no legal moves remain. Pegs left: {count}.")
        elif self.selected is not None:
            self.status.setText(f"Selected {self.selected}. Choose an empty destination. Pegs: {count}.")
        else:
            self.status.setText(f"Game active — {count} pegs remaining. Select a peg to move.")

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        if hasattr(self, "cells") and self.cells:
            self.render_board()


def main() -> None:
    app = QApplication(sys.argv)
    window = SolitaireWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
