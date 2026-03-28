"""Response verification panel widget."""

from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from core.response_verifier import verify_response


class ResponseTestPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Press to run verification")
        self.button = QPushButton("Run Test")
        self.button.clicked.connect(self.run_test)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.button)

    def run_test(self):
        ok = verify_response("verified", "verified")
        self.label.setText("Verification passed" if ok else "Verification failed")
