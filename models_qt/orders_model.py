from PySide6.QtCore import QAbstractTableModel, Qt

from db.models.orders import Order


class OrdersTableModel(QAbstractTableModel):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.orders = self.session.query(Order).all()
        self.headers = ["ID", "Product ID", "User ID", "Quantity", "Status"]

    def rowCount(self, parent=None):
        return len(self.orders)

    def columnCount(self, parent=None):
        return 5

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        order = self.orders[index.row()]
        col = index.column()
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            if col == 0:
                return order.id
            elif col == 1:
                return order.product_id
            elif col == 2:
                return order.user_id
            elif col == 3:
                return order.quantity
            elif col == 4:
                return order.status
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
        order = self.orders[index.row()]
        col = index.column()
        if col == 1:
            order.product_id = int(value)
        elif col == 2:
            order.user_id = int(value)
        elif col == 3:
            order.quantity = int(value)
        elif col == 4:
            order.status = str(value)
        self.session.commit()
        self.dataChanged.emit(index, index)
        return True

    def addOrder(self, product_id=0, user_id=0, quantity=1, status="Pending"):
        new_order = Order(
            product_id=product_id, user_id=user_id, quantity=quantity, status=status
        )
        self.session.add(new_order)
        self.session.commit()
        self.layoutAboutToBeChanged.emit()
        self.orders = self.session.query(Order).all()
        self.layoutChanged.emit()

    def deleteOrders(self, rows):
        for row in sorted(rows, reverse=True):
            order = self.orders[row]
            self.session.delete(order)
        self.session.commit()
        self.layoutAboutToBeChanged.emit()
        self.orders = self.session.query(Order).all()
        self.layoutChanged.emit()

    def removeOrdersWithProducts(self, deleted_product_ids):
        """Remove orders referencing deleted products (for cross-tab refresh)"""
        to_delete = [o for o in self.orders if o.product_id in deleted_product_ids]
        for order in to_delete:
            self.session.delete(order)
        self.session.commit()
        self.layoutAboutToBeChanged.emit()
        self.orders = self.session.query(Order).all()
        self.layoutChanged.emit()
