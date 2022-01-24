import sys

from PyQt6.QtWidgets import QApplication, QWidget, QInputDialog


class App(QWidget):

    def __init__(self, current, mn, mx):
        super().__init__()
        self.current = current
        self.mn = mn
        self.mx = mx

    def getInteger(self):
        i, okPressed = QInputDialog.getInt(self, "Select game level", "Level:", self.current, self.mn, self.mx)
        return i if okPressed else False


def get_level(app, current=1, mn=1, mx=2):
    """Get level from user"""
    return App(current, mn, mx).getInteger()
