class UnifiedStyles:
    @staticmethod
    def get_stylesheet(theme="dark"):
        if theme.lower() == "light":
            return UnifiedStyles._get_light_theme()
        else:
            return UnifiedStyles._get_dark_theme()

    @staticmethod
    def _get_dark_theme():
        return """
            /* =======================================================
               THEME: DEEP DARK EMERALD
               ======================================================= */

            QWidget {
                background: transparent;
                color: #f1f5f9; /* Slate 50 */
                font-family: 'Segoe UI', 'Inter', system-ui, sans-serif;
                font-size: 13px;
                border: none;
                outline: none;
            }

            /* --- WINDOW & CONTAINERS --- */
            QWidget#main_window {
                background-color: #0a0e1a; /* DEEP DARK BG (Prawie czarny) */
                border-radius: 16px;
                border: 1px solid rgba(16, 185, 129, 0.2);
            }

            QWidget#main_header {
                background-color: #0a0e1a;
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
                border-top-left-radius: 16px;
                border-top-right-radius: 16px;
            }

            QWidget#bottom_bar {
                background-color: #0a0e1a;
                border-top: 1px solid rgba(255, 255, 255, 0.05);
                border-bottom-left-radius: 16px;
                border-bottom-right-radius: 16px;
            }

            QStackedWidget {
                background-color: #0a0e1a;
            }

            /* --- TYPOGRAPHY --- */
            QLabel#header_title {
                font-size: 16px;
                font-weight: 800;
                color: #ffffff;
                letter-spacing: 0.5px;
            }

            /* --- NETWORK LIST ITEMS --- */
            QFrame#network_item_frame {
                background: transparent;
            }

            QFrame#inner_container {
                background-color: transparent; /* Minimalistyczny start */
                border-radius: 12px;
                border: none;
            }

            QFrame#inner_container:hover {
                background-color: rgba(255, 255, 255, 0.04); /* Subtelne podświetlenie */
            }

            QFrame#inner_container[connected="true"] {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(16, 185, 129, 0.15),
                    stop:1 rgba(16, 185, 129, 0.05));
                /* Bez ramki, sam gradient */
            }

            QLabel#network_name {
                color: #ffffff;
                font-weight: 600;
                font-size: 14px;
            }
            
            QLabel#network_status {
                color: #64748b; /* Slate 500 */
                font-size: 11px;
            }

            /* Minimalistyczna kłódka bez tła */
            QLabel#secured_indicator {
                background: transparent;
                color: #10b981;
                font-size: 10px;
                font-weight: bold;
                padding: 0px;
            }

            /* --- BUTTONS --- */
            QPushButton#header_back_btn {
                background: transparent;
                color: #10b981;
                font-size: 24px;
                font-weight: bold;
                border: none;
            }
            QPushButton#header_back_btn:hover {
                background: rgba(16, 185, 129, 0.1);
                border-radius: 8px;
            }

            QPushButton#settings_btn {
                background: transparent;
                font-size: 18px;
                color: #10b981;
            }
            QPushButton#settings_btn:hover {
                color: #34d399;
            }

            /* Action Buttons (Connect) */
            .btn-primary {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #10b981, stop:1 #059669);
                color: white;
                font-weight: 700;
                font-size: 13px;
                border-radius: 8px;
                border: none;
                padding: 6px 12px;
            }
            .btn-primary:hover {
                background: #10b981;
            }
            .btn-primary:pressed {
                background: #047857;
            }
            .btn-primary:disabled {
                background: rgba(255, 255, 255, 0.05);
                color: rgba(255, 255, 255, 0.3);
            }

            /* --- INPUTS & CONTROLS --- */
            QLineEdit {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 8px 12px;
                color: white;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #10b981;
                background: rgba(255, 255, 255, 0.08);
            }

            QCheckBox {
                spacing: 8px;
                color: #cbd5e1;
                font-size: 12px;
                font-weight: 500;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 4px;
            }
            QCheckBox::indicator:checked {
                background-color: #10b981;
                border: 1px solid #10b981;
            }

            QComboBox {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 6px;
                padding: 4px 8px;
                color: white;
                min-width: 60px;
            }
            QComboBox:hover {
                border: 1px solid #10b981;
            }
            QComboBox::drop-down {
                border: none;
                background: transparent;
            }
            QComboBox QAbstractItemView {
                background: #0a0e1a;
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.1);
                selection-background-color: #10b981;
            }

            QGroupBox {
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                margin-top: 8px;
                padding-top: 12px;
                font-weight: bold;
                color: #10b981;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                left: 10px;
            }

            /* --- SCROLLBAR --- */
            QScrollArea { background: transparent; }
            QScrollBar:vertical {
                background: transparent;
                width: 6px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.1);
                min-height: 20px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(255, 255, 255, 0.2);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
                height: 0px;
            }
            
            /* --- CONNECTION FORM SPECIFIC --- */
            QLabel#connection_icon_large {
                background: rgba(16, 185, 129, 0.1);
                color: #10b981;
                border-radius: 32px;
                font-size: 32px;
                border: 1px solid rgba(16, 185, 129, 0.3);
            }
            QLabel#connection_ssid_large {
                font-size: 18px;
                font-weight: 700;
                color: white;
                margin-top: 10px;
            }
        """

    @staticmethod
    def _get_light_theme():
        return """
            /* =======================================================
               THEME: CLEAN LIGHT
               ======================================================= */

            QWidget {
                background: transparent;
                color: #1e293b; /* Slate 800 */
                font-family: 'Segoe UI', 'Inter', system-ui, sans-serif;
                font-size: 13px;
                border: none;
                outline: none;
            }

            /* --- WINDOW & CONTAINERS --- */
            QWidget#main_window {
                background-color: #ffffff; /* White */
                border-radius: 16px;
                border: 1px solid #cbd5e1; /* Slate 300 */
            }

            QWidget#main_header {
                background-color: #f8fafc; /* Slate 50 */
                border-bottom: 1px solid #e2e8f0;
                border-top-left-radius: 16px;
                border-top-right-radius: 16px;
            }

            QWidget#bottom_bar {
                background-color: #f8fafc;
                border-top: 1px solid #e2e8f0;
                border-bottom-left-radius: 16px;
                border-bottom-right-radius: 16px;
            }

            QStackedWidget {
                background-color: #ffffff;
            }

            /* --- TYPOGRAPHY --- */
            QLabel#header_title {
                font-size: 16px;
                font-weight: 800;
                color: #059669; /* Emerald 600 (Darker for light bg) */
                letter-spacing: 0.5px;
            }

            /* --- NETWORK LIST ITEMS --- */
            QFrame#network_item_frame {
                background: transparent;
            }

            QFrame#inner_container {
                background-color: transparent;
                border-radius: 12px;
                border: 1px solid transparent;
            }

            QFrame#inner_container:hover {
                background-color: #f1f5f9; /* Slate 100 */
            }

            QFrame#inner_container[connected="true"] {
                background-color: #ecfdf5; /* Emerald 50 */
                border: 1px solid #a7f3d0;
            }

            QLabel#network_name {
                color: #0f172a; /* Slate 900 */
                font-weight: 600;
                font-size: 14px;
            }
            
            QLabel#network_status {
                color: #64748b; /* Slate 500 */
                font-size: 11px;
            }

            QLabel#secured_indicator {
                background: transparent;
                color: #059669; /* Emerald 600 */
                font-size: 10px;
                font-weight: bold;
                padding: 0px;
            }

            /* --- BUTTONS --- */
            QPushButton#header_back_btn {
                background: transparent;
                color: #059669;
                font-size: 24px;
                font-weight: bold;
                border: none;
            }
            QPushButton#header_back_btn:hover {
                background: #e2e8f0;
                border-radius: 8px;
            }

            QPushButton#settings_btn {
                background: transparent;
                font-size: 18px;
                color: #059669;
            }
            QPushButton#settings_btn:hover {
                background: #e2e8f0;
                border-radius: 6px;
            }

            /* Action Buttons */
            .btn-primary {
                background: #059669;
                color: white;
                font-weight: 700;
                font-size: 13px;
                border-radius: 8px;
                border: none;
                padding: 6px 12px;
            }
            .btn-primary:hover {
                background: #047857;
            }
            .btn-primary:pressed {
                background: #065f46;
                padding-top: 7px;
            }
            .btn-primary:disabled {
                background: #cbd5e1;
                color: #94a3b8;
            }

            /* --- INPUTS & CONTROLS --- */
            QLineEdit {
                background: #ffffff;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                padding: 8px 12px;
                color: #0f172a;
                font-size: 13px;
                selection-background-color: #34d399;
            }
            QLineEdit:focus {
                border: 1px solid #059669;
                background: #f8fafc;
            }

            QCheckBox {
                spacing: 8px;
                color: #334155;
                font-size: 12px;
                font-weight: 500;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                background: #f1f5f9;
                border: 1px solid #94a3b8;
                border-radius: 4px;
            }
            QCheckBox::indicator:checked {
                background-color: #059669;
                border: 1px solid #059669;
            }

            QComboBox {
                background: #ffffff;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                padding: 4px 8px;
                color: #0f172a;
                min-width: 60px;
            }
            QComboBox:hover {
                border: 1px solid #059669;
            }
            QComboBox::drop-down {
                border: none;
                background: transparent;
            }
            QComboBox QAbstractItemView {
                background: #ffffff;
                color: #0f172a;
                border: 1px solid #cbd5e1;
                selection-background-color: #d1fae5;
                selection-color: #064e3b;
            }

            QGroupBox {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                margin-top: 8px;
                padding-top: 12px;
                font-weight: bold;
                color: #059669;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                left: 10px;
                background: transparent;
            }

            /* --- SCROLLBAR --- */
            QScrollArea { background: transparent; }
            QScrollBar:vertical {
                background: #f1f5f9;
                width: 6px;
                border-radius: 3px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #cbd5e1;
                min-height: 20px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical:hover {
                background: #94a3b8;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
                height: 0px;
            }
            
            /* --- CONNECTION FORM SPECIFIC --- */
            QLabel#connection_icon_large {
                background: #ecfdf5;
                color: #059669;
                border-radius: 32px;
                font-size: 32px;
                border: 1px solid #a7f3d0;
            }
            QLabel#connection_ssid_large {
                font-size: 18px;
                font-weight: 700;
                color: #0f172a;
            }
        """