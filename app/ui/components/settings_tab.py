from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class SettingsTab(QWidget):
    def __init__(self, config, network_manager=None):
        super().__init__()
        self.config = config
        self.network_manager = network_manager
        self.init_ui()
    
    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(250)
        sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setSpacing(0)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        
        # Sidebar header
        sidebar_header = QWidget()
        sidebar_header.setFixedHeight(120)
        sidebar_header.setObjectName("sidebar_header")
        sidebar_header_layout = QVBoxLayout(sidebar_header)
        sidebar_header_layout.setContentsMargins(20, 20, 20, 20)
        
        app_title = QLabel("Wi-Fi Manager")
        app_title.setObjectName("app_title")
        
        app_subtitle = QLabel("Professional Wireless Network Management")
        app_subtitle.setObjectName("app_subtitle")
        
        sidebar_header_layout.addWidget(app_title)
        sidebar_header_layout.addWidget(app_subtitle)
        sidebar_header_layout.addStretch()
        
        sidebar_layout.addWidget(sidebar_header)
        
        # Sidebar menu
        sidebar_menu = QWidget()
        sidebar_menu_layout = QVBoxLayout(sidebar_menu)
        sidebar_menu_layout.setSpacing(5)
        sidebar_menu_layout.setContentsMargins(10, 20, 10, 20)
        
        self.general_btn = QPushButton("📱 General")
        self.appearance_btn = QPushButton("🎨 Appearance")
        self.connections_btn = QPushButton("🔗 Connections")
        self.networks_btn = QPushButton("📶 Saved Networks")
        
        # Style menu buttons
        menu_buttons = [self.general_btn, self.appearance_btn, self.connections_btn, self.networks_btn]
        for btn in menu_buttons:
            btn.setFixedHeight(45)
            btn.setCheckable(True)
        
        self.general_btn.setChecked(True)
        
        sidebar_menu_layout.addWidget(self.general_btn)
        sidebar_menu_layout.addWidget(self.appearance_btn)
        sidebar_menu_layout.addWidget(self.connections_btn)
        sidebar_menu_layout.addWidget(self.networks_btn)
        sidebar_menu_layout.addStretch()
        
        sidebar_layout.addWidget(sidebar_menu)
        
        # Content area
        content_area = QWidget()
        content_area.setObjectName("content_area")
        content_layout = QVBoxLayout(content_area)
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Content header
        content_header = QWidget()
        content_header.setFixedHeight(80)
        content_header.setObjectName("content_header")
        content_header_layout = QHBoxLayout(content_header)
        content_header_layout.setContentsMargins(30, 0, 30, 0)
        
        self.content_title = QLabel("General Settings")
        self.content_title.setObjectName("content_title")
        
        content_header_layout.addWidget(self.content_title)
        content_header_layout.addStretch()
        
        content_layout.addWidget(content_header)
        
        # Content scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(25)
        scroll_layout.setContentsMargins(30, 30, 30, 30)
        
        # General Settings Section
        self.general_section = self.create_general_section()
        scroll_layout.addWidget(self.general_section)
        
        # Appearance Section (initially hidden)
        self.appearance_section = self.create_appearance_section()
        self.appearance_section.setVisible(False)
        scroll_layout.addWidget(self.appearance_section)
        
        # Connections Section (initially hidden)
        self.connections_section = self.create_connections_section()
        self.connections_section.setVisible(False)
        scroll_layout.addWidget(self.connections_section)
        
        # Saved Networks Section (initially hidden)
        self.networks_section = self.create_networks_section()
        self.networks_section.setVisible(False)
        scroll_layout.addWidget(self.networks_section)
        
        scroll_layout.addStretch()
        
        scroll_area.setWidget(scroll_content)
        content_layout.addWidget(scroll_area)
        
        main_layout.addWidget(sidebar)
        main_layout.addWidget(content_area)
        
        # Connect menu buttons
        self.general_btn.clicked.connect(lambda: self.show_section("general"))
        self.appearance_btn.clicked.connect(lambda: self.show_section("appearance"))
        self.connections_btn.clicked.connect(lambda: self.show_section("connections"))
        self.networks_btn.clicked.connect(lambda: self.show_section("networks"))
    
    def create_general_section(self):
        section = QWidget()
        layout = QVBoxLayout(section)
        layout.setSpacing(20)
        
        # Basic Settings Group
        basic_group = QGroupBox("Basic Settings")
        basic_group.setObjectName("settings_group")
        basic_layout = QVBoxLayout(basic_group)
        basic_layout.setSpacing(15)
        
        # Auto-start
        auto_start_layout = QHBoxLayout()
        auto_start_label = QLabel("Start with system:")
        auto_start_label.setObjectName("setting_label")
        self.auto_start_cb = QCheckBox()
        self.auto_start_cb.setChecked(True)
        auto_start_layout.addWidget(auto_start_label)
        auto_start_layout.addStretch()
        auto_start_layout.addWidget(self.auto_start_cb)
        basic_layout.addLayout(auto_start_layout)
        
        # Minimize to tray
        minimize_layout = QHBoxLayout()
        minimize_label = QLabel("Minimize to system tray:")
        minimize_label.setObjectName("setting_label")
        self.minimize_cb = QCheckBox()
        self.minimize_cb.setChecked(True)
        minimize_layout.addWidget(minimize_label)
        minimize_layout.addStretch()
        minimize_layout.addWidget(self.minimize_cb)
        basic_layout.addLayout(minimize_layout)
        
        layout.addWidget(basic_group)
        
        # Apply button
        apply_btn = QPushButton("Apply Settings")
        apply_btn.setFixedHeight(45)
        layout.addWidget(apply_btn)
        
        return section
    
    def create_appearance_section(self):
        section = QWidget()
        layout = QVBoxLayout(section)
        layout.setSpacing(20)
        
        # Theme Settings
        theme_group = QGroupBox("Appearance Settings")
        theme_group.setObjectName("settings_group")
        theme_layout = QVBoxLayout(theme_group)
        theme_layout.setSpacing(15)
        
        # Theme selection
        theme_select_layout = QHBoxLayout()
        theme_label = QLabel("Theme:")
        theme_label.setObjectName("setting_label")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark Mode", "Light Mode", "Auto"])
        self.theme_combo.setFixedHeight(35)
        theme_select_layout.addWidget(theme_label)
        theme_select_layout.addStretch()
        theme_select_layout.addWidget(self.theme_combo)
        theme_layout.addLayout(theme_select_layout)
        
        # Opacity
        opacity_layout = QHBoxLayout()
        opacity_label = QLabel("Window opacity:")
        opacity_label.setObjectName("setting_label")
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(50, 100)
        self.opacity_slider.setValue(95)
        self.opacity_value = QLabel("95%")
        opacity_layout.addWidget(opacity_label)
        opacity_layout.addWidget(self.opacity_slider)
        opacity_layout.addWidget(self.opacity_value)
        theme_layout.addLayout(opacity_layout)
        
        layout.addWidget(theme_group)
        return section
    
    def create_connections_section(self):
        section = QWidget()
        layout = QVBoxLayout(section)
        layout.setSpacing(20)
        
        # Connection Settings
        conn_group = QGroupBox("Connection Settings")
        conn_group.setObjectName("settings_group")
        conn_layout = QVBoxLayout(conn_group)
        conn_layout.setSpacing(15)
        
        # Auto-scan
        auto_scan_layout = QHBoxLayout()
        auto_scan_label = QLabel("Automatically scan for networks:")
        auto_scan_label.setObjectName("setting_label")
        self.auto_scan_cb = QCheckBox()
        self.auto_scan_cb.setChecked(True)
        auto_scan_layout.addWidget(auto_scan_label)
        auto_scan_layout.addStretch()
        auto_scan_layout.addWidget(self.auto_scan_cb)
        conn_layout.addLayout(auto_scan_layout)
        
        # Auto-connect
        auto_connect_layout = QHBoxLayout()
        auto_connect_label = QLabel("Auto-connect to known networks:")
        auto_connect_label.setObjectName("setting_label")
        self.auto_connect_cb = QCheckBox()
        self.auto_connect_cb.setChecked(True)
        auto_connect_layout.addWidget(auto_connect_label)
        auto_connect_layout.addStretch()
        auto_connect_layout.addWidget(self.auto_connect_cb)
        conn_layout.addLayout(auto_connect_layout)
        
        # Scan interval
        scan_interval_layout = QHBoxLayout()
        scan_interval_label = QLabel("Scan interval:")
        scan_interval_label.setObjectName("setting_label")
        self.scan_interval_combo = QComboBox()
        self.scan_interval_combo.addItems(["30 seconds", "1 minute", "2 minutes", "5 minutes"])
        self.scan_interval_combo.setCurrentIndex(1)
        self.scan_interval_combo.setFixedHeight(35)
        scan_interval_layout.addWidget(scan_interval_label)
        scan_interval_layout.addStretch()
        scan_interval_layout.addWidget(self.scan_interval_combo)
        conn_layout.addLayout(scan_interval_layout)
        
        # Notifications
        notify_layout = QHBoxLayout()
        notify_label = QLabel("Enable connection notifications:")
        notify_label.setObjectName("setting_label")
        self.notify_cb = QCheckBox()
        self.notify_cb.setChecked(True)
        notify_layout.addWidget(notify_label)
        notify_layout.addStretch()
        notify_layout.addWidget(self.notify_cb)
        conn_layout.addLayout(notify_layout)
        
        layout.addWidget(conn_group)
        return section
    
    def create_networks_section(self):
        section = QWidget()
        layout = QVBoxLayout(section)
        layout.setSpacing(20)
        
        # Saved Networks
        networks_group = QGroupBox("Saved Networks")
        networks_group.setObjectName("settings_group")
        networks_layout = QVBoxLayout(networks_group)
        
        # Networks list
        self.networks_list = QListWidget()
        self.networks_list.setFixedHeight(300)
        
        # Add sample networks
        sample_networks = ["Home_WiFi", "Office_Network", "Guest_WiFi", "AndroidAP"]
        for network in sample_networks:
            item = QListWidgetItem(f"📶 {network}")
            self.networks_list.addItem(item)
        
        networks_layout.addWidget(self.networks_list)
        
        # Network buttons
        network_buttons_layout = QHBoxLayout()
        
        forget_btn = QPushButton("Forget Selected")
        forget_btn.setFixedHeight(35)
        
        clear_btn = QPushButton("Clear All")
        clear_btn.setFixedHeight(35)
        
        network_buttons_layout.addWidget(forget_btn)
        network_buttons_layout.addWidget(clear_btn)
        
        networks_layout.addLayout(network_buttons_layout)
        
        layout.addWidget(networks_group)
        return section
    
    def show_section(self, section_name):
        # Hide all sections
        self.general_section.setVisible(False)
        
        self.networks_btn.setChecked(False)
        
        # Show selected section
        if section_name == "general":
            self.general_section.setVisible(True)
            self.general_btn.setChecked(True)
            self.content_title.setText("General Settings")
        elif section_name == "appearance":
            self.appearance_section.setVisible(True)
            self.appearance_btn.setChecked(True)
            self.content_title.setText("Appearance Settings")
        elif section_name == "connections":
            self.connections_section.setVisible(True)
            self.connections_btn.setChecked(True)
            self.content_title.setText("Connection Settings")
        elif section_name == "networks":
            self.networks_section.setVisible(True)
            self.networks_btn.setChecked(True)
            self.content_title.setText("Saved Networks")