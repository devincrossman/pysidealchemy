import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)

from utils.config import app_path


class AddProductDialog(QDialog):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.setWindowTitle("Add Product")
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        self.name = QLineEdit()
        form_layout.addRow("Name", self.name)

        self.price = QDoubleSpinBox()
        self.price.setDecimals(2)
        self.price.setMinimum(0.0)
        self.price.setMaximum(9999.99)
        form_layout.addRow("Price", self.price)

        self.stock_qty = QSpinBox()
        self.stock_qty.setMinimum(0)
        self.stock_qty.setMaximum(10000)
        form_layout.addRow("Stock Qty", self.stock_qty)

        self.image_path = ""
        self.select_image_button = QPushButton("Select Image")
        self.select_image_button.clicked.connect(self.select_image)
        form_layout.addRow("Image", self.select_image_button)

        layout.addLayout(form_layout)

        self.image_preview = QLabel()
        self.image_preview.setFixedSize(100, 100)
        self.image_preview.setStyleSheet("border: 1px solid gray;")
        self.image_preview.setScaledContents(True)
        self.image_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addRow("", self.image_preview)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def accept(self):
        if len(self.name.text()) == 0:
            QMessageBox.warning(self, "Invalid Product", "A product must have a name.")
            return
        super().accept()

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp)",
        )
        if file_path:
            self.image_path = os.path.relpath(file_path, app_path())
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                self.image_preview.setPixmap(
                    pixmap.scaled(
                        self.image_preview.size(),
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                )
        else:
            self.image_path = ""
            self.image_preview.clear()

    def get_values(self):
        name = self.name.text()
        price = self.price.value()
        stock_qty = self.stock_qty.value()
        image_path = self.image_path
        return name, price, stock_qty, image_path
