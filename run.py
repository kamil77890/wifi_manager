import sys
import os
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import QTimer, Qt, QSize
from app.ui.main_wifi import ModernWifiWindow
from app.logic.network_manager import NetworkManager
from app.config import ConfigManager
from app.ui.styles.styles import UnifiedStyles

class WifiManagerApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.config = ConfigManager()
        self.network_manager = NetworkManager()
        self.current_icon_level = -1  
        self.setup_app()

    def setup_app(self):
        self.app.setStyleSheet(UnifiedStyles.get_stylesheet())
        self.app.setApplicationName("Wi-Fi Manager")
        self.app.setApplicationVersion("1.0.0")
        self.app.setQuitOnLastWindowClosed(False)
        self.main_window = ModernWifiWindow(self.network_manager, self.config)
        self.main_window.hide()
        
        self.main_window.networks_updated.connect(self.update_tray_icon_based_on_signal)
        
        self.setup_tray_icon()
        
        if self.config.get('auto_scan', True):
            QTimer.singleShot(1000, self.main_window.trigger_initial_scan)
        
        self.icon_update_timer = QTimer()
        self.icon_update_timer.timeout.connect(self.update_tray_icon_based_on_signal)
        self.icon_update_timer.start(5000)  # Update every 5 seconds

    def setup_tray_icon(self):
        icon = self.load_wifi_icon(3)  
        
        self.tray_icon = QSystemTrayIcon(icon, self.app)
        self.tray_icon.setToolTip("Wi-Fi Manager")
        
        tray_menu = QMenu()
        show_action = QAction("Show Wi-Fi Manager", self.app)
        show_action.triggered.connect(self.show_main_window)
        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        quit_action = QAction("Quit", self.app)
        quit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()

    def load_wifi_icon(self, signal_level):
        """
        Load WiFi icon based on signal level
        signal_level: 0 = no connection/off, 1 = weak (1 bar), 2 = medium (2 bars), 3 = strong (3 bars)
        """
        icon_paths = {
            0: "./app/assets/wifi_0.png",  # No connection or WiFi off
            1: "./app/assets/wifi_1.png",  # 1 bar
            2: "./app/assets/wifi_2.png",  # 2 bars
            3: "./app/assets/wifi.png",    # 3 bars (full)
        }
        
        icon_path = icon_paths.get(signal_level, "./app/assets/wifi.png")
        
        if os.path.exists(icon_path):
            print(f"Loading icon from: {icon_path}")
            pixmap = QPixmap(icon_path)
            scaled_pixmap = pixmap.scaledToWidth(48, Qt.SmoothTransformation)
            icon = QIcon(scaled_pixmap)
            icon.addPixmap(scaled_pixmap, QIcon.Normal)
            icon.addPixmap(scaled_pixmap, QIcon.Active)
            
            if not icon.isNull():
                return icon
        
        # Fallback to generated icon
        return self.create_wifi_icon()

    def create_wifi_icon(self):
        """Fallback: create a simple WiFi icon programmatically"""
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        pen = QPen(QColor(255, 255, 255), 4)
        painter.setPen(pen)
        
        # Draw WiFi arcs
        painter.drawArc(10, 20, 44, 44, 0, 180 * 16)
        painter.drawArc(18, 28, 28, 28, 0, 180 * 16)
        painter.drawArc(26, 36, 12, 12, 0, 180 * 16)
        
        # Draw center dot
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawEllipse(28, 46, 8, 8)
        
        painter.end()
        return QIcon(pixmap)

    def update_tray_icon_based_on_signal(self, networks=None):
        """Update tray icon based on current connection signal strength"""
        if not self.main_window.wifi_on:
            # WiFi is off
            if self.current_icon_level != 0:
                self.tray_icon.setIcon(self.load_wifi_icon(0))
                self.tray_icon.setToolTip("Wi-Fi Manager - WiFi Off")
                self.current_icon_level = 0
            return
        
        current_network = self.network_manager.current_network
        
        if not current_network:
            # Not connected
            if self.current_icon_level != 0:
                self.tray_icon.setIcon(self.load_wifi_icon(0))
                self.tray_icon.setToolTip("Wi-Fi Manager - Not Connected")
                self.current_icon_level = 0
            return
        
        # Find signal strength of current network
        signal_strength = 50  # Default medium strength
        
        if networks:
            for net in networks:
                if net['ssid'] == current_network:
                    signal_strength = net['strength']
                    break
        
        # Determine icon level based on signal strength
        if signal_strength >= 70:
            icon_level = 3  # Strong signal (3 bars)
        elif signal_strength >= 40:
            icon_level = 2  # Medium signal (2 bars)
        else:
            icon_level = 1  # Weak signal (1 bar)
        
        # Only update if icon level changed
        if icon_level != self.current_icon_level:
            self.tray_icon.setIcon(self.load_wifi_icon(icon_level))
            self.tray_icon.setToolTip(f"Wi-Fi Manager - {current_network} ({signal_strength}%)")
            self.current_icon_level = icon_level
            print(f"Updated tray icon to level {icon_level} for {current_network} ({signal_strength}%)")

    def on_tray_activated(self, reason):
        """Handle tray icon activation"""
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick, QSystemTrayIcon.MiddleClick):
            self.toggle_main_window()

    def toggle_main_window(self):
        if self.main_window.isVisible():
            self.main_window.hide()
        else:
            self.show_main_window()

    def show_main_window(self):
        self.main_window.show()
        self.main_window.raise_()
        self.main_window.activateWindow()
        self.main_window.setFocus()  # Upewnij się, że okno ma fokus po pokazaniu

    def quit_application(self):
        self.icon_update_timer.stop()
        self.tray_icon.hide()
        self.app.quit()

    def run(self):
        return self.app.exec_()

def main():
    app = WifiManagerApp()
    sys.exit(app.run())

if __name__ == "__main__":
    main()