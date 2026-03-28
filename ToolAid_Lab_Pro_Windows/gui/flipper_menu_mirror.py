"""Flipper menu mirror panel."""

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class FlipperMenuMirror(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Flipper Menu Mirror"))
        layout.addWidget(QLabel("Main > RF > Capture"))
