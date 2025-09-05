from collections.abc import Callable

from PySide6.QtWidgets import QTabBar


class SecureTabBar(QTabBar):
    def __init__(self, parent, check_auth: Callable[[int], bool]):
        super().__init__(parent)
        self.check_auth = check_auth

    def mousePressEvent(self, event):
        index = self.tabAt(event.pos())
        if self.check_auth(index):
            super().mousePressEvent(event)
