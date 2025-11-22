from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class ConnectionForm(QWidget):
    connect_signal = pyqtSignal(str, str, bool)
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.current_network = None
        self.auto_connect_enabled = True
        self.init_ui()
    
    def init_ui(self):
        self.setObjectName("connection_form")
        self.setVisible(False)
        self.setFixedSize(320, 220)  # Mniejsze okno
        
        # Ustawienie jako niezależnego okna zawsze na wierzchu
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        
        # Main layout - bardziej zwarty
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Header z ikoną i tytułem
        header_layout = QHBoxLayout()
        
        wifi_icon = QLabel("📶")
        wifi_icon.setStyleSheet("""
            font-size: 18px; 
            background: transparent;
            padding: 2px;
        """)
        
        self.title_label = QLabel()
        self.title_label.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: white;
            background: transparent;
        """)
        self.title_label.setAlignment(Qt.AlignLeft)
        
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(20, 20)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(239, 83, 80, 0.2);
                color: #EF5350;
                border: 1px solid rgba(239, 83, 80, 0.4);
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(239, 83, 80, 0.3);
            }
        """)
        self.close_btn.clicked.connect(self.hide)
        
        header_layout.addWidget(wifi_icon)
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.close_btn)
        
        layout.addLayout(header_layout)
        
        # Delikatny separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background: rgba(255, 255, 255, 0.08); border: none; height: 1px;")
        separator.setFixedHeight(1)
        layout.addWidget(separator)
        
        # Sekcja hasła - bardziej kompaktowa
        password_layout = QVBoxLayout()
        password_layout.setSpacing(6)
        
        password_label = QLabel("Network Password:")
        password_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.9);
            font-size: 12px;
            font-weight: 500;
            background: transparent;
        """)
        password_layout.addWidget(password_label)
        
        # Input hasła z toggle - bardziej zwarty
        password_input_layout = QHBoxLayout()
        password_input_layout.setSpacing(8)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password...")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(32)
        self.password_input.textChanged.connect(self.on_password_changed)
        self.password_input.returnPressed.connect(self.initiate_connection)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 0.07);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 6px;
                padding: 6px 10px;
                color: white;
                font-size: 13px;
                selection-background-color: rgba(76, 175, 80, 0.3);
            }
            QLineEdit:focus {
                border: 1px solid rgba(76, 175, 80, 0.6);
                background: rgba(255, 255, 255, 0.1);
            }
        """)
        
        self.toggle_visibility_btn = QPushButton("👁")
        self.toggle_visibility_btn.setFixedSize(32, 32)
        self.toggle_visibility_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.08);
                color: rgba(255, 255, 255, 0.7);
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 6px;
                font-size: 12px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.12);
                color: white;
            }
        """)
        self.toggle_visibility_btn.clicked.connect(self.toggle_password_visibility)
        
        password_input_layout.addWidget(self.password_input)
        password_input_layout.addWidget(self.toggle_visibility_btn)
        password_layout.addLayout(password_input_layout)
        
        # Checkbox - mniejszy
        self.auto_connect_cb = QCheckBox("Remember and auto-connect")
        self.auto_connect_cb.setChecked(True)
        self.auto_connect_cb.setStyleSheet("""
            QCheckBox {
                color: rgba(255, 255, 255, 0.8);
                background: transparent;
                spacing: 6px;
                font-size: 11px;
            }
            QCheckBox::indicator {
                width: 14px;
                height: 14px;
                border-radius: 3px;
                border: 1.5px solid rgba(255, 255, 255, 0.3);
                background: rgba(255, 255, 255, 0.1);
            }
            QCheckBox::indicator:checked {
                background: #4CAF50;
                border: 1.5px solid #4CAF50;
            }
            QCheckBox::indicator:hover {
                border: 1.5px solid rgba(255, 255, 255, 0.5);
            }
        """)
        password_layout.addWidget(self.auto_connect_cb)
        
        layout.addLayout(password_layout)
        
        layout.addSpacing(8)
        
        # Status message - bardziej subtelny
        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFixedHeight(24)
        self.status_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.7);
            font-size: 11px;
            background: transparent;
            padding: 2px 4px;
        """)
        layout.addWidget(self.status_label)
        
        # Przyciski akcji - bardziej kompaktowe
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(8)
        
        self.hide_btn = QPushButton("Cancel")
        self.hide_btn.setFixedHeight(30)
        self.hide_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.08);
                color: rgba(255, 255, 255, 0.9);
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 6px;
                font-weight: 500;
                font-size: 12px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.12);
            }
        """)
        self.hide_btn.clicked.connect(self.hide)
        
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.setFixedHeight(30)
        self.connect_btn.setEnabled(False)
        self.connect_btn.setStyleSheet("""
            QPushButton {
                background: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #45a049;
            }
            QPushButton:pressed {
                background: #388E3C;
            }
            QPushButton:disabled {
                background: rgba(255, 255, 255, 0.08);
                color: rgba(255, 255, 255, 0.4);
            }
        """)
        self.connect_btn.clicked.connect(self.initiate_connection)
        
        buttons_layout.addWidget(self.hide_btn)
        buttons_layout.addWidget(self.connect_btn)
        
        layout.addLayout(buttons_layout)
        
        # Styl głównego okna
        self.setStyleSheet("""
            QWidget#connection_form {
                background: rgba(26, 26, 46, 0.98);
                border: 1px solid rgba(76, 175, 80, 0.3);
                border-radius: 10px;
            }
        """)
        
        # Position management dla przeciągania
        self.dragging = False
        self.offset = QPoint()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.frameGeometry().topLeft()
    
    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.offset)
    
    def mouseReleaseEvent(self, event):
        self.dragging = False
    
    def on_network_selected(self, ssid, is_secured, strength):
        self.current_network = ssid
        self.is_secured = is_secured
        
        # Update title with network name
        self.title_label.setText(ssid)
        
        # Load saved password
        saved_password = self.config.get_saved_password(ssid)
        if saved_password:
            self.password_input.setText(saved_password)
        
        # Configure form for network type
        if not is_secured:
            self.password_input.setVisible(False)
            self.toggle_visibility_btn.setVisible(False)
            self.status_label.setText("Open network - no password required")
            # Enable connect button immediately for open networks
            self.connect_btn.setEnabled(True)
        else:
            self.password_input.setVisible(True)
            self.toggle_visibility_btn.setVisible(True)
            self.status_label.setText("Enter password to connect")
            self.password_input.setFocus()
        
        # Position at absolute position (right side of screen)
        self.position_at_side()
        self.show()
        self.raise_()
        self.activateWindow()
    
    def position_at_side(self):
        """Position the popup at the right side of the screen"""
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        
        # Pozycjonowanie absolutne - prawa strona ekranu
        x = screen_geometry.width() - self.width() - 20  # 20px od prawej krawędzi
        y = (screen_geometry.height() - self.height()) // 2  # Wyśrodkowanie pionowe
        
        self.move(x, y)
    
    def position_near_cursor(self):
        """Position near mouse cursor"""
        cursor_pos = QCursor.pos()
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        
        x = cursor_pos.x() - self.width() // 2
        y = cursor_pos.y() - 50  # 50px nad kursorem
        
        # Upewnij się, że okno nie wychodzi poza ekran
        x = max(10, min(x, screen_geometry.width() - self.width() - 10))
        y = max(10, min(y, screen_geometry.height() - self.height() - 10))
        
        self.move(x, y)
    
    def on_password_changed(self, text):
        if not self.is_secured:
            return
            
        is_enabled = bool(text.strip())
        self.connect_btn.setEnabled(is_enabled)
        
        if text:
            self.status_label.setText("Ready to connect")
        else:
            self.status_label.setText("Enter password to connect")
    
    def toggle_password_visibility(self):
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_visibility_btn.setText("🔒")
            self.toggle_visibility_btn.setToolTip("Hide password")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.toggle_visibility_btn.setText("👁")
            self.toggle_visibility_btn.setToolTip("Show password")
    
    def initiate_connection(self):
        if not self.current_network:
            return
            
        password = self.password_input.text().strip() if self.is_secured else None
        remember = self.auto_connect_cb.isChecked()
        
        self.status_label.setText("Connecting...")
        self.connect_btn.setEnabled(False)
        self.connect_btn.setText("Connecting...")
        
        # Emit connection signal
        self.connect_signal.emit(self.current_network, password, remember)
        
        # Auto-hide after connection attempt
        QTimer.singleShot(1500, self.hide)
    
    def hide(self):
        super().hide()
        self.password_input.clear()
        self.connect_btn.setText("Connect")
        self.connect_btn.setEnabled(False)
        # Reset visibility button
        if self.toggle_visibility_btn.text() == "🔒":
            self.toggle_password_visibility()
    
    def keyPressEvent(self, event):
        """Handle Escape key to close"""
        if event.key() == Qt.Key_Escape:
            self.hide()
        else:
            super().keyPressEvent(event)