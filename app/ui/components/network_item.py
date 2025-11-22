from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class NetworkItem(QFrame):
    clicked = pyqtSignal(str, bool, int)
    
    def __init__(self, ssid, strength, is_secured, is_connected=False):
        super().__init__()
        self.ssid = ssid
        self.is_secured = is_secured
        self.is_connected = is_connected
        self.strength = strength
        self.init_ui()
    
    def init_ui(self):
        self.setMinimumHeight(70)
        self.setMaximumHeight(70)
        self.setCursor(Qt.PointingHandCursor)
        self.setObjectName("network_item")
        
        self.setAttribute(Qt.WA_Hover, True)
        if self.is_connected:
            self.setProperty("connected", "true")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)
        
        dot_label = QLabel()
        dot_label.setFixedSize(12, 12)
        dot_label.setPixmap(self.create_signal_dot())
        dot_label.setToolTip(f"Signal strength: {self.strength}%")
        layout.addWidget(dot_label)
        
        info_widget = QWidget()
        info_widget.setStyleSheet("background: transparent;")
        info_layout = QVBoxLayout(info_widget)
        info_layout.setSpacing(4)
        info_layout.setContentsMargins(0, 0, 0, 0)
        
        # Network name - bold and prominent
        name_label = QLabel(self.ssid)
        name_label.setObjectName("network_name")
        name_label.setStyleSheet("""
            QLabel#network_name {
                font-size: 16px;
                font-weight: bold;
                color: white;
                background: transparent;
            }
        """)
        info_layout.addWidget(name_label)
        
        # Status text - simple and clean
        status_label = self.create_status_label()
        info_layout.addWidget(status_label)
        
        info_layout.addStretch()
        layout.addWidget(info_widget, 1)
        
        # Security icon at the end - simple lock/unlock
        security_label = QLabel()
        security_label.setFixedSize(20, 20)
        security_label.setPixmap(self.create_security_icon())
        security_label.setToolTip("Secured network" if self.is_secured else "Open network")
        security_label.setStyleSheet("background: transparent;")
        layout.addWidget(security_label)
        
        # Apply modern styling without any background
        self.setStyleSheet("""
            QFrame#network_item {
                border-radius: 12px;
                margin: 2px;
                background: transparent;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            QFrame#network_item[connected="true"] {
                background: transparent;
                border: 1px solid rgba(76, 175, 80, 0.4);
            }
            QFrame#network_item:hover {
                background: transparent;
                border: 1px solid rgba(76, 175, 80, 0.6);
            }
        """)
    
    def create_signal_dot(self):
        """Create a colored dot indicating signal strength"""
        pixmap = QPixmap(12, 12)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Determine color based on connection and strength
        if self.is_connected:
            color = QColor("#4CAF50")  # Green for connected
        elif self.strength > 70:
            color = QColor("#4CAF50")  # Green for strong
        elif self.strength > 40:
            color = QColor("#FF9800")  # Orange for medium
        else:
            color = QColor("#F44336")  # Red for weak
        
        # Draw solid colored dot
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, 12, 12)
        
        painter.end()
        return pixmap
    
    def create_security_icon(self):
        """Create simple security icon (lock/unlock)"""
        pixmap = QPixmap(20, 20)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if self.is_secured:
            # Simple lock icon
            lock_color = QColor("#FFA726")  # Orange for secured
            
            # Lock body
            painter.setPen(QPen(lock_color, 2))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(5, 8, 10, 7, 2, 2)
            
            # Lock shackle
            painter.drawArc(3, 6, 14, 7, 0, 180 * 16)
        else:
            # Simple unlock icon
            unlock_color = QColor("#4CAF50")  # Green for open
            
            # Lock body (open)
            painter.setPen(QPen(unlock_color, 2))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(5, 8, 10, 7, 2, 2)
            
            # Open shackle
            painter.drawArc(7, 4, 6, 6, 45 * 16, 180 * 16)
        
        painter.end()
        return pixmap
    
    def create_status_label(self):
        if self.is_connected:
            text = "Connected"
            style = """
                QLabel {
                    color: #4CAF50;
                    font-size: 13px;
                    font-weight: 500;
                    background: transparent;
                }
            """
        elif self.is_secured:
            text = "Secured"
            style = """
                QLabel {
                    color: #FFA726;
                    font-size: 13px;
                    font-weight: 500;
                    background: transparent;
                }
            """
        else:
            text = "Open"
            style = """
                QLabel {
                    color: #4CAF50;
                    font-size: 13px;
                    font-weight: 500;
                    background: transparent;
                }
            """
        
        label = QLabel(text)
        label.setStyleSheet(style)
        return label
    
    def enterEvent(self, event):
        """Handle hover enter"""
        self.setStyleSheet("""
            QFrame#network_item {
                border: 1px solid rgba(76, 175, 80, 0.6);
                border-radius: 12px;
                background: transparent;
            }
            QFrame#network_item[connected="true"] {
                border: 1px solid rgba(76, 175, 80, 0.6);
                background: transparent;
            }
        """)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Handle hover leave"""
        self.setStyleSheet("""
            QFrame#network_item {
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                background: transparent;
            }
            QFrame#network_item[connected="true"] {
                border: 1px solid rgba(76, 175, 80, 0.4);
                background: transparent;
            }
        """)
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.animate_click()
            self.clicked.emit(self.ssid, self.is_secured, self.strength)
        super().mousePressEvent(event)
    
    def animate_click(self):
        """Simple click animation"""
        animation = QPropertyAnimation(self, b"geometry")
        animation.setDuration(100)
        animation.setKeyValueAt(0, self.geometry())
        animation.setKeyValueAt(0.3, QRect(
            self.x() - 1, self.y() - 1,
            self.width() + 2, self.height() + 2
        ))
        animation.setKeyValueAt(1, self.geometry())
        animation.start(QAbstractAnimation.DeleteWhenStopped)