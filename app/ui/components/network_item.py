from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os

class NetworkItem(QFrame):
    connect_clicked = pyqtSignal(str, str, bool)  # ssid, password, remember
    network_selected = pyqtSignal(str, bool)      # ssid, is_secured

    def __init__(self, ssid, strength, is_secured, is_connected=False, parent=None):
        super().__init__(parent)
        self.ssid = ssid
        self.strength = int(strength)
        self.is_secured = is_secured
        self.is_connected = is_connected
        
        self.init_ui()

    def get_signal_icon_path(self):
        base_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
        if self.strength >= 70:
            icon_name = 'net_icon_3.png'
        elif self.strength >= 40:
            icon_name = 'net_icon_2.png'
        else:
            icon_name = 'net_icon_1.png'
        return os.path.normpath(os.path.join(base_path, icon_name))

    def init_ui(self):
        self.setObjectName("network_item_frame")
        self.setFrameShape(QFrame.StyledPanel)
        self.setFixedHeight(60) # Nieco wyższy dla lepszego "oddechu" (whitespace)
        self.setCursor(Qt.PointingHandCursor)

        if self.is_connected:
            self.setProperty("connected", "true")

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 2, 0, 2)
        self.main_layout.setSpacing(0)
        
        # Przezroczyste tło dla głównej ramki
        self.setStyleSheet("background: transparent;")

        # --- KONTENER WEWNĘTRZNY ---
        self.container = QFrame()
        self.container.setObjectName("inner_container")
        self.container_layout = QHBoxLayout(self.container)
        self.container_layout.setContentsMargins(16, 0, 16, 0)
        self.container_layout.setSpacing(16) # Większy odstęp między ikoną a tekstem
        
        # Szerokość 95%
        self.container.setFixedWidth(int(self.parent().width() * 0.95) if self.parent() else 330)

        # STYLE MINIMALISTYCZNE
        self.container.setStyleSheet("""
            QFrame#inner_container {
                background-color: transparent;
                border-radius: 8px;
                border: none;
            }
            /* Hover: Bardzo delikatne rozjaśnienie tła */
            QFrame#inner_container:hover {
                background-color: rgba(255, 255, 255, 0.04);
            }
            /* Connected: Subtelna zielona nuta */
            QFrame#inner_container[connected="true"] {
                background-color: rgba(16, 185, 129, 0.08);
            }
        """)
        
        # Jeśli połączony, ustaw property dla stylów
        if self.is_connected:
            self.container.setProperty("connected", "true")

        # 1. LEWA STRONA: Ikona sygnału
        signal_widget = self.create_signal_icon_widget()
        self.container_layout.addWidget(signal_widget)

        # 2. ŚRODEK: Informacje
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(2) # Tekst bliżej siebie
        info_layout.setAlignment(Qt.AlignVCenter)

        # Nazwa sieci (SSID)
        self.name_label = QLabel(self.ssid)
        self.name_label.setStyleSheet("""
            font-family: 'Segoe UI', sans-serif;
            font-weight: 600; 
            color: #f1f5f9; 
            font-size: 14px;
        """)
        info_layout.addWidget(self.name_label)

        # Status i ikona kłódki w jednej linii
        details_layout = QHBoxLayout()
        details_layout.setSpacing(8)
        
        self.status_label = QLabel(self.get_status_text())
        # Kolor szary (Slate-400), mniejszy font
        self.status_label.setStyleSheet("font-size: 11px; color: #94a3b8; font-weight: 400;")
        details_layout.addWidget(self.status_label)

        

        details_layout.addStretch()
        info_layout.addLayout(details_layout)
        
        self.container_layout.addLayout(info_layout, 1)

        # 3. PRAWA STRONA: Akcja
        # Usunięto tło (panel), teraz to po prostu layout
        self.right_layout = QHBoxLayout()
        self.right_layout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.right_layout.setContentsMargins(0,0,0,0)

        if self.is_connected:
            # Minimalistyczny "tick"
            connected_label = QLabel("Connected")
            connected_label.setStyleSheet("color: #10b981; font-size: 11px; font-weight: 600;")
            self.right_layout.addWidget(connected_label)
            
        elif self.is_secured:
            # Subtelna strzałka
            chevron_label = QLabel("›") # Używam znaku "chevron right" zamiast strzałki
            chevron_label.setStyleSheet("color: #475569; font-size: 24px; font-weight: 300; margin-bottom: 4px;") 
            # Na hover strzałka robi się zielona (obsłużone w mouseEnter/Leave rodzica lub globalnym CSS)
            self.chevron_label = chevron_label # referencja
            self.right_layout.addWidget(chevron_label)
            
        else:
            # Przycisk "Connect" - czysty tekst lub bardzo prosty guzik
            self.connect_btn = QPushButton("Connect")
            self.connect_btn.setFixedSize(60, 26)
            self.connect_btn.setCursor(Qt.PointingHandCursor)
            self.connect_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #10b981;
                    border: 1px solid rgba(16, 185, 129, 0.3);
                    border-radius: 4px;
                    font-weight: 600;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: rgba(16, 185, 129, 0.1);
                    border: 1px solid #10b981;
                }
            """)
            self.connect_btn.clicked.connect(self.connect_open_network)
            self.right_layout.addWidget(self.connect_btn)

        self.container_layout.addLayout(self.right_layout)

        # Centrowanie kontenera w głównym layoucie
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.container)
        self.main_layout.addStretch()

    def create_signal_icon_widget(self):
        icon_label = QLabel()
        icon_label.setFixedSize(24, 24) # Mniejsza ikona
        icon_label.setAlignment(Qt.AlignCenter)
        icon_path = self.get_signal_icon_path()
        
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            # Opcjonalnie: Przemaluj ikonę na biały/szary jeśli nie jest kolorowa
            pixmap = pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(pixmap)
        else:
            icon_label.setText("📶")
            # Bardziej stonowany kolor ikony (nie jaskrawy zielony)
            icon_label.setStyleSheet("font-size: 18px; color: #cbd5e1;") 
        return icon_label

    def get_status_text(self):
        if self.is_connected:
            return "Current network"
        strength_text = "Excellent" if self.strength >= 70 else "Good" if self.strength >= 40 else "Weak"

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.is_secured:
                self.network_selected.emit(self.ssid, True)
            else:
                self.connect_open_network()
        super().mousePressEvent(event)
        
    def enterEvent(self, event):
        if hasattr(self, 'chevron_label'):
             self.chevron_label.setStyleSheet("color: #10b981; font-size: 24px; font-weight: 300; margin-bottom: 4px;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        if hasattr(self, 'chevron_label'):
             self.chevron_label.setStyleSheet("color: #475569; font-size: 24px; font-weight: 300; margin-bottom: 4px;")
        super().leaveEvent(event)

    def connect_open_network(self):
        self.connect_clicked.emit(self.ssid, "", False)
        self.status_label.setText("Connecting...")
        self.status_label.setStyleSheet("color: #10b981;")