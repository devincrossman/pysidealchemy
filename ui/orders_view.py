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

from models_qt.orders_model import OrdersTableModel
from ui.add_order_dialog import AddOrderDialog
from ui.edit_order_dialog import EditOrderDialog


class OrdersView(QWidget):
    """Orders tab with table and buttons."""

    def __init__(self, session):
        super().__init__()
        layout = QVBoxLayout(self)

        self.session = session
        self.model = OrdersTableModel(self.session)

        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # User
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Products
        header.setSectionResizeMode(
            3, QHeaderView.ResizeMode.ResizeToContents
        )  # Status
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Total
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableView.SelectionMode.ExtendedSelection)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Order")
        self.edit_btn = QPushButton("Edit Selected")
        self.del_btn = QPushButton("Delete Selected")
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.del_btn)
        layout.addLayout(btn_layout)

        self.add_btn.clicked.connect(self.add_order)
        self.edit_btn.clicked.connect(self.edit_order)
        self.del_btn.clicked.connect(self.delete_selected)

    def add_order(self):
        dlg = AddOrderDialog(self.session)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            user_id, products = dlg.get_values()
            self.model.addOrder(user_id=user_id, products=products)

    def edit_order(self):
        selection = self.table.selectionModel().selectedRows()
        if not selection:
            QMessageBox.information(
                self, "No Selection", "Please select an order to edit."
            )
            return
        if len(selection) > 1:
            QMessageBox.information(
                self, "Multiple Selection", "Please select only one order to edit."
            )
            return

        row = selection[0].row()
        order = self.model.orders[row]

        dlg = EditOrderDialog(self.session, order)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            user_id, products = dlg.get_values()
            self.model.updateOrder(order, user_id, products)

    def delete_selected(self):
        selection = self.table.selectionModel().selectedRows()
        if not selection:
            QMessageBox.information(self, "No Selection", "No rows selected.")
            return
        rows = [index.row() for index in selection]
        self.model.deleteOrders(rows)
