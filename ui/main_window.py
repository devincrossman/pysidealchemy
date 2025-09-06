from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from db.base import SessionLocal
from db.create_db import create_db
from services.auth_service import init_auth_service
from ui.login_dialog import LoginDialog
from ui.orders_view import OrdersView
from ui.products_view import ProductsView
from ui.secure_tab_bar import SecureTabBar
from ui.users_view import UsersView


class MainWindow(QMainWindow):
    """Main window with tabs for Products, Orders, and Users."""

    def __init__(self):
        super().__init__()
        create_db()
        self.setWindowTitle("PySide Alechemy")
        self.resize(800, 600)

        self.session = SessionLocal()
        self.auth = init_auth_service(self.session)

        # Central widget with tabs
        central = QWidget()
        layout = QVBoxLayout(central)
        self.tabs = QTabWidget()
        self.tabs.setTabBar(SecureTabBar(self.tabs, self.check_auth))
        layout.addWidget(self.tabs)
        self.setCentralWidget(central)

        self.tabs.addTab(ProductsView(self.session), "Products")
        self.tabs.addTab(OrdersView(self.session), "Orders")
        self.tabs.addTab(UsersView(self.session), "Users")

        # --- Menu Bar ---
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        # About action
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        file_menu.addAction(about_action)

        # Logout action
        self.logout_action = QAction("Logout", self)
        self.logout_action.triggered.connect(self.logout)
        self.logout_action.setVisible(False)
        file_menu.addAction(self.logout_action)

        # Quit action
        quit_action = QAction("Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

    def show_about(self):
        QMessageBox.information(
            self,
            "About PySideAlchemy",
            "PySideAlchemy App\nVersion 1.0\nPowered by Awesomeness",
        )

    def update_logout_action(self):
        if self.auth.is_authenticated():
            self.logout_action.setVisible(True)
        else:
            self.logout_action.setVisible(False)

    def logout(self):
        self.tabs.setCurrentIndex(0)
        self.auth.logout()
        self.update_logout_action()
        QMessageBox.information(self, "Logged Out", "You have been logged out.")

    def on_login_success(self):
        self.update_logout_action()

    def on_tab_changed(self, index):
        tab_text = self.tabs.tabText(index)

        # Orders: any logged-in user
        if tab_text == "Orders" and not self.auth.is_authenticated():
            if not self.prompt_login():
                # prevent tab switch
                self.tabs.setCurrentIndex(self.previous_tab_index)
                return
        # Users: admin only
        elif tab_text == "Users" and not self.auth.is_authorized("admin"):
            if not self.prompt_login(required_role="admin"):
                self.tabs.setCurrentIndex(self.previous_tab_index)
                return

        # update previous index if login succeeds
        self.previous_tab_index = index

    def check_auth(self, index):
        tab_text = self.tabs.tabText(index)
        if tab_text == "Orders" and not self.auth.is_authenticated():
            return self.prompt_login()
        elif tab_text == "Users" and not self.auth.is_authorized("admin"):
            return self.prompt_login(required_role="admin")
        return True

    def prompt_login(self, required_role=None):
        dlg = LoginDialog()
        if dlg.exec():
            username, password = dlg.get_credentials()
            if not self.auth.authenticate_user(username, password):
                QMessageBox.warning(self, "Login Failed", "Invalid credentials")
                return False
            if required_role and not self.auth.is_authorized(required_role):
                QMessageBox.warning(
                    self,
                    "Access Denied",
                    f"{required_role.capitalize()} credentials required",
                )
                return False
            self.on_login_success()
            return True
        return False
