import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QTableWidget, QTableWidgetItem, 
    QLineEdit, QLabel, QPushButton, QMenuBar, QMenu
)
from PyQt5.QtCore import Qt

class ExpenseMenu(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_menu()

    def setup_menu(self):
        file_menu = QMenu("File", self)
        edit_menu = QMenu("Edit", self)
        help_menu = QMenu("Help", self)
        self.addMenu(file_menu)
        self.addMenu(edit_menu)
        self.addMenu(help_menu)

class ExpenseTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Expense", "Price"])
        self.setRowCount(0)  # Start with no rows

        # Initialize with default data
        initial_data = [("Veg", 40.0), ("Fruit", 70.0), ("Fuel", 60.0)]
        for expense, price in initial_data:
            self.add_expense(expense, price)

    def add_expense(self, expense_name, price):
        row_position = self.rowCount()
        self.insertRow(row_position)
        self.setItem(row_position, 0, QTableWidgetItem(expense_name))
        self.setItem(row_position, 1, QTableWidgetItem(f"{price:.2f}"))

    def calculate_total(self):
        total = 0.0
        for row in range(self.rowCount()):
            price_item = self.item(row, 1)
            if price_item:
                total += float(price_item.text())
        return total

class ExpenseInputPanel(QWidget):
    def __init__(self, table, update_total_callback, parent=None):
        super().__init__(parent)
        self.table = table
        self.update_total_callback = update_total_callback
        self.setup_input_panel()

    def setup_input_panel(self):
        layout = QHBoxLayout()
        self.expense_input = QLineEdit()
        self.expense_input.setPlaceholderText("Expense")
        self.expense_input.setFixedWidth(150)

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Price")
        self.price_input.setFixedWidth(100)

        add_button = QPushButton("Add Expense")
        add_button.clicked.connect(self.add_expense)

        layout.addWidget(QLabel("Expense:"))
        layout.addWidget(self.expense_input)
        layout.addWidget(QLabel("Price:"))
        layout.addWidget(self.price_input)
        layout.addWidget(add_button)
        self.setLayout(layout)

    def add_expense(self):
        expense_name = self.expense_input.text().strip()
        price_text = self.price_input.text().strip()

        try:
            price = float(price_text)
            self.table.add_expense(expense_name, price)
            self.expense_input.clear()
            self.price_input.clear()
            self.update_total_callback()
        except ValueError:
            print("Please enter a valid number for price.")

class ExpenseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expense Tracker")
        self.setGeometry(100, 100, 600, 300)

        # Set up the main layout and menu
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        self.menu_bar = ExpenseMenu(self)
        self.setMenuBar(self.menu_bar)

        # Set up the table and input panel
        self.expense_table = ExpenseTable(self)
        self.expense_input_panel = ExpenseInputPanel(self.expense_table, self.update_total, self)
        self.layout.addWidget(self.expense_input_panel)

        self.layout.addWidget(self.expense_table)


        # Create the bottom panel for displaying the total
        total_label = QLabel("Total:")
        self.total_value = QLabel("0.00")
        total_layout = QHBoxLayout()
        total_layout.addWidget(total_label)
        total_layout.addWidget(self.total_value)
        self.layout.addLayout(total_layout)

        self.update_total()  # Initial calculation of total

    def update_total(self):
        total = self.expense_table.calculate_total()
        self.total_value.setText(f" {total:.2f}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpenseApp()
    window.show()
    sys.exit(app.exec_())
