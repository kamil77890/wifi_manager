from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading

from app.ui.components.network_item import NetworkItem


class NetworkList(QScrollArea):
    network_selected = pyqtSignal(str, bool, int)
    _scan_completed = pyqtSignal(list)
    _scan_error = pyqtSignal(str)
    
    def __init__(self, network_manager):
        super().__init__()
        self.network_manager = network_manager
        self.networks = []
        self.network_widgets = []
        
        self._scan_completed.connect(self.display_networks)
        self._scan_error.connect(self.display_error)
        
        self.init_ui()
    
    def init_ui(self):
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setMinimumHeight(400)
        
        self.container = QWidget()
        self.container.setObjectName("network_list_container")
        self.main_layout = QVBoxLayout(self.container)
        self.main_layout.setSpacing(12)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Loading indicator
        self.loading_widget = self.create_loading_widget()
        self.main_layout.addWidget(self.loading_widget)
        
        # Networks container
        self.networks_container = QWidget()
        self.networks_container.setObjectName("networks_container")
        self.networks_layout = QVBoxLayout(self.networks_container)
        self.networks_layout.setSpacing(10)
        self.networks_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.networks_container)
        
        self.main_layout.addStretch()
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh Networks")
        refresh_btn.setObjectName("refresh_button")
        refresh_btn.clicked.connect(self.update_networks)
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.setMinimumHeight(45)
        self.main_layout.addWidget(refresh_btn)
        
        self.setWidget(self.container)
        self.show_loading()
    
    def create_loading_widget(self):
        widget = QWidget()
        widget.setObjectName("loading_widget")
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        
        loading_icon = QLabel("🔍")
        loading_icon.setObjectName("loading_icon")
        loading_icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(loading_icon)
        
        loading_text = QLabel("Scanning for networks...")
        loading_text.setObjectName("loading_text")
        loading_text.setAlignment(Qt.AlignCenter)
        layout.addWidget(loading_text)
        
        return widget
    
    def update_networks(self):
        self.show_loading()
        
        def scan_networks():
            try:
                networks = self.network_manager.scan_networks()
                self._scan_completed.emit(networks)
            except Exception as e:
                self._scan_error.emit(str(e))
        
        threading.Thread(target=scan_networks, daemon=True).start()
    
    def show_loading(self):
        self.clear_networks()
        self.loading_widget.setVisible(True)
        self.networks_container.setVisible(False)
    
    def display_networks(self, networks):
        self.loading_widget.setVisible(False)
        self.clear_networks()
        self.networks = networks
        
        if not networks:
            no_net = QLabel("📡 No networks available")
            no_net.setObjectName("no_networks_label")
            no_net.setAlignment(Qt.AlignCenter)
            self.networks_layout.addWidget(no_net)
        else:
            for net in networks:
                item = NetworkItem(
                    ssid=net["ssid"],
                    strength=net["strength"],
                    is_secured=net["secured"],
                    is_connected=net.get("connected", False)
                )
                item.clicked.connect(self.on_network_clicked)
                self.networks_layout.addWidget(item)
                self.network_widgets.append(item)
        
        self.networks_container.setVisible(True)
        self.networks_container.updateGeometry()
    
    def on_network_clicked(self, ssid, is_secured, strength):
        self.network_selected.emit(ssid, is_secured, strength)
    
    def display_error(self, error_msg):
        self.loading_widget.setVisible(False)
        self.clear_networks()
        
        error = QLabel(f"❌ Scan Error: {error_msg}")
        error.setObjectName("error_label")
        error.setAlignment(Qt.AlignCenter)
        self.networks_layout.addWidget(error)
        self.networks_container.setVisible(True)
    
    def clear_networks(self):
        while self.networks_layout.count():
            item = self.networks_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.network_widgets.clear()