"""Session log viewer panel."""

from pathlib import Path

from PySide6.QtWidgets import QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget

from core.logger import log_message


class SessionLoggerPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.log_path = Path("logs/session.log")
        self.viewer = QTextEdit()
        self.viewer.setReadOnly(True)
        self.status = QLabel("No logs yet")
        self.append_btn = QPushButton("Append Sample Log")
        self.append_btn.clicked.connect(self.append_log)

        layout = QVBoxLayout(self)
        layout.addWidget(self.status)
        layout.addWidget(self.append_btn)
        layout.addWidget(self.viewer)

    def append_log(self):
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        log_message(self.log_path, "session event")
        self.viewer.setPlainText(self.log_path.read_text(encoding="utf-8"))
        self.status.setText("Log updated")
