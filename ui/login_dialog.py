# ui/login_dialog.py
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLineEdit


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        layout = QFormLayout(self)

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addRow("Username:", self.username)
        layout.addRow("Password:", self.password)

        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        self.button_box = QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def get_credentials(self):
        return self.username.text(), self.password.text()
