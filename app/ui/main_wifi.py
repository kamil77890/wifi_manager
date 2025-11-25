from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from app.ui.components.settings_tab import SettingsTab
from app.ui.components.network_list import NetworkList
from app.ui.components.connection_form import ConnectionForm


class ModernWifiWindow(QWidget):
    def __init__(self, network_manager, config):
        super().__init__()
        self.network_manager = network_manager
        self.config = config
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Wi-Fi Manager")
        self.resize(600, 700)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        header = self.create_header()
        main_layout.addWidget(header)

        platform_label = QLabel(f"🌐 Platform: {self.get_platform_info()}")
        platform_label.setObjectName("mock_label")
        platform_label.setAlignment(Qt.AlignCenter)
        platform_label.setFixedHeight(35)
        main_layout.addWidget(platform_label)

        self.tabs = QTabWidget()
        self.setup_tabs()
        main_layout.addWidget(self.tabs)

        self.setLayout(main_layout)

        self.connection_form = ConnectionForm(self.config, self)
        self.connection_form.hide()

        QTimer.singleShot(1000, self.trigger_initial_scan)

    def get_platform_info(self):
        import platform
        system = platform.system()
        if system == "Windows":
            return "Windows"
        elif system == "Linux":
            return "Linux"
        elif system == "Darwin":
            return "macOS"
        else:
            return system

    def create_header(self):
        header = QWidget()
        header.setFixedHeight(100)
        header.setObjectName("main_header")

        layout = QVBoxLayout(header)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(8)

        title = QLabel("📶 Wi-Fi Manager")
        title.setObjectName("main_title")
        title.setStyleSheet("font-size: 28px;")

        subtitle = QLabel("Professional Wireless Network Management")
        subtitle.setObjectName("main_subtitle")
        subtitle.setStyleSheet("font-size: 12px;")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        return header

    def setup_tabs(self):
        self.networks_tab = QWidget()
        self.setup_networks_tab()
        self.tabs.addTab(self.networks_tab, "🌐 Networks")

        # self.settings_tab = SettingsTab(self.config, self.network_manager)
        # self.tabs.addTab(self.settings_tab, "⚙️ Settings")

    def setup_networks_tab(self):
        layout = QVBoxLayout(self.networks_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        self.network_list = NetworkList(self.network_manager)

        self.network_list.network_selected.connect(
            self.handle_network_selected)

        layout.addWidget(self.network_list)

    def handle_network_selected(self, ssid, is_secured, strength):
        """Obsługa wyboru sieci - pokazanie ConnectionForm jako overlay"""
        self.connection_form.on_network_selected(ssid, is_secured, strength)
        self.connection_form.connect_signal.connect(self.connect_network)

    def connect_network(self, ssid, password, save_password):
        def connect():
            success = self.network_manager.connect_to_network(ssid, password)
            if success and save_password:
                self.config.save_network(ssid, password)

            QTimer.singleShot(
                0, lambda: self.show_connection_status(ssid, success))
            QTimer.singleShot(2000, self.network_list.update_networks)

        import threading
        threading.Thread(target=connect, daemon=True).start()

    def show_connection_status(self, ssid, success):
        if success:
            QMessageBox.information(self, "Connection Successful",
                                    f"✅ Successfully connected to {ssid}!")
        else:
            QMessageBox.warning(self, "Connection Failed",
                                f"❌ Failed to connect to {ssid}\n\nPlease check your password and try again.")

    def trigger_initial_scan(self):
        if hasattr(self, 'network_list'):
            self.network_list.update_networks()

    def resizeEvent(self, event):
        """Przy zmianie rozmiaru okna, aktualizujemy pozycję ConnectionForm"""
        super().resizeEvent(event)
        if hasattr(self, 'connection_form'):
            if self.connection_form.isVisible():
                self.connection_form.position_at_bottom()
