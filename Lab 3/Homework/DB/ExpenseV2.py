import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QTableWidget, QTableWidgetItem, 
    QLineEdit, QLabel, QPushButton, QMenuBar, QMenu, QMessageBox
)
from PyQt5.QtCore import Qt
from DB_Client import ExpensesDatabaseClient
from datetime import datetime

client = ExpensesDatabaseClient()

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
    def __init__(self, db_client: ExpensesDatabaseClient, parent=None):
        super().__init__(parent)
        self.db_client = db_client
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Expense", "Price", "Date", "Actions"])
        self.load_expenses()

    def load_expenses(self):
        expenses = self.db_client.read_all_expenses(3)
        for exp_id, expense, price, date in expenses:
            self.add_expense(expense, price, date, exp_id)

    def add_expense(self, expense_name, price, date, exp_id=None):
        row_position = self.rowCount()
        self.insertRow(row_position)
        self.setItem(row_position, 0, QTableWidgetItem(expense_name))
        self.setItem(row_position, 1, QTableWidgetItem(f"{price:.2f}"))
        self.setItem(row_position, 2, QTableWidgetItem(date))

        self.item(row_position, 0).setData(Qt.UserRole, exp_id)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda: self.delete_expense(exp_id, row_position))
        self.setCellWidget(row_position, 3, delete_button)

    def delete_expense(self, exp_id, row):
        self.db_client.delete_expense(exp_id)
        self.removeRow(row)
        self.parentWidget().parent().update_total()

    def calculate_total(self):
        total = 0.0
        for row in range(self.rowCount()):
            price_item = self.item(row, 1)
            if price_item:
                total += float(price_item.text())
        return total
    
class ExpenseInputPanel(QWidget):
    def __init__(self, table, db_client: ExpensesDatabaseClient, update_total_callback, parent=None):
        super().__init__(parent)
        self.table = table
        self.db_client = db_client
        self.update_total_callback = update_total_callback
        self.setup_input_panel()

    def setup_input_panel(self):
        layout = QHBoxLayout()
        
        # Inputs for expense and price
        self.expense_input = QLineEdit()
        self.expense_input.setPlaceholderText("Expense")
        self.expense_input.setFixedWidth(150)

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Price")
        self.price_input.setFixedWidth(100)

        # Inputs for date
        self.day_input = QLineEdit()
        self.day_input.setPlaceholderText("Day")
        self.day_input.setFixedWidth(50)

        self.month_input = QLineEdit()
        self.month_input.setPlaceholderText("Month")
        self.month_input.setFixedWidth(50)

        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("Year")
        self.year_input.setFixedWidth(60)

        # Buttons
        add_button = QPushButton("Add Expense")
        add_button.clicked.connect(self.add_expense)

        layout.addWidget(QLabel("Expense:"))
        layout.addWidget(self.expense_input)
        layout.addWidget(QLabel("Price:"))
        layout.addWidget(self.price_input)
        layout.addWidget(QLabel("Date (DD/MM/YYYY):"))
        layout.addWidget(self.day_input)
        layout.addWidget(self.month_input)
        layout.addWidget(self.year_input)
        layout.addWidget(add_button)
        self.setLayout(layout)

    def add_expense(self):
        expense_name = self.expense_input.text().strip()
        price_text = self.price_input.text().strip()
        
        day = self.day_input.text().strip()
        month = self.month_input.text().strip()
        year = self.year_input.text().strip()

        # Validate inputs
        if not expense_name or not price_text or not day or not month or not year:
            self.show_error("Please enter all inputs.")
            return

        try:
            # Check that the price is a valid, non-negative float
            price = float(price_text)
            if price < 0:
                self.show_error("Price cannot be negative.")
                return

            # Construct date from input and validate
            input_date_str = f"{day.zfill(2)}/{month.zfill(2)}/{year}"
            input_date = datetime.strptime(input_date_str, "%d/%m/%Y")
            
            # Get today's date
            today = datetime.today()
            
            # Ensure date is greater than year 2000 and less than today's date
            if input_date.year < 2000 or input_date >= today:
                self.show_error("Date must be before today and after the year 2000.")
                return

            # If valid, add the expense
            self.db_client.create_expense(expense_name, price, input_date_str)
            self.table.add_expense(expense_name, price, input_date_str)

            # Clear inputs and update total
            self.expense_input.clear()
            self.price_input.clear()
            self.day_input.clear()
            self.month_input.clear()
            self.year_input.clear()
            self.update_total_callback()

        except ValueError:
            self.show_error("Please enter a valid price and date.")


    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

class ExpenseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expense Tracker")
        self.setGeometry(100, 100, 600, 400)

        self.client = client

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        self.menu_bar = ExpenseMenu(self)
        self.setMenuBar(self.menu_bar)

        self.expense_table = ExpenseTable(self.client, self)
        
        self.expense_input_panel = ExpenseInputPanel(self.expense_table, self.client, self.update_total, self)
        self.layout.addWidget(self.expense_input_panel)
        self.layout.addWidget(self.expense_table)

        total_label = QLabel("Total:")
        self.total_value = QLabel("0.00")
        total_layout = QHBoxLayout()
        total_layout.addWidget(total_label)
        total_layout.addWidget(self.total_value)
        self.layout.addLayout(total_layout)

        self.update_total()  # Initial calculation of total

    def update_total(self):
        total = self.expense_table.calculate_total()
        self.total_value.setText(f"{total:.2f}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpenseApp()
    window.show()
    sys.exit(app.exec_())
