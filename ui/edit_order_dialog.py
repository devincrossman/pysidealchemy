from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHeaderView,
    QInputDialog,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from db.models.products import Product
from db.models.users import User


class EditOrderDialog(QDialog):
    def __init__(self, session, order):
        super().__init__()
        self.session = session
        self.order = order
        self.setWindowTitle("Edit Order")
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        self.user_cb = QComboBox()
        self.users = self.session.query(User).all()
        for u in self.users:
            self.user_cb.addItem(u.username, u.id)
        current_user_index = self.user_cb.findData(self.order.user_id)
        if current_user_index != -1:
            self.user_cb.setCurrentIndex(current_user_index)
        form_layout.addRow("User", self.user_cb)
        layout.addLayout(form_layout)

        self.products_table = QTableWidget()
        self.products_table.setColumnCount(2)
        self.products_table.setHorizontalHeaderLabels(["Product", "Quantity"])
        self.products_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        layout.addWidget(self.products_table)

        self.populate_products_table()

        product_btn_layout = QVBoxLayout()
        self.add_product_btn = QPushButton("Add Product")
        self.remove_product_btn = QPushButton("Remove Selected Product")
        product_btn_layout.addWidget(self.add_product_btn)
        product_btn_layout.addWidget(self.remove_product_btn)
        layout.addLayout(product_btn_layout)

        self.add_product_btn.clicked.connect(self.add_product)
        self.remove_product_btn.clicked.connect(self.remove_product)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def populate_products_table(self):
        for op in self.order.products:
            row_position = self.products_table.rowCount()
            self.products_table.insertRow(row_position)

            product_item = QTableWidgetItem(op.product.name)
            product_item.setData(Qt.ItemDataRole.UserRole, op.product.id)
            self.products_table.setItem(row_position, 0, product_item)

            quantity_spin = QSpinBox()
            quantity_spin.setRange(
                1, op.product.stock + op.quantity
            )  # Allow for current quantity
            quantity_spin.setValue(op.quantity)
            self.products_table.setCellWidget(row_position, 1, quantity_spin)

    def add_product(self):
        products = self.session.query(Product).all()
        product_names = [p.name for p in products]
        product_name, ok = QInputDialog.getItem(
            self, "Select Product", "Product:", product_names, 0, False
        )

        if ok and product_name:
            for row in range(self.products_table.rowCount()):
                if self.products_table.item(row, 0).text() == product_name:
                    return

            product = next((p for p in products if p.name == product_name), None)
            if product:
                row_position = self.products_table.rowCount()
                self.products_table.insertRow(row_position)

                product_item = QTableWidgetItem(product.name)
                product_item.setData(Qt.ItemDataRole.UserRole, product.id)
                self.products_table.setItem(row_position, 0, product_item)

                quantity_spin = QSpinBox()
                quantity_spin.setRange(1, product.stock)
                self.products_table.setCellWidget(row_position, 1, quantity_spin)

    def remove_product(self):
        selected_row = self.products_table.currentRow()
        if selected_row >= 0:
            self.products_table.removeRow(selected_row)

    def accept(self):
        if self.products_table.rowCount() == 0:
            QMessageBox.warning(
                self, "No Products", "An order must have at least one product."
            )
            return
        super().accept()

    def get_values(self):
        user_id = self.user_cb.currentData()
        products = []
        for row in range(self.products_table.rowCount()):
            product_id = self.products_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
            quantity = self.products_table.cellWidget(row, 1).value()
            products.append({"product_id": product_id, "quantity": quantity})
        return user_id, products
