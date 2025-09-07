import csv
from PySide6.QtCore import QAbstractTableModel, Qt
import pandas as pd


def export_to_csv(model: QAbstractTableModel, file_path: str):
    """Exports the data from a QAbstractTableModel to a CSV file."""
    try:
        with open(file_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)

            # Write headers
            headers = [
                model.headerData(i, Qt.Orientation.Horizontal)
                for i in range(model.columnCount())
            ]
            writer.writerow(headers)

            # Write data
            for row in range(model.rowCount()):
                row_data = [
                    model.data(model.index(row, col))
                    for col in range(model.columnCount())
                ]
                writer.writerow(row_data)
    except Exception as e:
        print(f"Error exporting to CSV: {e}")


def export_to_xlsx(model: QAbstractTableModel, file_path: str):
    """Exports the data from a QAbstractTableModel to an XLSX file."""
    try:
        headers = [
            model.headerData(i, Qt.Orientation.Horizontal)
            for i in range(model.columnCount())
        ]
        data = [
            [model.data(model.index(row, col)) for col in range(model.columnCount())]
            for row in range(model.rowCount())
        ]

        df = pd.DataFrame(data, columns=headers)
        df.to_excel(file_path, index=False)
    except Exception as e:
        print(f"Error exporting to XLSX: {e}")
