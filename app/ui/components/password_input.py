from PyQt5.QtWidgets import (
    QWidget, QLineEdit, QLabel, QHBoxLayout, QPushButton, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class ModernPasswordInput(QWidget):
    def __init__(self, placeholder="Enter password", parent=None):
        super().__init__(parent)
        self.setFixedHeight(40)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(6)

        # Ikonka
        self.icon = QLabel()
        self.icon.setPixmap(QIcon.fromTheme("object-locked").pixmap(20, 20))
        layout.addWidget(self.icon)

        # Pole hasła
        self.input = QLineEdit()
        self.input.setPlaceholderText(placeholder)
        self.input.setEchoMode(QLineEdit.Password)
        self.input.setStyleSheet("""
            QLineEdit {
                background: #ffffff;
                border: 1px solid #c0c0c0;
                border-radius: 6px;
                padding: 6px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #4A90E2;
            }
        """)
        layout.addWidget(self.input)

        # Przycisk pokaz/ukryj hasło
        self.toggle_btn = QPushButton("👁")
        self.toggle_btn.setFixedWidth(30)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                font-size: 16px;
            }
            QPushButton:hover {
                color: #4A90E2;
            }
        """)
        self.toggle_btn.clicked.connect(self.toggle_password)
        layout.addWidget(self.toggle_btn)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(12)
        shadow.setOffset(0, 2)
        shadow.setColor(Qt.black)
        self.setGraphicsEffect(shadow)

    def toggle_password(self):
        if self.input.echoMode() == QLineEdit.Password:
            self.input.setEchoMode(QLineEdit.Normal)
            self.toggle_btn.setText("🙈")
        else:
            self.input.setEchoMode(QLineEdit.Password)
            self.toggle_btn.setText("👁")

    def text(self):
        return self.input.text()
