from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ConnectionForm(QWidget):
    connect_signal = pyqtSignal(str, str, bool)     
    
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.current_network = None
        self.is_secured = True

        self.setObjectName("connection_form_page")
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        # Marginesy wewnątrz strony
        layout.setContentsMargins(24, 10, 24, 20)# Pycha treść do środka
        self.network_icon.setObjectName("connection_icon_large") # Wymaga stylu w CSS
        self.network_icon.setAlignment(Qt.AlignCenter)
        self.network_icon.setFixedSize(64, 64)
        
        icon_container = QHBoxLayout()
        icon_container.addStretch()
        icon_container.addWidget(self.network_icon)
        icon_container.addStretch()
        info_layout.addLayout(icon_container)

        self.network_ssid = QLabel("Unknown")
        self.network_ssid.setObjectName("connection_ssid_large") 
        self.network_ssid.setAlignment(Qt.AlignCenter)
        self.network_ssid.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        info_layout.addWidget(self.network_ssid)

        self.status_label = QLabel("Enter password to connect")
        self.status_label.setStyleSheet("color: #a1a1aa; font-size: 12px;")
        self.status_label.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(self.status_label)

        layout.addLayout(info_layout)

        self.form_container = QWidget()
        form_layout = QVBoxLayout(self.form_container)
        form_layout.setContentsMargins(0, 10, 0, 0)
        form_layout.setSpacing(8)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(36)
        self.password_input.returnPressed.connect(self.on_connect_clicked)
        form_layout.addWidget(self.password_input)

        options_layout = QHBoxLayout()
        
        self.show_pass_cb = QCheckBox("Show")
        self.show_pass_cb.stateChanged.connect(self.toggle_password_visibility)
        options_layout.addWidget(self.show_pass_cb)
        
        options_layout.addStretch()
        
        self.remember_cb = QCheckBox("Remember")
        self.remember_cb.setChecked(True)
        options_layout.addWidget(self.remember_cb)
        
        form_layout.addLayout(options_layout)
        layout.addWidget(self.form_container)

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.setProperty("class", "btn-primary")
        self.connect_btn.setFixedHeight(40)
        self.connect_btn.setCursor(Qt.PointingHandCursor)
        self.connect_btn.clicked.connect(self.on_connect_clicked)
        layout.addWidget(self.connect_btn)

        layout.addStretch()

    def set_network(self, ssid, is_secured):
        """Metoda wywoływana przez główne okno przy przełączaniu widoku"""
        self.current_network = ssid
        self.is_secured = is_secured
        self.network_ssid.setText(ssid)
        self.password_input.clear()
        self.connect_btn.setText("Connect")
        self.connect_btn.setEnabled(True)
        
        if is_secured:
            self.network_icon.setText("🔒")
            self.form_container.show()
            self.status_label.setText("Secured Network")
            self.password_input.setFocus()
        else:
            self.network_icon.setText("🔓")
            self.form_container.hide()
            self.status_label.setText("Open Network")

    def toggle_password_visibility(self, state):
        if state == Qt.Checked:
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)

    def on_connect_clicked(self):
        pwd = self.password_input.text()
        remember = self.remember_cb.isChecked()
        self.connect_signal.emit(self.current_network, pwd, remember)
        
        self.connect_btn.setText("Connecting...")
        self.connect_btn.setEnabled(False)