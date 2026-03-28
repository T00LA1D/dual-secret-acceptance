"""Simple dashboard panel summarizing lab modules."""

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class DashboardPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("ToolAid Dashboard"))
        layout.addWidget(QLabel("• Capture"))
        layout.addWidget(QLabel("• Transmit"))
        layout.addWidget(QLabel("• Automation"))
        layout.addWidget(QLabel("• Logging"))
