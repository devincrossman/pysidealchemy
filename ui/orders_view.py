from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from models_qt.orders_model import OrdersTableModel
from ui.add_order_dialog import AddOrderDialog


class OrdersView(QWidget):
    """Orders tab with table and buttons."""

    def __init__(self, session):
        super().__init__()
        layout = QVBoxLayout(self)

        self.session = session
        self.model = OrdersTableModel(self.session)

        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableView.SelectionMode.ExtendedSelection)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Order")
        self.del_btn = QPushButton("Delete Selected")
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.del_btn)
        layout.addLayout(btn_layout)

        self.add_btn.clicked.connect(self.add_order)
        self.del_btn.clicked.connect(self.delete_selected)

    def add_order(self):
        dlg = AddOrderDialog(self.session)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            user_id, product_id, qty = dlg.get_values()
            self.model.addOrder(product_id=product_id, user_id=user_id, quantity=qty)

    def delete_selected(self):
        selection = self.table.selectionModel().selectedRows()
        if not selection:
            QMessageBox.information(self, "No Selection", "No rows selected.")
            return
        rows = [index.row() for index in selection]
        self.model.deleteOrders(rows)
