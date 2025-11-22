import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QSystemTrayIcon, QMenu, QAction,
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


from wifi_manager.app.ui.main_wifi import main

class TrayApp:
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.tray = QSystemTrayIcon(QIcon(".assets/icon.png"))
        self.tray.setToolTip("Wi-Fi Control")
        self.tray.setVisible(True)

        menu = QMenu()

        open_wifi = QAction("Open Wi-Fi Settings")
        open_wifi.triggered.connect(self.open_wifi_window)
        menu.addAction(open_wifi)

        quit_action = QAction("Quit")
        quit_action.triggered.connect(self.app.quit)
        menu.addAction(quit_action)

        self.tray.setContextMenu(menu)

        self.tray.activated.connect(self.on_tray_click)

        self.wifi_window = main()

    def on_tray_click(self, reason):
        if reason == QSystemTrayIcon.Trigger:  
            self.open_wifi_window()

    def open_wifi_window(self):
        self.wifi_window.show()
        self.wifi_window.raise_()
        self.wifi_window.activateWindow()

    def run(self):
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    TrayApp.run()