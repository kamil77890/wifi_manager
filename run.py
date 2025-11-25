import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

from app.ui.main_wifi import ModernWifiWindow
from app.logic.network_manager import NetworkManager
from app.config import ConfigManager
from app.ui.styles.styles import UnifiedStyles


class WifiManagerApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.config = ConfigManager()
        self.network_manager = NetworkManager(self.config)
        self.setup_app()

    def setup_app(self):
        self.app.setStyleSheet(UnifiedStyles.get_stylesheet())

        self.app.setApplicationName("Wi-Fi Manager")
        self.app.setApplicationVersion("1.0.0")
        self.app.setQuitOnLastWindowClosed(False)

        self.main_window = ModernWifiWindow(self.network_manager, self.config)

        if self.config.get('auto_scan', True):
            QTimer.singleShot(1000, self.main_window.trigger_initial_scan)

    def run(self):
        self.main_window.show()
        return self.app.exec_()


def main():
    app = WifiManagerApp()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
