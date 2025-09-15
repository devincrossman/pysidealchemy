import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QMessageBox,
    QPushButton,
    QStyledItemDelegate,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from models_qt.products_model import ProductTableModel
from ui.add_product_dialog import AddProductDialog
from utils.config import resource_path


class ImageDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        if index.column() == 4:  # Image Path column
            path = index.data()
            pixmap = QPixmap()
            if path and os.path.exists(resource_path(path)):
                pixmap.load(resource_path(path))
            else:
                pixmap.load(resource_path("assets/images/placeholder.png"))

            # Scale to the cell size while keeping aspect ratio
            scaled_pixmap = pixmap.scaled(
                option.rect.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            # Center the image in the cell
            x = option.rect.x() + (option.rect.width() - scaled_pixmap.width()) / 2
            y = option.rect.y() + (option.rect.height() - scaled_pixmap.height()) / 2
            painter.drawPixmap(int(x), int(y), scaled_pixmap)
        else:
            super().paint(painter, option, index)

    def createEditor(self, parent, option, index):
        if index.column() == 4:
            file_path, _ = QFileDialog.getOpenFileName(
                parent,
                "Select Image",
                "",
                "Image Files (*.png *.jpg *.jpeg *.bmp)",
            )
            if file_path:
                relative_path = os.path.relpath(file_path, resource_path(""))
                index.model().setData(index, relative_path, Qt.ItemDataRole.EditRole)
            return None  # no editor widget needed
        return super().createEditor(parent, option, index)


class ProductsView(QWidget):
    """Products tab with table and buttons."""

    def __init__(self, session):
        super().__init__()
        layout = QVBoxLayout(self)

        self.session = session
        self.model = ProductTableModel(self.session)

        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setAlternatingRowColors(True)
        self.table.setItemDelegateForColumn(4, ImageDelegate(self.table))

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.verticalHeader().setDefaultSectionSize(100)  # set row height
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
        dlg = AddProductDialog(self.session)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            name, price, stock_qty, image_path = dlg.get_values()
            self.model.addProduct(name, price, stock_qty, image_path)

    def delete_selected(self):
        selection = self.table.selectionModel().selectedRows()
        if not selection:
            QMessageBox.information(self, "No Selection", "No rows selected.")
            return
        rows = [index.row() for index in selection]
        self.model.deleteProducts(rows)
