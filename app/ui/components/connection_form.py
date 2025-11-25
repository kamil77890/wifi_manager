from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class ConnectionForm(QWidget):
    connect_signal = pyqtSignal(str, str, bool)
    
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.current_network = None
        self.auto_connect_enabled = True
        self.init_ui()
        self.animation = None
    
    def init_ui(self):
        self.setObjectName("connection_form")
        self.setProperty("class", "bottom-sheet")
        self.setVisible(False)
        
        self.setWindowFlags(Qt.Widget)
        
        self.setMinimumWidth(380)
        self.setMinimumHeight(260)
        self.setMaximumWidth(500)
        
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(12)  # Mniejszy spacing
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setAlignment(Qt.AlignCenter)
        
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)
        header_layout.setSpacing(10)
        
        wifi_icon = QLabel("🌐")
        wifi_icon.setProperty("class", "form-title")
        wifi_icon.setStyleSheet("""
            font-size: 20px; 
            background: transparent;
            min-width: 30px;
        """)
        
        self.title_label = QLabel()
        self.title_label.setProperty("class", "form-title")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            background: transparent;
            font-size: 16px;
            font-weight: 600;
        """)
        self.title_label.setWordWrap(True)
        self.title_label.setMinimumHeight(30)
        
        header_layout.addWidget(wifi_icon)
        header_layout.addWidget(self.title_label)
        
        layout.addLayout(header_layout)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background: rgba(255, 255, 255, 0.1); border: none; height: 1px;")
        separator.setFixedHeight(1)
        layout.addWidget(separator)
        
        password_layout = QVBoxLayout()
        password_layout.setSpacing(8)
        password_layout.setAlignment(Qt.AlignCenter)
        
        password_label = QLabel("Enter Wi-Fi Password")
        password_label.setProperty("class", "form-subtitle")
        password_label.setAlignment(Qt.AlignCenter)
        password_label.setStyleSheet("""
            background: transparent;
            font-size: 13px;
            font-weight: 500;
            margin-bottom: 8px;
        """)
        password_layout.addWidget(password_label)
        
        password_input_layout = QHBoxLayout()
        password_input_layout.setAlignment(Qt.AlignCenter)
        password_input_layout.setSpacing(8)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter network password...")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(40)
        self.password_input.setProperty("class", "input-field")
        self.password_input.textChanged.connect(self.on_password_changed)
        self.password_input.returnPressed.connect(self.initiate_connection)
        
        self.toggle_visibility_btn = QPushButton("👁")
        self.toggle_visibility_btn.setFixedSize(40, 40)
        self.toggle_visibility_btn.setProperty("class", "password-toggle")
        self.toggle_visibility_btn.clicked.connect(self.toggle_password_visibility)
        
        password_input_layout.addWidget(self.password_input, 1)  
        password_input_layout.addWidget(self.toggle_visibility_btn)
        password_layout.addLayout(password_input_layout)
        
        self.auto_connect_cb = QCheckBox("Remember password and auto-connect")
        self.auto_connect_cb.setChecked(True)
        self.auto_connect_cb.setProperty("class", "checkbox")
        self.auto_connect_cb.setStyleSheet("""
            background: transparent;
            margin-top: 8px;
        """)
        password_layout.addWidget(self.auto_connect_cb, 0, Qt.AlignCenter)
        
        layout.addLayout(password_layout)
        
        layout.addSpacing(8)
        
        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setMinimumHeight(30)
        self.status_label.setProperty("class", "status-message status-info")
        self.status_label.setStyleSheet("""
            background: transparent;
            font-size: 12px;
            padding: 6px 12px;
        """)
        layout.addWidget(self.status_label)
        
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)
        buttons_layout.setAlignment(Qt.AlignCenter)
        
        self.hide_btn = QPushButton("Cancel")
        self.hide_btn.setMinimumSize(100, 36)
        self.hide_btn.setProperty("class", "btn-secondary")
        self.hide_btn.clicked.connect(self.hide_with_animation)
        
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.setMinimumSize(100, 36)
        self.connect_btn.setEnabled(False)
        self.connect_btn.setProperty("class", "btn-primary")
        self.connect_btn.clicked.connect(self.initiate_connection)
        
        buttons_layout.addWidget(self.hide_btn)
        buttons_layout.addWidget(self.connect_btn)
        
        layout.addLayout(buttons_layout)
        
        layout.addStretch(1)
        
        self.setStyleSheet("""
            QWidget#connection_form {
                background: rgba(26, 26, 46, 0.95);
                border: none;
                border-top: 1px solid rgba(139, 92, 246, 0.4);
                border-top-left-radius: 20px;
                border-top-right-radius: 20px;
                box-shadow: 0 -10px 50px rgba(0, 0, 0, 0.5);
            }
            
            .input-field {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 10px;
                padding: 10px 14px;
                color: #f8fafc;
                font-size: 14px;
                selection-background-color: rgba(139, 92, 246, 0.3);
                min-height: 40px;
            }
            
            .input-field:focus {
                border: 1px solid #8b5cf6;
                background: rgba(255, 255, 255, 0.12);
            }
            
            .input-field::placeholder {
                color: rgba(226, 232, 240, 0.5);
            }
            
            .btn-primary {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #8b5cf6, stop:0.5 #6366f1, stop:1 #0ea5e9);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 8px 16px;
                font-weight: 600;
                font-size: 13px;
                min-height: 36px;
            }
            
            .btn-primary:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7c3aed, stop:0.5 #4f46e5, stop:1 #0284c7);
            }
            
            .btn-secondary {
                background: rgba(255, 255, 255, 0.08);
                color: #e2e8f0;
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 10px;
                padding: 8px 16px;
                font-weight: 500;
                font-size: 13px;
                min-height: 36px;
            }
            
            .btn-secondary:hover {
                background: rgba(255, 255, 255, 0.12);
            }
            
            .password-toggle {
                background: rgba(255, 255, 255, 0.08);
                color: rgba(226, 232, 240, 0.7);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 8px;
                font-size: 14px;
            }
            
            .password-toggle:hover {
                background: rgba(255, 255, 255, 0.12);
                color: #e2e8f0;
            }
            
            .checkbox {
                color: rgba(226, 232, 240, 0.9);
                background: transparent;
                spacing: 8px;
                font-size: 12px;
            }
            
            .status-message {
                border-radius: 8px;
                font-weight: 500;
            }
            
            .status-info {
                background: rgba(14, 165, 233, 0.1);
                color: #0ea5e9;
                border: 1px solid rgba(14, 165, 233, 0.2);
            }
            
            .status-success {
                background: rgba(34, 197, 94, 0.1);
                color: #22c55e;
                border: 1px solid rgba(34, 197, 94, 0.2);
            }
            
            .status-warning {
                background: rgba(245, 158, 11, 0.1);
                color: #f59e0b;
                border: 1px solid rgba(245, 158, 11, 0.2);
            }
        """)
    
    def position_at_bottom(self):
        if not self.parent():
            return
            
        parent_rect = self.parent().rect()
        x = (parent_rect.width() - self.width()) // 2
        y = parent_rect.height()  
        
        self.move(x, y)
    
    def show_with_animation(self):
        if not self.parent():
            return
            
        self.adjustSize()
        
        self.position_at_bottom()
        self.show()
        self.raise_()  
        
        # Animacja wysuwania od dołu
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(400)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        
        parent_rect = self.parent().rect()
        start_pos = QPoint(self.x(), parent_rect.height())
        end_pos = QPoint(self.x(), parent_rect.height() - self.height())
        
        self.animation.setStartValue(start_pos)
        self.animation.setEndValue(end_pos)
        self.animation.start()
    
    def hide_with_animation(self):
        if not self.parent():
            return
            
        if self.animation and self.animation.state() == QPropertyAnimation.Running:
            return
            
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(400)
        self.animation.setEasingCurve(QEasingCurve.InCubic)
        
        parent_rect = self.parent().rect()
        start_pos = self.pos()
        end_pos = QPoint(self.x(), parent_rect.height())
        
        self.animation.setStartValue(start_pos)
        self.animation.setEndValue(end_pos)
        self.animation.finished.connect(self.hide)
        self.animation.start()
    
    def on_network_selected(self, ssid, is_secured, strength):
        self.current_network = ssid
        self.is_secured = is_secured
        
        self.title_label.setText(f"Connect to {ssid}")
        
        saved_password = self.config.get_saved_password(ssid)
        if saved_password:
            self.password_input.setText(saved_password)
        
        if not is_secured:
            self.password_input.setVisible(False)
            self.toggle_visibility_btn.setVisible(False)
            self.status_label.setText("🔓 Open network - no password required")
            self.status_label.setProperty("class", "status-message status-success")
            self.connect_btn.setEnabled(True)
        else:
            self.password_input.setVisible(True)
            self.toggle_visibility_btn.setVisible(True)
            self.status_label.setText("Enter password to connect to this network")
            self.status_label.setProperty("class", "status-message status-info")
            self.password_input.setFocus()
        
        self.style().polish(self.status_label)
        self.adjustSize()
        
        self.show_with_animation()
    
    def on_password_changed(self, text):
        if not self.is_secured:
            return
            
        is_enabled = bool(text.strip())
        self.connect_btn.setEnabled(is_enabled)
        
        if text:
            self.status_label.setText("✅ Ready to connect")
            self.status_label.setProperty("class", "status-message status-success")
        else:
            self.status_label.setText("Enter password to connect to this network")
            self.status_label.setProperty("class", "status-message status-info")
        
        self.style().polish(self.status_label)
    
    def toggle_password_visibility(self):
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_visibility_btn.setText("🔒")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.toggle_visibility_btn.setText("👁")
    
    def initiate_connection(self):
        if not self.current_network:
            return
            
        password = self.password_input.text().strip() if self.is_secured else None
        remember = self.auto_connect_cb.isChecked()
        
        self.status_label.setText("🔄 Connecting to network...")
        self.status_label.setProperty("class", "status-message status-warning")
        self.style().polish(self.status_label)
        
        self.connect_btn.setEnabled(False)
        self.connect_btn.setText("Connecting...")
        
        self.connect_signal.emit(self.current_network, password, remember)
        
        QTimer.singleShot(2000, self.hide_with_animation)
    
    def hide(self):
        super().hide()
        self.password_input.clear()
        self.connect_btn.setText("Connect")
        self.connect_btn.setEnabled(False)
        if self.toggle_visibility_btn.text() == "🔒":
            self.toggle_password_visibility()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        input_width = min(self.width() - 120, 300) 
        self.password_input.setMaximumWidth(input_width)