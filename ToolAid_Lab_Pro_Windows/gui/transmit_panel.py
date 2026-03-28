"""Transmit panel widget."""

from PySide6.QtWidgets import QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget

from core.serial_manager import MockFlipperDevice
from core.transmit_engine import transmit_signal


class TransmitPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.device = MockFlipperDevice()
        self.signals = QTextEdit("sigA\nsigB")
        self.status = QLabel("Ready")
        self.send_btn = QPushButton("Transmit")
        self.send_btn.clicked.connect(self.transmit)

        layout = QVBoxLayout(self)
        layout.addWidget(self.signals)
        layout.addWidget(self.send_btn)
        layout.addWidget(self.status)

    def transmit(self):
        signals = [x.strip() for x in self.signals.toPlainText().splitlines() if x.strip()]
        transmit_signal(self.device, signals)
        self.status.setText(f"Transmitted {len(signals)} signals")
