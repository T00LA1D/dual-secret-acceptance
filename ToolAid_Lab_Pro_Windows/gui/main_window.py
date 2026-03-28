"""Main window for ToolAid Lab desktop app."""

from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget

from .automation_panel import AutomationPanel
from .dashboard_panel import DashboardPanel
from .response_test_panel import ResponseTestPanel
from .session_logger_panel import SessionLoggerPanel
from .signal_capture_panel import SignalCapturePanel
from .transmit_panel import TransmitPanel


class ToolAidMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ToolAid Launcher")
        tabs = QTabWidget()
        tabs.addTab(DashboardPanel(), "Dashboard")
        tabs.addTab(SignalCapturePanel(), "Capture")
        tabs.addTab(TransmitPanel(), "Transmit")
        tabs.addTab(AutomationPanel(), "Automation")
        tabs.addTab(ResponseTestPanel(), "Response")
        tabs.addTab(SessionLoggerPanel(), "Logs")
        self.setCentralWidget(tabs)


def run_gui():
    app = QApplication.instance() or QApplication([])
    window = ToolAidMainWindow()
    window.resize(700, 480)
    window.show()
    return app.exec()
