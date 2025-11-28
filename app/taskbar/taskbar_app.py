import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QSystemTrayIcon, QMenu, QAction, QWidget
)
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtCore import QTimer, QSize

# Dodaj ścieżkę do projektu jeśli potrzebne
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ui.main_wifi import ModernWifiWindow
from app.logic.network_manager import NetworkManager
from app.config import ConfigManager
from app.ui.styles.styles import UnifiedStyles


class TrayApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.config = ConfigManager()
        self.network_manager = NetworkManager(self.config)
        
        self.app.setStyleSheet(UnifiedStyles.get_stylesheet())
        self.app.setApplicationName("Wi-Fi Manager")
        self.app.setApplicationVersion("1.0.0")
        self.app.setQuitOnLastWindowClosed(False)

        # Tworzymy główne okno
        self.main_window = ModernWifiWindow(self.network_manager, self.config)
        
        # Setup system tray
        self.tray = QSystemTrayIcon()
        # Tworzymy prostą ikonę programowo
        self.tray.setIcon(self.create_tray_icon())
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

        # Trigger initial scan
        if self.config.get('auto_scan', True):
            QTimer.singleShot(1000, self.main_window.trigger_initial_scan)

    def create_tray_icon(self):
        """Tworzy prostą ikonę WiFi dla system tray"""
        size = 64
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Rysujemy ikonę WiFi
        center = size // 2
        painter.setPen(QPen(QColor("#10b981"), 3))
        painter.setBrush(Qt.NoBrush)
        
        # Rysujemy kręgi (sygnał WiFi)
        radii = [20, 15, 10, 5]
        for radius in radii:
            painter.drawEllipse(center - radius, center - radius, radius * 2, radius * 2)
        
        # Rysujemy centralną kropkę
        painter.setBrush(QBrush(QColor("#10b981")))
        painter.drawEllipse(center - 2, center - 2, 4, 4)
        
        painter.end()
        return QIcon(pixmap)

    def on_tray_click(self, reason):
        if reason == QSystemTrayIcon.Trigger:  
            self.open_wifi_window()

    def open_wifi_window(self):
        if self.main_window.isVisible():
            self.main_window.hide()
        else:
            self.main_window.show()
            self.main_window.raise_()
            self.main_window.activateWindow()

    def run(self):
        return self.app.exec_()


if __name__ == "__main__":
    app = TrayApp()
    sys.exit(app.run())