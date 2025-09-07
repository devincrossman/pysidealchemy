import csv
import os
import unittest

import pandas as pd
from PySide6.QtCore import QAbstractTableModel, Qt

from utils.export import export_to_csv, export_to_xlsx


class MockTableModel(QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self._headers = headers

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self._headers[section]
        return None


class TestExport(unittest.TestCase):
    def setUp(self):
        self.data = [
            [1, "Alice", "Engineer"],
            [2, "Bob", "Doctor"],
            [3, "Charlie", "Artist"],
        ]
        self.headers = ["ID", "Name", "Job"]
        self.model = MockTableModel(self.data, self.headers)
        self.csv_file = "test.csv"
        self.xlsx_file = "test.xlsx"

    def tearDown(self):
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)
        if os.path.exists(self.xlsx_file):
            os.remove(self.xlsx_file)

    def test_export_to_csv(self):
        export_to_csv(self.model, self.csv_file)
        self.assertTrue(os.path.exists(self.csv_file))
        with open(self.csv_file) as f:
            reader = csv.reader(f)
            self.assertEqual(next(reader), self.headers)
            for i, row in enumerate(reader):
                self.assertEqual(row, [str(x) for x in self.data[i]])

    def test_export_to_xlsx(self):
        export_to_xlsx(self.model, self.xlsx_file)
        self.assertTrue(os.path.exists(self.xlsx_file))
        df = pd.read_excel(self.xlsx_file)
        self.assertEqual(list(df.columns), self.headers)
        self.assertEqual(df.values.tolist(), self.data)


if __name__ == "__main__":
    unittest.main()
