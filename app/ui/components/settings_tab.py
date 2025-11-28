from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class SettingsTab(QWidget):
    # Sygnał informujący główne okno o zmianie, żeby np. zaktualizować timer skanowania
    settings_changed = pyqtSignal(dict)

    def __init__(self, config, network_manager=None):
        super().__init__()
        self.config = config
        self.network_manager = network_manager
        self.init_ui()
        
        # WAŻNE: Wczytaj ustawienia z pliku przy starcie
        self.load_current_settings()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)
        
        # Tytuł
        title = QLabel("Settings")
        title.setObjectName("settings_title")
        title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 700;
                color: #10b981;
                background: transparent;
            }
        """)
        layout.addWidget(title)
        
        # --- Sekcja General ---
        self.general_group = self.create_group("General")
        
        self.auto_start_cb = self.create_checkbox("Start with system")
        self.minimize_tray_cb = self.create_checkbox("Minimize to tray")
        
        self.general_group.layout().addWidget(self.auto_start_cb)
        self.general_group.layout().addWidget(self.minimize_tray_cb)
        layout.addWidget(self.general_group)
        
        # --- Sekcja Appearance ---
        self.app_group = self.create_group("Appearance")
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Theme:")
        theme_label.setStyleSheet("color: #e4e4e7; font-size: 11px; font-weight: 600;")
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light", "Auto"])
        self.theme_combo.setStyleSheet(self.get_combo_style())
        # Zapisz przy zmianie
        self.theme_combo.currentTextChanged.connect(self.save_settings)
        
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        self.app_group.layout().addLayout(theme_layout)
        layout.addWidget(self.app_group)
        
        # --- Sekcja Connection ---
        self.conn_group = self.create_group("Connection")
        
        self.auto_scan_cb = self.create_checkbox("Auto-scan networks")
        self.auto_connect_cb = self.create_checkbox("Auto-connect to known")
        
        interval_layout = QHBoxLayout()
        interval_label = QLabel("Scan Interval:")
        interval_label.setStyleSheet("color: #e4e4e7; font-size: 11px; font-weight: 600;")
        
        self.scan_interval_combo = QComboBox()
        self.scan_interval_combo.addItems(["5s", "10s", "30s", "1m", "5m"])
        self.scan_interval_combo.setStyleSheet(self.get_combo_style())
        # Zapisz przy zmianie
        self.scan_interval_combo.currentTextChanged.connect(self.save_settings)
        
        interval_layout.addWidget(interval_label)
        interval_layout.addWidget(self.scan_interval_combo)
        interval_layout.addStretch()
        
        self.conn_group.layout().addWidget(self.auto_scan_cb)
        self.conn_group.layout().addWidget(self.auto_connect_cb)
        self.conn_group.layout().addLayout(interval_layout)
        
        layout.addWidget(self.conn_group)
        layout.addStretch()
    
    def create_group(self, title):
        group = QGroupBox(title)
        group.setStyleSheet("""
            QGroupBox {
                background: rgba(24, 24, 27, 0.65);
                border: 1.2px solid rgba(16, 185, 129, 0.35);
                border-radius: 7px;
                margin-top: 5px;
                padding: 10px 10px 6px 10px;
                font-size: 11px;
                color: #10b981;
                font-weight: 600;
            }
            QGroupBox::title {
                color: #10b981;
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                background: transparent;
            }
        """)
        l = QVBoxLayout()
        l.setSpacing(5)
        l.setContentsMargins(0, 5, 0, 0)
        group.setLayout(l)
        return group

    def create_checkbox(self, text):
        cb = QCheckBox(text)
        cb.setStyleSheet("""
            QCheckBox {
                color: #e4e4e7;
                background: transparent;
                spacing: 8px;
                font-size: 11px;
                font-weight: 500;
                padding: 3px 0px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1.5px solid rgba(16, 185, 129, 0.5);
                border-radius: 3px;
                background: rgba(255, 255, 255, 0.06);
            }
            QCheckBox::indicator:checked {
                background: #10b981;
                border: 1.5px solid #10b981;
            }
            QCheckBox::indicator:hover {
                border: 1.5px solid rgba(16, 185, 129, 0.8);
            }
        """)
        cb.stateChanged.connect(self.save_settings)
        return cb
    
    def get_combo_style(self):
        return """
            QComboBox {
                background: rgba(255, 255, 255, 0.07);
                border: 1.2px solid rgba(16, 185, 129, 0.35);
                border-radius: 5px;
                padding: 3px 6px;
                color: #ffffff;
                font-size: 11px;
                min-width: 80px;
            }
            QComboBox:hover { border: 1.2px solid rgba(16, 185, 129, 0.55); }
            QComboBox QAbstractItemView {
                background: #0a0e1a;
                border: 1px solid #333;
                selection-background-color: rgba(16, 185, 129, 0.35);
                color: #e4e4e7;
            }
        """

    def load_current_settings(self):
        """Pobiera dane z ConfigManager i ustawia stan kontrolek UI"""
        # Blokujemy sygnały, aby ustawianie wartości nie wywołało metody save_settings
        self.blockSignals(True)
        
        # Checkboxy (używamy kluczy z Twojego Config Managera)
        self.auto_start_cb.setChecked(self.config.get('auto_start', False))
        self.minimize_tray_cb.setChecked(self.config.get('minimize_to_tray', False))
        self.auto_scan_cb.setChecked(self.config.get('auto_scan', True))
        self.auto_connect_cb.setChecked(self.config.get('auto_connect', False))
        
        # ComboBox - Theme
        theme = self.config.get('theme', 'Dark')
        # Konwersja (np. 'dark' -> 'Dark')
        theme_idx = self.theme_combo.findText(theme.capitalize())
        if theme_idx >= 0:
            self.theme_combo.setCurrentIndex(theme_idx)
            
        # ComboBox - Scan Interval
        # Twój config domyślny ma '60' (int), ale combo ma stringi "5s", "1m".
        # Musimy to zmapować.
        interval_val = self.config.get('scan_interval', 60)
        
        # Mapa wartości int -> tekst w combo
        val_map = {5: "5s", 10: "10s", 30: "30s", 60: "1m", 300: "5m"}
        text_val = val_map.get(interval_val, "1m") # Domyślnie 1m
        
        interval_idx = self.scan_interval_combo.findText(text_val)
        if interval_idx >= 0:
            self.scan_interval_combo.setCurrentIndex(interval_idx)
        
        self.blockSignals(False)

    def save_settings(self):
        """Pobiera stan z UI i zapisuje przez ConfigManager"""
        
        # Parsowanie interwału (Tekst -> Sekundy Int)
        interval_text = self.scan_interval_combo.currentText()
        interval_sec = 60
        if interval_text.endswith('s'):
            interval_sec = int(interval_text[:-1])
        elif interval_text.endswith('m'):
            interval_sec = int(interval_text[:-1]) * 60

        self.config.set('auto_start', self.auto_start_cb.isChecked())
        self.config.set('minimize_to_tray', self.minimize_tray_cb.isChecked())
        self.config.set('theme', self.theme_combo.currentText().lower())
        self.config.set('auto_scan', self.auto_scan_cb.isChecked())
        self.config.set('auto_connect', self.auto_connect_cb.isChecked())
        self.config.set('scan_interval', interval_sec)
        
        settings_dict = {
            'auto_start': self.auto_start_cb.isChecked(),
            'minimize_to_tray': self.minimize_tray_cb.isChecked(),
            'auto_scan': self.auto_scan_cb.isChecked(),
            'auto_connect': self.auto_connect_cb.isChecked(),
            'scan_interval': interval_text # Przekazujemy tekst, bo ModernWifiWindow ma parser tekstu
        }
        
        self.settings_changed.emit(settings_dict)