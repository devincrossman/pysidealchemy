from PySide6.QtCore import QAbstractTableModel, Qt

from db.models.order_products import OrderProduct
from db.models.orders import Order


class OrdersTableModel(QAbstractTableModel):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.orders = self.session.query(Order).all()
        self.headers = ["ID", "User", "Products", "Status", "Total"]

    def rowCount(self, parent=None):
        return len(self.orders)

    def columnCount(self, parent=None):
        return 5

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        order = self.orders[index.row()]
        col = index.column()
        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0:
                return order.id
            elif col == 1:
                return order.user.username
            elif col == 2:
                return ", ".join(
                    [f"{op.product.name} (x{op.quantity})" for op in order.products]
                )
            elif col == 3:
                return order.status
            elif col == 4:  # Total
                return f"{order.total:.2f}"
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
        # Make all columns non-editable for now, except status
        if index.column() == 3:
            return (
                Qt.ItemFlag.ItemIsSelectable
                | Qt.ItemFlag.ItemIsEnabled
                | Qt.ItemFlag.ItemIsEditable
            )
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if not index.isValid() or role != Qt.ItemDataRole.EditRole:
            return False
        order = self.orders[index.row()]
        col = index.column()
        if col == 3:
            order.status = str(value)
        else:
            return False
        self.session.commit()
        self.dataChanged.emit(index, index)
        return True

    def addOrder(self, user_id, products, status="Pending"):
        new_order = Order(user_id=user_id, status=status)
        for p_info in products:
            order_product = OrderProduct(
                order=new_order,
                product_id=p_info["product_id"],
                quantity=p_info["quantity"],
            )
            self.session.add(order_product)
        self.session.add(new_order)
        self.session.commit()
        self.layoutAboutToBeChanged.emit()
        self.orders = self.session.query(Order).all()
        self.layoutChanged.emit()

    def updateOrder(self, order, user_id, products):
        order.user_id = user_id

        # Remove old products
        for op in order.products:
            self.session.delete(op)

        # Add new products
        for p_info in products:
            order_product = OrderProduct(
                order=order,
                product_id=p_info["product_id"],
                quantity=p_info["quantity"],
            )
            self.session.add(order_product)

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
        # This needs to be updated to check the new relationship
        orders_to_delete = []
        for order in self.orders:
            for op in order.products:
                if op.product_id in deleted_product_ids:
                    orders_to_delete.append(order)
                    break

        for order in orders_to_delete:
            self.session.delete(order)

        self.session.commit()
        self.layoutAboutToBeChanged.emit()
        self.orders = self.session.query(Order).all()
        self.layoutChanged.emit()
