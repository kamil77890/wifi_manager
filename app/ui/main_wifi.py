from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading

# --- IMPORTY KOMPONENTÓW ---
from app.ui.components.wifi_switch import ModernWiFiSwitch
from app.ui.components.network_list import NetworkList
from app.ui.components.settings_tab import SettingsTab
from app.ui.components.connection_form import ConnectionForm
from app.ui.styles.styles import UnifiedStyles  # Upewnij się, że ścieżka jest poprawna

class ModernWifiWindow(QWidget):
    networks_updated = pyqtSignal(list)

    def __init__(self, network_manager, config):
        super().__init__()
        self.network_manager = network_manager
        self.config = config
        self.wifi_on = True
        
        self.init_ui()
        
        # Sygnały
        self.networks_updated.connect(self.on_networks_updated)
        self.network_manager.connection_changed.connect(self.on_connection_changed)

        # Aplikujemy ustawienia startowe (Theme, Scan interval, etc.)
        self.apply_settings()

    def init_ui(self):
        self.setWindowTitle("Wi-Fi Manager")
        self.setObjectName("main_window") # Kluczowe dla tła z CSS
        self.resize(340, 420)
        
        # --- FLAGI OKNA ---
        # Qt.Tool: Ukrywa okno z paska zadań i Alt+Tab
        # Qt.FramelessWindowHint: Usuwa systemową belkę tytułową
        # Qt.WindowStaysOnTopHint: Okno zawsze na wierzchu
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_StyledBackground, True)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ================= HEADER =================
        header = QWidget()
        header.setFixedHeight(56)
        header.setObjectName("main_header") # Styl zdefiniowany w UnifiedStyles
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 0, 16, 0)
        header_layout.setSpacing(12)
        
        self.back_btn = QPushButton("←")
        self.back_btn.setObjectName("header_back_btn")
        self.back_btn.setFixedSize(32, 32)
        self.back_btn.setCursor(Qt.PointingHandCursor)
        self.back_btn.hide()
        self.back_btn.clicked.connect(self.go_back_to_list)
        header_layout.addWidget(self.back_btn)

        self.title_label = QLabel("Wi-Fi")
        self.title_label.setObjectName("header_title")
        header_layout.addWidget(self.title_label)
        
        header_layout.addStretch()
        
        self.wifi_toggle = ModernWiFiSwitch()
        self.wifi_toggle.setChecked(True)
        self.wifi_toggle.toggled.connect(self.on_wifi_toggle)
        header_layout.addWidget(self.wifi_toggle)
        
        main_layout.addWidget(header)

        # ================= STACK (STRONY) =================
        self.stacked_widget = QStackedWidget()
        # Brak sztywnego stylu - tło ustawi CSS
        
        # 1. Lista Sieci
        self.network_list = NetworkList(self.network_manager, parent=None)
        self.network_list.network_clicked.connect(self.show_connection_form)
        self.stacked_widget.addWidget(self.network_list)

        # 2. Ustawienia
        self.settings_tab = SettingsTab(self.config, self.network_manager)
        self.settings_tab.settings_changed.connect(self.apply_settings)
        self.stacked_widget.addWidget(self.settings_tab)

        # 3. Formularz Połączenia
        self.connection_form = ConnectionForm(self.config, self)
        self.connection_form.connect_signal.connect(self.handle_connect_request)
        self.stacked_widget.addWidget(self.connection_form)
        
        main_layout.addWidget(self.stacked_widget, 1)

        # ================= BOTTOM BAR =================
        self.bottom_bar = QWidget()
        self.bottom_bar.setObjectName("bottom_bar") # Styl zdefiniowany w UnifiedStyles
        self.bottom_bar.setFixedHeight(44)
        
        layout_b = QHBoxLayout(self.bottom_bar)
        layout_b.setContentsMargins(14, 0, 14, 0)
        
        self.current_network_label = QLabel("Initializing...")
        self.current_network_label.setObjectName("network_status") # Używamy ID dla spójności czcionki
        # Nadpisujemy kolor statusu dynamicznie w update_status_label, więc tutaj styl podstawowy wystarczy
        layout_b.addWidget(self.current_network_label)
        
        layout_b.addStretch()
        
        settings_btn = QPushButton("⚙️")
        settings_btn.setObjectName("settings_btn")
        settings_btn.setFixedSize(32, 32)
        settings_btn.setCursor(Qt.PointingHandCursor)
        settings_btn.clicked.connect(self.toggle_settings)
        layout_b.addWidget(settings_btn)
        
        main_layout.addWidget(self.bottom_bar)

        # --- LOGIKA STARTOWA ---
        self.scan_timer = QTimer()
        self.scan_timer.timeout.connect(self.trigger_initial_scan)
        # Timer zostanie uruchomiony/skonfigurowany w apply_settings

        QTimer.singleShot(500, self.trigger_initial_scan)
        QTimer.singleShot(100, self.position_at_bottom_right)
        self.update_status_label(None, "disconnected")
        
        QApplication.instance().installEventFilter(self)

    # --- ZARZĄDZANIE KONFIGURACJĄ I MOTYWEM ---

    def apply_settings(self, settings=None):
        """
        Reaguje na zmiany w configu (lub inicjalizuje przy starcie).
        Obsługuje zmianę motywu, interwału skanowania i auto-scan.
        """
        # 1. Pobierz ustawienia (z argumentu lub z configu)
        theme = self.config.get('theme', 'dark')
        interval_str = self.config.get('scan_interval', '5s')
        auto_scan = self.config.get('auto_scan', True)

        # 2. APLIKACJA MOTYWU (Dark/Light)
        # Sprawdzamy, czy motyw faktycznie się zmienił, żeby nie mrugać niepotrzebnie
        if not hasattr(self, '_current_theme') or self._current_theme != theme:
            print(f"[UI] Applying theme: {theme}")
            new_stylesheet = UnifiedStyles.get_stylesheet(theme)
            QApplication.instance().setStyleSheet(new_stylesheet)
            self._current_theme = theme
            self.update() # Wymuś przerysowanie

        # 3. Interwał skanowania
        ms = self.parse_interval(interval_str)
        if self.scan_timer.interval() != ms:
            self.scan_timer.setInterval(ms)

        # 4. Auto-Scan
        if auto_scan and not self.scan_timer.isActive() and self.wifi_on:
            self.scan_timer.start()
        elif not auto_scan and self.scan_timer.isActive():
            self.scan_timer.stop()

    def parse_interval(self, text):
        text = str(text).lower()
        if text.endswith('s'): return int(text[:-1]) * 1000
        if text.endswith('m'): return int(text[:-1]) * 60000
        return 5000

    # --- ZDARZENIA SYSTEMOWE ---

    def closeEvent(self, event):
        """Tylko ukrywa okno, aplikacja żyje w trayu"""
        event.ignore()
        self.hide()

    def eventFilter(self, obj, event):
        """Zamykanie po kliknięciu poza obszarem okna"""
        if event.type() == QEvent.MouseButtonPress and self.isVisible():
            if not self.frameGeometry().contains(event.globalPos()):
                self.hide()
                return True
        return False

    # --- LOGIKA SIECI ---

    def on_networks_updated(self, networks):
        current = getattr(self.network_manager, "current_network", None)
        
        # Logika Auto-Connect
        auto_connect = self.config.get('auto_connect', False)
        if auto_connect and not current and "Connecting" not in self.current_network_label.text():
            # Tutaj można w przyszłości dodać logikę łączenia ze znanymi sieciami
            pass

        # Aktualizacja statusu
        if current: 
            self.update_status_label(current, "connected")
        elif self.current_network_label.text().startswith("Connecting"): 
            pass 
        else: 
            self.update_status_label(None, "disconnected")

        # Sortowanie i wyświetlanie
        for net in networks:
            net["connected"] = (net["ssid"] == current)
        
        # Sortowanie: połączona -> siła sygnału
        networks.sort(key=lambda x: (not x["connected"], -x.get("strength", 0)))
        self.network_list.display_networks(networks)

    def update_status_label(self, ssid=None, state="disconnected"):
        """Aktualizuje tekst i kolor dolnego paska statusu"""
        if not self.wifi_on:
            self.current_network_label.setText("Wi-Fi Off")
            self.current_network_label.setStyleSheet("color: #71717a; font-size: 12px;") # Szary
            return

        if state == "connecting":
            text = f"Connecting to {ssid}..." if ssid else "Connecting..."
            self.current_network_label.setText(text)
            self.current_network_label.setStyleSheet("color: #f59e0b; font-size: 12px; font-weight: 500;") # Pomarańczowy
        
        elif state == "connected" and ssid:
            self.current_network_label.setText(f"Connected: {ssid}")
            self.current_network_label.setStyleSheet("color: #10b981; font-size: 12px; font-weight: bold;") # Zielony
        
        else:
            self.current_network_label.setText("Not connected")
            self.current_network_label.setStyleSheet("color: #94a3b8; font-size: 12px;") # Jasny szary

    def handle_connect_request(self, ssid, password, remember):
        self.go_back_to_list()
        self.update_status_label(ssid, "connecting")
        
        # Jeśli remember jest True, można tu zapisać hasło w ConfigManager
        if remember:
            # self.config.save_network(ssid, password) # Jeśli zaimplementowane
            pass

        self.network_manager.connect_to_network(ssid, password)
        self.trigger_initial_scan()

    def on_connection_changed(self, ssid):
        self.network_manager.current_network = ssid
        if ssid: 
            self.update_status_label(ssid, "connected")
        else: 
            self.update_status_label(None, "disconnected")
        self.trigger_initial_scan()

    def on_wifi_toggle(self, state):
        self.wifi_on = state
        self.apply_settings() # Re-aplikuj timery
        
        if state:
            self.trigger_initial_scan()
            self.network_list.setEnabled(True)
            current = self.network_manager.current_network
            if current: self.update_status_label(current, "connected")
            else: self.update_status_label(None, "disconnected")
        else:
            self.update_status_label(None, "off")
            self.network_list.display_networks([])
            self.network_list.setEnabled(False)
            self.scan_timer.stop()

    def trigger_initial_scan(self):
        # Nie skanuj, jeśli użytkownik wpisuje hasło lub wifi wyłączone
        if not self.wifi_on or self.stacked_widget.currentWidget() == self.connection_form: 
            return
        
        def scan():
            nets = self.network_manager.scan_networks() if hasattr(self.network_manager, "scan_networks") else []
            self.networks_updated.emit(nets)
        
        threading.Thread(target=scan, daemon=True).start()

    # --- NAWIGACJA UI ---

    def show_connection_form(self, ssid, is_secured):
        self.connection_form.set_network(ssid, is_secured)
        self.stacked_widget.setCurrentWidget(self.connection_form)
        self.back_btn.show()
        self.wifi_toggle.hide()
        self.title_label.setText("Connect")
        self.bottom_bar.hide()

    def go_back_to_list(self):
        self.stacked_widget.setCurrentWidget(self.network_list)
        self.back_btn.hide()
        self.wifi_toggle.show()
        self.title_label.setText("Wi-Fi")
        self.bottom_bar.show()

    def toggle_settings(self):
        if self.stacked_widget.currentWidget() == self.connection_form:
            self.go_back_to_list()
        
        current = self.stacked_widget.currentWidget()
        if current == self.settings_tab:
            self.go_back_to_list()
        else:
            self.stacked_widget.setCurrentWidget(self.settings_tab)
            self.back_btn.show()
            try: self.back_btn.clicked.disconnect()
            except: pass
            self.back_btn.clicked.connect(self.toggle_settings)
            
            self.wifi_toggle.hide()
            self.title_label.setText("Settings")

    def position_at_bottom_right(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.width() - self.width() - 10
        y = screen.height() - self.height() - 10
        self.move(x, y)