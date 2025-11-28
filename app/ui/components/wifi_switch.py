from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, pyqtProperty

class ModernWiFiSwitch(QWidget):
    
    toggled = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(32, 16)  # Rozmiar kompaktowy
        self.setCursor(Qt.PointingHandCursor)
        
        # Stan początkowy
        self._is_on = True
        self._slider_pos = 22.0  # Pozycja dla "Włączony" (22px)
        self.animation = None

    # --- Wymagane metody API (naprawiają błąd AttributeError) ---

    def setChecked(self, checked):
        """Metoda wymagana przez run.py do ustawienia stanu przy starcie"""
        self._is_on = checked
        # Ustawiamy pozycję natychmiastowo bez animacji przy inicjalizacji
        self._slider_pos = 22.0 if checked else 10.0
        self.update()

    def isChecked(self):
        """Zwraca aktualny stan logiczny"""
        return self._is_on

    # --- Property dla animacji ---

    @pyqtProperty(float)
    def slider_pos(self):
        return self._slider_pos
    
    @slider_pos.setter
    def slider_pos(self, value):
        self._slider_pos = value
        self.update()
    
    # --- Rysowanie i obsługa ---

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Kolory
        # Zielony (#10b981) jeśli ON, Szary (#4b5563) jeśli OFF
        track_color = QColor("#10b981") if self._is_on else QColor("#4b5563")
        
        # Rysowanie obramowania/tła
        painter.setPen(QPen(track_color, 1.5))
        painter.setBrush(Qt.NoBrush) # Przeźroczyste tło, tylko ramka (zgodnie z Twoim stylem)
        painter.drawRoundedRect(1, 1, 30, 14, 7, 7)
        
        # Rysowanie kropki (suwaka)
        circle_color = track_color # Kropka w tym samym kolorze co ramka
        painter.setBrush(QBrush(circle_color))
        painter.setPen(Qt.NoPen)
        # slider_pos to środek kropki
        painter.drawEllipse(int(self._slider_pos) - 4, 4, 8, 8)
        
        # Efekt poświaty (Glow) gdy włączony
        if self._is_on:
            glow_color = QColor("#10b981")
            glow_color.setAlpha(40)
            painter.setBrush(QBrush(glow_color))
            painter.drawEllipse(int(self._slider_pos) - 6, 2, 12, 12)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.toggle()
        super().mouseReleaseEvent(event)
    
    def toggle(self):
        self._is_on = not self._is_on
        self.animate()
        self.toggled.emit(self._is_on)
    
    def animate(self):
        if self.animation:
            self.animation.stop()
        
        self.animation = QPropertyAnimation(self, b"slider_pos")
        self.animation.setDuration(250)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Startujemy z AKTUALNEJ pozycji (płynniej przy szybkim klikaniu)
        self.animation.setStartValue(self._slider_pos)
        
        # Pozycja docelowa: 22 (prawo/ON) lub 10 (lewo/OFF)
        end_pos = 22.0 if self._is_on else 10.0
        self.animation.setEndValue(end_pos)
        
        self.animation.start()