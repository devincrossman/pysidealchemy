from PySide6.QtCore import QAbstractTableModel, Qt

from db.models.users import User
from services.user_service import UserService


class UsersTableModel(QAbstractTableModel):
    def __init__(self, user_service: UserService):
        super().__init__()
        self.user_service = user_service
        self.users: list[User] = self.user_service.get_all_users()
        self.headers = ["ID", "Username", "Email", "Role"]

    def rowCount(self, parent=None):
        return len(self.users)

    def columnCount(self, parent=None):
        return 4

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        row: int = index.row()
        user = self.users[row]
        col = index.column()
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            if col == 0:
                return user.id
            elif col == 1:
                return user.username
            elif col == 2:
                return user.email
            elif col == 3:
                return user.role
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if (
            orientation == Qt.Orientation.Horizontal
            and role == Qt.ItemDataRole.DisplayRole
        ):
            return self.headers[section]
        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemFlag.ItemIsEnabled
        if index.column() == 0:
            return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        return (
            Qt.ItemFlag.ItemIsSelectable
            | Qt.ItemFlag.ItemIsEnabled
            | Qt.ItemFlag.ItemIsEditable
        )

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if not index.isValid() or role != Qt.ItemDataRole.EditRole:
            return False
        row: int = index.row()
        user = self.users[row]
        col = index.column()

        kwargs = {}
        if col == 1:
            kwargs["username"] = str(value)
        elif col == 2:
            kwargs["email"] = str(value)
        elif col == 3:
            kwargs["role"] = str(value)
        else:
            return False

        self.user_service.update_user(user.id, **kwargs)
        self.users = self.user_service.get_all_users()
        self.dataChanged.emit(index, index)
        return True

    def addUser(self, username: str, password: str, email: str, role: str = "user"):
        self.layoutAboutToBeChanged.emit()
        self.user_service.add_user(username, password, email, role)
        self.users = self.user_service.get_all_users()
        self.layoutChanged.emit()

    def deleteUsers(self, rows: list[int]):
        self.layoutAboutToBeChanged.emit()
        ids = [self.users[row].id for row in rows]
        self.user_service.delete_users(ids)
        self.users = self.user_service.get_all_users()
        self.layoutChanged.emit()
