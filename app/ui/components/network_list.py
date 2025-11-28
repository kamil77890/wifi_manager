from PyQt5.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal

from app.ui.components.network_item import NetworkItem

class NetworkList(QScrollArea):
    network_clicked = pyqtSignal(str, bool) 

    def __init__(self, network_manager, parent=None): 
        super().__init__(parent)         
        self.network_manager = network_manager
        
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setStyleSheet("background: transparent; border: none;")
        
        self.container = QWidget()
        self.container.setObjectName("network_list_container")
        self.layout = QVBoxLayout(self.container)
        self.layout.setSpacing(4)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addStretch()  
        
        self.setWidget(self.container)

    def display_networks(self, networks):
        while self.layout.count() > 1:
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for net in networks:
            self.add_network_item(net)

    def add_network_item(self, net_data):
        ssid = net_data.get('ssid', 'Unknown')
        strength = net_data.get('strength', 0)
        secured = net_data.get('secured', False)
        connected = net_data.get('connected', False)

        item = NetworkItem(ssid, strength, secured, connected)
        
        item.network_selected.connect(self.network_clicked.emit)

        self.layout.insertWidget(self.layout.count() - 1, item)