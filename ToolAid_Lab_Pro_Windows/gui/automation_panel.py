"""Automation panel for experiment loops."""

from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from core.experiment_runner import run_experiment
from core.serial_manager import MockFlipperDevice


class AutomationPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.device = MockFlipperDevice()
        self.status = QLabel("Ready")
        self.run_btn = QPushButton("Run 3 loops")
        self.run_btn.clicked.connect(self.run_automation)

        layout = QVBoxLayout(self)
        layout.addWidget(self.status)
        layout.addWidget(self.run_btn)

    def run_automation(self):
        results = run_experiment(self.device, ["sigA", "sigB"], loops=3)
        self.status.setText(f"Completed loops: {len(results)}")
