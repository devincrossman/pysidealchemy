from PySide6.QtCore import QAbstractTableModel, Qt

from db.models.products import Product


class ProductTableModel(QAbstractTableModel):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.products = self.session.query(Product).all()
        self.headers = ["ID", "Name", "Price", "Stock", "Image"]

    def rowCount(self, parent=None):
        return len(self.products)

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        product = self.products[index.row()]
        col = index.column()
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            if col == 0:
                return product.id
            elif col == 1:
                return product.name
            elif col == 2:
                return product.price
            elif col == 3:
                return product.stock
            elif col == 4:
                return product.image_path
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
        if index.column() == 0:  # ID is read-only
            return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        return (
            Qt.ItemFlag.ItemIsSelectable
            | Qt.ItemFlag.ItemIsEnabled
            | Qt.ItemFlag.ItemIsEditable
        )

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if not index.isValid() or role != Qt.ItemDataRole.EditRole:
            return False
        product = self.products[index.row()]
        col = index.column()
        if col == 1:
            product.name = str(value)
        elif col == 2:
            try:
                product.price = float(value)
            except ValueError:
                return False
        elif col == 3:
            try:
                product.stock = int(value)
            except ValueError:
                return False
        elif col == 4:
            product.image_path = str(value)
        self.session.commit()
        self.dataChanged.emit(index, index)
        return True

    def addProduct(self, name="New Product", price=0.0, stock=0, image_path=""):
        new_product = Product(
            name=name, price=price, stock=stock, image_path=image_path
        )
        self.session.add(new_product)
        self.session.commit()
        self.layoutAboutToBeChanged.emit()
        self.products = self.session.query(Product).all()
        self.layoutChanged.emit()

    def deleteProducts(self, rows):
        for row in sorted(rows, reverse=True):
            product = self.products[row]
            self.session.delete(product)
        self.session.commit()
        self.layoutAboutToBeChanged.emit()
        self.products = self.session.query(Product).all()
        self.layoutChanged.emit()
