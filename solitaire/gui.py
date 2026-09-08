"""Provide an interactive rating preview for the Sprint 0 GUI exercise."""
from pathlib import Path

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QRadioButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from solitaire.rating import RatingPolicy


class RatingPreview(QWidget):
    """Display example results using the independent rating policy."""

    def __init__(self):
        super().__init__()
        self.policy = RatingPolicy()
        self.setWindowTitle("Peg Solitaire | Sprint 0")
        self.resize(640, 460)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(18)

        eyebrow = QLabel("CS 449  /  SPRINT 0")
        eyebrow.setObjectName("eyebrow")
        layout.addWidget(eyebrow)

        title = QLabel("Peg Solitaire")
        title.setObjectName("title")
        layout.addWidget(title)

        introduction = QLabel(
            "Explore the rating awarded when a game ends. "
            "This preview demonstrates the interface; gameplay comes later."
        )
        introduction.setWordWrap(True)
        layout.addWidget(introduction)

        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFixedHeight(2)
        divider.setStyleSheet("background-color: #CBD5E1;")
        layout.addWidget(divider)

        layout.addWidget(QLabel("Choose an example finishing count"))

        presets = QHBoxLayout()
        self.preset_group = QButtonGroup(self)
        self.preset_group.setExclusive(True)

        for count in (1, 2, 3, 4):
            label = "1 peg" if count == 1 else f"{count} pegs"
            button = QRadioButton(label)
            self.preset_group.addButton(button, count)
            presets.addWidget(button)

        layout.addLayout(presets)

        count_row = QHBoxLayout()
        count_label = QLabel("Pegs remaining:")
        self.peg_count = QSpinBox()
        self.peg_count.setRange(1, 32)
        self.peg_count.setValue(1)
        self.peg_count.setAccessibleName("Pegs remaining")
        count_label.setBuddy(self.peg_count)
        count_row.addWidget(count_label)
        count_row.addWidget(self.peg_count)
        count_row.addStretch()
        layout.addLayout(count_row)

        self.rating_label = QLabel()
        self.rating_label.setObjectName("rating")
        self.rating_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rating_label.setAccessibleName("Resulting rating")
        layout.addWidget(self.rating_label)

        self.show_explanation = QCheckBox("Show rating explanation")
        self.show_explanation.setChecked(True)
        layout.addWidget(self.show_explanation)

        self.explanation = QLabel()
        self.explanation.setWordWrap(True)
        layout.addWidget(self.explanation)
        layout.addStretch()

        self.preset_group.idClicked.connect(self.peg_count.setValue)
        self.peg_count.valueChanged.connect(self.update_rating)
        self.show_explanation.toggled.connect(self.explanation.setVisible)

        self.setStyleSheet("""
            QWidget {
                background-color: #F8FAFC;
                color: #172033;
                font-family: "Segoe UI";
                font-size: 14px;
            }
            QLabel#eyebrow {
                color: #475569;
                font-size: 12px;
                font-weight: bold;
            }
            QLabel#title {
                font-size: 32px;
                font-weight: bold;
            }
            QLabel#rating {
                background-color: #E0F2FE;
                color: #075985;
                border: 1px solid #7DD3FC;
                border-radius: 12px;
                padding: 18px;
                font-size: 26px;
                font-weight: bold;
            }
            QSpinBox {
                background-color: white;
                border: 1px solid #64748B;
                border-radius: 4px;
                padding: 6px;
                min-width: 72px;
            }
            QSpinBox:focus {
                border: 2px solid #0369A1;
            }
            QRadioButton, QCheckBox {
                spacing: 8px;
                padding: 4px;
            }
                        QRadioButton::indicator,
            QCheckBox::indicator {
                width: 22px;
                height: 22px;
                background-color: white;
                border: 2px solid #475569;
            }

            QRadioButton::indicator {
                border-radius: 12px;
            }

            QCheckBox::indicator {
                border-radius: 4px;
            }

            QRadioButton::indicator:checked,
            QCheckBox::indicator:checked {
                background-color: #0369A1;
                border-color: #0369A1;
            }

            QRadioButton:hover,
            QCheckBox:hover {
                background-color: #E2E8F0;
                border-radius: 4px;
            }

            QRadioButton:focus,
            QCheckBox:focus {
                outline: 2px solid #0369A1;
            }

            QSpinBox {
                min-height: 48px;
                min-width: 110px;
                padding-right: 40px;
                font-size: 18px;
            }

            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 36px;
                height: 28px;
                background-color: #E2E8F0;
                border-left: 1px solid #64748B;
                border-bottom: 1px solid #64748B;
            }

            QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 36px;
                height: 28px;
                background-color: #E2E8F0;
                border-left: 1px solid #64748B;
            }

            QSpinBox::up-button:hover,
            QSpinBox::down-button:hover {
                background-color: #BAE6FD;
            }

            QSpinBox::up-arrow,
            QSpinBox::down-arrow {
                width: 12px;
                height: 12px;
            }
        """)
        icon_directory = (
            Path(__file__).resolve().parent / "assets" / "icons"
        ).as_posix()

        self.show_explanation.setStyleSheet(
            """
            QCheckBox::indicator:checked {
                image: url("ICON_DIRECTORY/check.svg");
                background-color: #0369A1;
                border: 2px solid #0369A1;
                width: 22px;
                height: 22px;
            }
            """.replace("ICON_DIRECTORY", icon_directory)
        )

        self.peg_count.setStyleSheet(
            """
            QSpinBox::up-arrow {
                image: url("ICON_DIRECTORY/arrow-up.svg");
                width: 16px;
                height: 16px;
            }
            QSpinBox::down-arrow {
                image: url("ICON_DIRECTORY/arrow-down.svg");
                width: 16px;
                height: 16px;
            }
            """.replace("ICON_DIRECTORY", icon_directory)
        )
        
        self.update_rating(self.peg_count.value())

    def update_rating(self, remaining_pegs: int):
        """Refresh the displayed result and synchronize preset selection."""
        self.rating_label.setText(self.policy.rate(remaining_pegs))
        self.explanation.setText(
            f"With {remaining_pegs} peg(s) remaining, the rating is "
            f"{self.policy.rate(remaining_pegs)}. "
            "The thresholds are: 1 = Outstanding, 2 = Very Good, "
            "3 = Good, and 4 or more = Average."
        )

        # Counts outside the presets should leave no preset selected.
        self.preset_group.setExclusive(False)
        for button in self.preset_group.buttons():
            button.setChecked(
                self.preset_group.id(button) == remaining_pegs
            )
        self.preset_group.setExclusive(True)


def main():
    """Start the desktop preview."""
    app = QApplication(sys.argv)
    window = RatingPreview()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()