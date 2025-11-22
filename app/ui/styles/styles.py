class UnifiedStyles:
    """Centralized modern styles for the entire application"""
    
    @staticmethod
    def get_stylesheet():
        return """
            /* ===== MODERN WIFI MANAGER STYLES ===== */
            
            /* Base Application */
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a2e, stop:0.5 #16213e, stop:1 #0f3460);
                color: #ffffff;
                font-family: 'Segoe UI', 'SF Pro Display', system-ui;
                font-size: 14px;
                border: none;
            }
            
            /* Main Header */
            QWidget#main_header {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(76, 175, 80, 0.3), stop:1 rgba(33, 150, 243, 0.2));
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            QLabel#main_title {
                font-size: 32px;
                font-weight: bold;
                color: #4CAF50;
                background: transparent;
            }
            
            QLabel#main_subtitle {
                font-size: 14px;
                color: rgba(255, 255, 255, 0.7);
                background: transparent;
            }
            
            /* Mock Data Label */
            QLabel#mock_label {
                color: #FFA726;
                font-weight: bold;
                background: rgba(255, 167, 38, 0.1);
                border: 1px solid rgba(255, 167, 38, 0.3);
                border-radius: 10px;
                padding: 8px 16px;
            }
            
            /* Tab Widget */
            QTabWidget::pane {
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                background: rgba(30, 30, 46, 0.8);
            }
            
            QTabBar::tab {
                background: rgba(255, 255, 255, 0.05);
                color: rgba(255, 255, 255, 0.7);
                padding: 12px 24px;
                margin: 5px;
                border-radius: 8px;
                font-weight: 500;
                font-size: 14px;
            }
            
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4CAF50, stop:1 #2196F3);
                color: white;
                font-weight: 600;
            }
            
            QTabBar::tab:hover:!selected {
                background: rgba(76, 175, 80, 0.2);
                color: white;
            }
            
            /* Network List */
            QWidget#network_list_container {
                background: transparent;
            }
            
            QWidget#loading_widget {
                background: transparent;
            }
            
            QLabel#loading_icon {
                font-size: 48px;
                color: #4CAF50;
            }
            
            QLabel#loading_text {
                color: #4CAF50;
                font-size: 16px;
                font-weight: 500;
            }
            
            QWidget#networks_container {
                background: transparent;
            }
            
            QLabel#no_networks_label {
                color: #FFA726;
                font-size: 16px;
                padding: 40px;
            }
            
            QLabel#error_label {
                color: #EF5350;
                font-size: 14px;
                padding: 30px;
            }
            
            /* Refresh Button */
            QPushButton#refresh_button {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4CAF50, stop:1 #2196F3);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 24px;
                font-weight: 600;
                font-size: 14px;
            }
            
            QPushButton#refresh_button:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #45a049, stop:1 #1976D2);
            }
            
            QPushButton#refresh_button:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #388E3C, stop:1 #1565C0);
            }
            
            /* Network Items */
            QFrame#network_item {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
            }
            
            QFrame#network_item[connected="true"] {
                background: rgba(76, 175, 80, 0.15);
                border: 1px solid rgba(76, 175, 80, 0.4);
            }
            
            QFrame#network_item:hover {
                background: rgba(76, 175, 80, 0.2);
                border: 1px solid rgba(76, 175, 80, 0.6);
            }
            
            QLabel#network_name {
                color: white;
                font-size: 16px;
                font-weight: 600;
                background: transparent;
            }
            
            QLabel#status_connected {
                color: #4CAF50;
                font-size: 12px;
                font-weight: 500;
                background: rgba(76, 175, 80, 0.2);
                padding: 4px 12px;
                border-radius: 8px;
            }
            
            QLabel#status_secured {
                color: #FFA726;
                font-size: 12px;
                font-weight: 500;
                background: rgba(255, 167, 38, 0.2);
                padding: 4px 12px;
                border-radius: 8px;
            }
            
            QLabel#status_open {
                color: #2196F3;
                font-size: 12px;
                font-weight: 500;
                background: rgba(33, 150, 243, 0.2);
                padding: 4px 12px;
                border-radius: 8px;
            }
            
            QLabel#strength_percent {
                color: white;
                font-size: 12px;
                font-weight: 600;
                background: transparent;
            }
            
            /* Connection Form */
            QWidget#connection_form {
                background: rgba(30, 30, 46, 0.9);
                border: 1px solid rgba(76, 175, 80, 0.3);
                border-radius: 12px;
            }
            
            QLabel#form_title {
                color: white;
                font-size: 18px;
                font-weight: 600;
                background: transparent;
            }
            
            QPushButton#close_button {
                background: rgba(239, 83, 80, 0.2);
                color: #EF5350;
                border: 1px solid rgba(239, 83, 80, 0.4);
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
            }
            
            QPushButton#close_button:hover {
                background: rgba(239, 83, 80, 0.3);
            }
            
            QLabel#network_info {
                color: white;
                font-size: 14px;
                background: transparent;
                padding: 10px;
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.05);
            }
            
            QLineEdit#password_input {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                padding: 10px 15px;
                color: white;
                font-size: 14px;
            }
            
            QLineEdit#password_input:focus {
                border: 1px solid #4CAF50;
                background: rgba(255, 255, 255, 0.15);
            }
            
            QPushButton#toggle_password {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
            }
            
            QPushButton#toggle_password:hover {
                background: rgba(255, 255, 255, 0.2);
            }
            
            QCheckBox#show_password_cb, QCheckBox#remember_cb {
                color: rgba(255, 255, 255, 0.8);
                background: transparent;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                background: rgba(255, 255, 255, 0.1);
            }
            
            QCheckBox::indicator:checked {
                background: #4CAF50;
                border: 2px solid #4CAF50;
            }
            
            QPushButton#cancel_button {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: 500;
            }
            
            QPushButton#cancel_button:hover {
                background: rgba(255, 255, 255, 0.2);
            }
            
            QPushButton#connect_button {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4CAF50, stop:1 #2196F3);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: 600;
            }
            
            QPushButton#connect_button:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #45a049, stop:1 #1976D2);
            }
            
            QPushButton#connect_button:disabled {
                background: rgba(255, 255, 255, 0.1);
                color: rgba(255, 255, 255, 0.4);
            }
            
            QLabel#status_label {
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 13px;
            }
            
            QLabel#status_label[status="info"] {
                color: #2196F3;
                background: rgba(33, 150, 243, 0.1);
                border: 1px solid rgba(33, 150, 243, 0.3);
            }
            
            QLabel#status_label[status="loading"] {
                color: #FFA726;
                background: rgba(255, 167, 38, 0.1);
                border: 1px solid rgba(255, 167, 38, 0.3);
            }
            
            /* Settings Tab */
            QGroupBox#settings_group {
                background: rgba(30, 30, 46, 0.8);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                margin-top: 10px;
                padding-top: 15px;
                font-weight: 600;
                color: white;
            }
            
            QGroupBox::title {
                color: #4CAF50;
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                background: transparent;
            }
            
            QComboBox {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                padding: 8px 12px;
                color: white;
                min-width: 120px;
            }
            
            QComboBox:hover {
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            
            QComboBox::drop-down {
                border-left: 1px solid rgba(255, 255, 255, 0.2);
                width: 20px;
            }
            
            QComboBox QAbstractItemView {
                background: rgba(30, 30, 46, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: white;
                selection-background-color: #4CAF50;
            }
            
            QListWidget#saved_networks_list {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                color: white;
                outline: none;
            }
            
            QListWidget::item {
                padding: 10px 15px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            }
            
            QListWidget::item:selected {
                background: rgba(76, 175, 80, 0.3);
                color: white;
            }
            
            QListWidget::item:hover {
                background: rgba(76, 175, 80, 0.2);
            }
            
            QPushButton#danger_button {
                background: rgba(239, 83, 80, 0.2);
                color: #EF5350;
                border: 1px solid rgba(239, 83, 80, 0.4);
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 500;
            }
            
            QPushButton#danger_button:hover {
                background: rgba(239, 83, 80, 0.3);
            }
            
            QPushButton#apply_button {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4CAF50, stop:1 #2196F3);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 30px;
                font-weight: 600;
                font-size: 14px;
                min-width: 150px;
            }
            
            QPushButton#apply_button:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #45a049, stop:1 #1976D2);
            }
            
            /* Scrollbars */
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.05);
                width: 12px;
                border-radius: 6px;
                margin: 2px;
            }
            
            QScrollBar::handle:vertical {
                background: rgba(76, 175, 80, 0.5);
                border-radius: 6px;
                min-height: 30px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: rgba(76, 175, 80, 0.7);
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            /* Message Boxes */
            QMessageBox {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a2e, stop:1 #16213e);
                color: white;
            }
            
            QMessageBox QLabel {
                color: white;
            }
            
            QMessageBox QPushButton {
                background: rgba(76, 175, 80, 0.3);
                color: white;
                border: 1px solid rgba(76, 175, 80, 0.5);
                border-radius: 6px;
                padding: 8px 16px;
                min-width: 80px;
            }
            
            QMessageBox QPushButton:hover {
                background: rgba(76, 175, 80, 0.5);
            }
        """