from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QHeaderView,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from models_qt.users_model import UsersTableModel
from services.user_service import UserService
from ui.add_user_dialog import AddUserDialog


class UsersView(QWidget):
    """Users tab with table and buttons."""

    def __init__(self, session):
        super().__init__()
        layout = QVBoxLayout(self)

        self.session = session
        self.user_service = UserService(session)
        self.model = UsersTableModel(self.user_service)

        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Username
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Email
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Role
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableView.SelectionMode.ExtendedSelection)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add User")
        self.del_btn = QPushButton("Delete Selected")
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.del_btn)
        layout.addLayout(btn_layout)

        self.add_btn.clicked.connect(self.add_user)
        self.del_btn.clicked.connect(self.delete_selected)

    def add_user(self):
        dlg = AddUserDialog(self.session)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            username, password, email, role = dlg.get_values()
            self.model.addUser(
                username=username, password=password, email=email, role=role
            )

    def delete_selected(self):
        selection = self.table.selectionModel().selectedRows()
        if not selection:
            QMessageBox.information(self, "No Selection", "No rows selected.")
            return
        rows = [index.row() for index in selection]
        self.model.deleteUsers(rows)
