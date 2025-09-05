from PySide6.QtWidgets import (
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from models_qt.products_model import ProductTableModel


class ProductsView(QWidget):
    """Products tab with table and buttons."""
    def __init__(self, session):
        super().__init__()
        layout = QVBoxLayout(self)

        self.session = session
        self.model = ProductTableModel(self.session)

        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableView.SelectionMode.ExtendedSelection)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Product")
        self.del_btn = QPushButton("Delete Selected")
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.del_btn)
        layout.addLayout(btn_layout)

        self.add_btn.clicked.connect(self.add_product)
        self.del_btn.clicked.connect(self.delete_selected)

    def add_product(self):
        self.model.addProduct()

    def delete_selected(self):
        selection = self.table.selectionModel().selectedRows()
        if not selection:
            QMessageBox.information(self, "No Selection", "No rows selected.")
            return
        rows = [index.row() for index in selection]
        self.model.deleteProducts(rows)
