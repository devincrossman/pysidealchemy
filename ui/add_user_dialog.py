from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
)

from services.auth_service import AuthService


class AddUserDialog(QDialog):
    def __init__(self, session):
        super().__init__()
        self.setWindowTitle("Add User")
        layout = QFormLayout(self)

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.email = QLineEdit()

        self.role = QComboBox()
        self.roles = AuthService.roles
        for r in self.roles.keys():
            self.role.addItem(r)

        layout.addRow("Username", self.username)
        layout.addRow("Password", self.password)
        layout.addRow("Email", self.email)
        layout.addRow("Role", self.role)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_values(self):
        user = self.username.text()
        password = self.password.text()
        email = self.email.text()
        role = self.role.currentData()
        return user, password, email, role
