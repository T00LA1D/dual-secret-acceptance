"""Signal capture panel widget."""

from PySide6.QtWidgets import QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget

from core.serial_manager import MockFlipperDevice
from core.signal_processor import capture_signal


class SignalCapturePanel(QWidget):
    def __init__(self):
        super().__init__()
        self.device = MockFlipperDevice()
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.status = QLabel("Ready")
        self.capture_btn = QPushButton("Capture 1s")
        self.capture_btn.clicked.connect(self.capture_once)

        layout = QVBoxLayout(self)
        layout.addWidget(self.status)
        layout.addWidget(self.capture_btn)
        layout.addWidget(self.output)

    def capture_once(self):
        logs = capture_signal(self.device, duration=1)
        self.status.setText(f"Captured {len(logs)} samples")
        self.output.setPlainText("\n".join(logs))
