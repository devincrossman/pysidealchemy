from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QSpinBox,
)

from db.models.products import Product
from db.models.users import User


class AddOrderDialog(QDialog):
    def __init__(self, session):
        super().__init__()
        self.setWindowTitle("Add Order")
        layout = QFormLayout(self)

        # Populate user and product combo boxes from the database
        self.user_cb = QComboBox()
        self.users = session.query(User).all()  # store objects
        for u in self.users:
            self.user_cb.addItem(u.username, u.id)  # display name, store id as data

        self.product_cb = QComboBox()
        self.products = session.query(Product).all()
        for p in self.products:
            self.product_cb.addItem(p.name, p.id)  # display name, store id

        self.qty_spin = QSpinBox()
        self.qty_spin.setRange(1, 1000)

        layout.addRow("User", self.user_cb)
        layout.addRow("Product", self.product_cb)
        layout.addRow("Quantity", self.qty_spin)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_values(self):
        user_id = self.user_cb.currentData()
        product_id = self.product_cb.currentData()
        quantity = self.qty_spin.value()
        return user_id, product_id, quantity
