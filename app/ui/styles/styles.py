class UnifiedStyles:
    """Modern dark theme with vibrant green accents"""

    @staticmethod
    def get_stylesheet():
        return """
            /* ===== MODERN DARK THEME WITH GREEN ACCENTS ===== */
            
            /* Base Application */
            QWidget {
                background: #0a0e1a;
                color: #e4e4e7;
                font-family: 'Segoe UI', 'SF Pro Display', -apple-system, system-ui;
                font-size: 14px;
                border: none;
            }
            
            /* Main Header */
            QWidget#main_header {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(16, 185, 129, 0.15), stop:1 rgba(5, 150, 105, 0.1));
                border-radius: 16px;
                border: 1px solid rgba(16, 185, 129, 0.2);
            }
            
            QLabel#main_title {
                font-size: 36px;
                font-weight: 700;
                color: #10b981;
                background: transparent;
                letter-spacing: -0.5px;
            }
            
            QLabel#main_subtitle {
                font-size: 14px;
                color: rgba(228, 228, 231, 0.6);
                background: transparent;
                font-weight: 400;
            }
            
            /* Platform Label */
            QLabel#mock_label {
                color: #10b981;
                font-weight: 600;
                background: rgba(16, 185, 129, 0.1);
                border: 1px solid rgba(16, 185, 129, 0.25);
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 13px;
            }
            
            /* Tab Widget */
            QTabWidget::pane {
                border: 1px solid rgba(39, 39, 42, 0.8);
                border-radius: 12px;
                background: #18181b;
            }
            
            QTabBar::tab {
                background: rgba(39, 39, 42, 0.5);
                color: rgba(228, 228, 231, 0.6);
                padding: 14px 28px;
                margin: 4px 2px;
                border-radius: 10px;
                font-weight: 500;
                font-size: 13px;
                border: 1px solid transparent;
            }
            
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #10b981, stop:1 #059669);
                color: #ffffff;
                font-weight: 600;
                border: 1px solid rgba(16, 185, 129, 0.3);
            }
            
            QTabBar::tab:hover:!selected {
                background: rgba(16, 185, 129, 0.15);
                color: #10b981;
                border: 1px solid rgba(16, 185, 129, 0.2);
            }
            
            /* Network List Container */
            QWidget#network_list_container {
                background: transparent;
            }
            
            /* Loading Widget */
            QWidget#loading_widget {
                background: transparent;
            }
            
            QLabel#loading_icon {
                font-size: 56px;
                color: #10b981;
            }
            
            QLabel#loading_text {
                color: #10b981;
                font-size: 16px;
                font-weight: 500;
            }
            
            /* Networks Container */
            QWidget#networks_container {
                background: transparent;
            }
            
            QLabel#no_networks_label {
                color: rgba(228, 228, 231, 0.6);
                font-size: 16px;
                padding: 40px;
                font-weight: 500;
            }
            
            QLabel#error_label {
                color: #ef4444;
                font-size: 14px;
                padding: 30px;
                font-weight: 500;
            }
            
            /* Refresh Button */
            QPushButton#refresh_button {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #10b981, stop:1 #059669);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 14px 28px;
                font-weight: 600;
                font-size: 14px;
                letter-spacing: 0.3px;
            }
            
            QPushButton#refresh_button:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #059669, stop:1 #047857);
            }
            
            QPushButton#refresh_button:pressed {
                background: #047857;
            }
            
            /* Network Items */
            QFrame#network_item {
                background: rgba(39, 39, 42, 0.4);
                border: 1px solid rgba(63, 63, 70, 0.6);
                border-radius: 12px;
            }
            
            QFrame#network_item[connected="true"] {
                background: rgba(16, 185, 129, 0.12);
                border: 1px solid rgba(16, 185, 129, 0.4);
            }
            
            QFrame#network_item:hover {
                background: rgba(16, 185, 129, 0.15);
                border: 1px solid rgba(16, 185, 129, 0.5);
            }
            
            QLabel#network_name {
                color: #f4f4f5;
                font-size: 16px;
                font-weight: 600;
                background: transparent;
            }
            
            QLabel#status_connected {
                color: #10b981;
                font-size: 12px;
                font-weight: 600;
                background: transparent;
            }
            
            QLabel#status_secured {
                color: #fbbf24;
                font-size: 12px;
                font-weight: 500;
                background: transparent;
            }
            
            QLabel#status_open {
                color: #10b981;
                font-size: 12px;
                font-weight: 500;
                background: transparent;
            }
            
            QLabel#strength_percent {
                color: #e4e4e7;
                font-size: 12px;
                font-weight: 600;
                background: transparent;
            }
            
            /* Connection Form */
            QWidget#connection_form {
                background: #18181b;
                border: 1px solid rgba(16, 185, 129, 0.3);
                border-radius: 12px;
            }
            
            QLabel#form_title {
                color: #f4f4f5;
                font-size: 18px;
                font-weight: 600;
                background: transparent;
            }
            
            QPushButton#close_button {
                background: rgba(239, 68, 68, 0.15);
                color: #ef4444;
                border: 1px solid rgba(239, 68, 68, 0.3);
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
            }
            
            QPushButton#close_button:hover {
                background: rgba(239, 68, 68, 0.25);
            }
            
            QLabel#network_info {
                color: #e4e4e7;
                font-size: 14px;
                background: rgba(39, 39, 42, 0.5);
                padding: 12px;
                border-radius: 8px;
            }
            
            QLineEdit#password_input {
                background: rgba(39, 39, 42, 0.6);
                border: 1px solid rgba(63, 63, 70, 0.8);
                border-radius: 8px;
                padding: 10px 15px;
                color: #f4f4f5;
                font-size: 14px;
                selection-background-color: rgba(16, 185, 129, 0.3);
            }
            
            QLineEdit#password_input:focus {
                border: 1px solid #10b981;
                background: rgba(39, 39, 42, 0.8);
            }
            
            QPushButton#toggle_password {
                background: rgba(39, 39, 42, 0.6);
                color: #a1a1aa;
                border: 1px solid rgba(63, 63, 70, 0.8);
                border-radius: 8px;
            }
            
            QPushButton#toggle_password:hover {
                background: rgba(39, 39, 42, 0.8);
                color: #e4e4e7;
            }
            
            QCheckBox#show_password_cb, QCheckBox#remember_cb {
                color: rgba(228, 228, 231, 0.8);
                background: transparent;
                spacing: 8px;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 2px solid rgba(113, 113, 122, 0.6);
                background: rgba(39, 39, 42, 0.6);
            }
            
            QCheckBox::indicator:hover {
                border: 2px solid rgba(16, 185, 129, 0.6);
            }
            
            QCheckBox::indicator:checked {
                background: #10b981;
                border: 2px solid #10b981;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEwIDNMNC41IDguNUwyIDYiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPg==);
            }
            
            QPushButton#cancel_button {
                background: rgba(39, 39, 42, 0.6);
                color: #e4e4e7;
                border: 1px solid rgba(63, 63, 70, 0.8);
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: 500;
            }
            
            QPushButton#cancel_button:hover {
                background: rgba(63, 63, 70, 0.8);
                border: 1px solid rgba(82, 82, 91, 0.8);
            }
            
            QPushButton#connect_button {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #10b981, stop:1 #059669);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: 600;
            }
            
            QPushButton#connect_button:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #059669, stop:1 #047857);
            }
            
            QPushButton#connect_button:pressed {
                background: #047857;
            }
            
            QPushButton#connect_button:disabled {
                background: rgba(39, 39, 42, 0.6);
                color: rgba(228, 228, 231, 0.4);
            }
            
            QLabel#status_label {
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 13px;
            }
            
            QLabel#status_label[status="info"] {
                color: #60a5fa;
                background: rgba(96, 165, 250, 0.1);
                border: 1px solid rgba(96, 165, 250, 0.3);
            }
            
            QLabel#status_label[status="loading"] {
                color: #fbbf24;
                background: rgba(251, 191, 36, 0.1);
                border: 1px solid rgba(251, 191, 36, 0.3);
            }
            
            /* Settings Tab */
            QWidget#sidebar {
                background: #18181b;
                border-right: 1px solid rgba(39, 39, 42, 0.8);
            }
            
            QWidget#sidebar_header {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(16, 185, 129, 0.15), stop:1 rgba(16, 185, 129, 0.05));
                border-bottom: 1px solid rgba(16, 185, 129, 0.2);
            }
            
            QLabel#app_title {
                font-size: 20px;
                font-weight: 700;
                color: #10b981;
                background: transparent;
            }
            
            QLabel#app_subtitle {
                font-size: 11px;
                color: rgba(228, 228, 231, 0.5);
                background: transparent;
            }
            
            QPushButton[checkable="true"] {
                background: transparent;
                color: rgba(228, 228, 231, 0.7);
                border: none;
                border-radius: 8px;
                text-align: left;
                padding-left: 16px;
                font-size: 14px;
                font-weight: 500;
            }
            
            QPushButton[checkable="true"]:hover {
                background: rgba(16, 185, 129, 0.1);
                color: #10b981;
            }
            
            QPushButton[checkable="true"]:checked {
                background: rgba(16, 185, 129, 0.15);
                color: #10b981;
                font-weight: 600;
                border-left: 3px solid #10b981;
                padding-left: 13px;
            }
            
            QWidget#content_area {
                background: #0a0e1a;
            }
            
            QWidget#content_header {
                background: #18181b;
                border-bottom: 1px solid rgba(39, 39, 42, 0.8);
            }
            
            QLabel#content_title {
                font-size: 24px;
                font-weight: 700;
                color: #f4f4f5;
                background: transparent;
            }
            
            QGroupBox#settings_group {
                background: rgba(24, 24, 27, 0.6);
                border: 1px solid rgba(39, 39, 42, 0.8);
                border-radius: 12px;
                margin-top: 16px;
                padding-top: 20px;
                font-weight: 600;
                color: #f4f4f5;
                font-size: 15px;
            }
            
            QGroupBox::title {
                color: #10b981;
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 10px;
                background: transparent;
                font-weight: 600;
            }
            
            QLabel#setting_label {
                color: #e4e4e7;
                font-size: 14px;
                font-weight: 500;
                background: transparent;
            }
            
            QComboBox {
                background: rgba(39, 39, 42, 0.6);
                border: 1px solid rgba(63, 63, 70, 0.8);
                border-radius: 8px;
                padding: 10px 14px;
                color: #e4e4e7;
                min-width: 150px;
                font-size: 14px;
            }
            
            QComboBox:hover {
                border: 1px solid rgba(16, 185, 129, 0.4);
                background: rgba(39, 39, 42, 0.8);
            }
            
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            
            QComboBox::down-arrow {
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEyIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDFMNiA2TDExIDEiIHN0cm9rZT0iIzEwYjk4MSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
                width: 12px;
                height: 8px;
            }
            
            QComboBox QAbstractItemView {
                background: #18181b;
                border: 1px solid rgba(39, 39, 42, 0.8);
                border-radius: 8px;
                color: #e4e4e7;
                selection-background-color: rgba(16, 185, 129, 0.2);
                selection-color: #10b981;
                padding: 4px;
                outline: none;
            }
            
            QComboBox QAbstractItemView::item {
                padding: 8px 12px;
                border-radius: 6px;
            }
            
            QComboBox QAbstractItemView::item:hover {
                background: rgba(16, 185, 129, 0.15);
            }
            
            QSlider::groove:horizontal {
                background: rgba(39, 39, 42, 0.6);
                height: 6px;
                border-radius: 3px;
            }
            
            QSlider::handle:horizontal {
                background: #10b981;
                width: 18px;
                height: 18px;
                margin: -6px 0;
                border-radius: 9px;
                border: 2px solid #059669;
            }
            
            QSlider::handle:horizontal:hover {
                background: #059669;
                border: 2px solid #047857;
            }
            
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #10b981, stop:1 #059669);
                border-radius: 3px;
            }
            
            QListWidget#saved_networks_list {
                background: rgba(39, 39, 42, 0.4);
                border: 1px solid rgba(63, 63, 70, 0.6);
                border-radius: 10px;
                color: #e4e4e7;
                outline: none;
                padding: 4px;
            }
            
            QListWidget::item {
                padding: 12px 16px;
                border-radius: 8px;
                margin: 2px 0;
            }
            
            QListWidget::item:selected {
                background: rgba(16, 185, 129, 0.2);
                color: #10b981;
                font-weight: 600;
            }
            
            QListWidget::item:hover {
                background: rgba(16, 185, 129, 0.1);
            }
            
            QPushButton#danger_button {
                background: rgba(239, 68, 68, 0.15);
                color: #ef4444;
                border: 1px solid rgba(239, 68, 68, 0.3);
                border-radius: 8px;
                padding: 10px 18px;
                font-weight: 500;
                font-size: 13px;
            }
            
            QPushButton#danger_button:hover {
                background: rgba(239, 68, 68, 0.25);
                border: 1px solid rgba(239, 68, 68, 0.4);
            }
            
            QPushButton#apply_button {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #10b981, stop:1 #059669);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 14px 32px;
                font-weight: 600;
                font-size: 14px;
                min-width: 160px;
                letter-spacing: 0.3px;
            }
            
            QPushButton#apply_button:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #059669, stop:1 #047857);
            }
            
            QPushButton#apply_button:pressed {
                background: #047857;
            }
            
            /* Scrollbars */
            QScrollBar:vertical {
                background: rgba(24, 24, 27, 0.5);
                width: 10px;
                border-radius: 5px;
                margin: 2px;
            }
            
            QScrollBar::handle:vertical {
                background: rgba(16, 185, 129, 0.5);
                border-radius: 5px;
                min-height: 30px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: rgba(16, 185, 129, 0.7);
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            QScrollBar:horizontal {
                background: rgba(24, 24, 27, 0.5);
                height: 10px;
                border-radius: 5px;
                margin: 2px;
            }
            
            QScrollBar::handle:horizontal {
                background: rgba(16, 185, 129, 0.5);
                border-radius: 5px;
                min-width: 30px;
            }
            
            QScrollBar::handle:horizontal:hover {
                background: rgba(16, 185, 129, 0.7);
            }
            
            /* Message Boxes */
            QMessageBox {
                background: #18181b;
                color: #e4e4e7;
            }
            
            QMessageBox QLabel {
                color: #e4e4e7;
                font-size: 14px;
            }
            
            QMessageBox QPushButton {
                background: rgba(16, 185, 129, 0.2);
                color: #10b981;
                border: 1px solid rgba(16, 185, 129, 0.4);
                border-radius: 8px;
                padding: 10px 20px;
                min-width: 90px;
                font-weight: 600;
            }
            
            QMessageBox QPushButton:hover {
                background: rgba(16, 185, 129, 0.3);
                border: 1px solid rgba(16, 185, 129, 0.5);
            }
            
            /* Tooltips */
            QToolTip {
                background: #18181b;
                color: #e4e4e7;
                border: 1px solid rgba(16, 185, 129, 0.3);
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 12px;
            }
        """
