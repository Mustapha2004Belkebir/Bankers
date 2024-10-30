import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QTableWidget, QTableWidgetItem, 
    QLineEdit, QLabel, QPushButton, QMenuBar, QMenu
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import QDate
from DB_Client import ExpensesDatabaseClient
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
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["Expense", "Price", "Actions"])
        self.load_expenses()

    def load_expenses(self):
        expenses = self.db_client.read_expenses()
        for exp_id, expense, price in expenses:
            self.add_expense(expense, price, exp_id)

    def add_expense(self, expense_name, price, exp_id=None):
        row_position = self.rowCount()
        self.insertRow(row_position)
        self.setItem(row_position, 0, QTableWidgetItem(expense_name))
        self.setItem(row_position, 1, QTableWidgetItem(f"{price:.2f}"))

        # Store exp_id in the item data for later retrieval
        self.item(row_position, 0).setData(Qt.UserRole, exp_id)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda: self.delete_expense(exp_id, row_position))
        self.setCellWidget(row_position, 2, delete_button)

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
class ExpenseSearch(QWidget):
    def __init__(self, expense_table):
        super().__init__()  
        self.expense_table = expense_table
        self.setup_search_panel()

    def setup_search_panel(self):
        layout = QHBoxLayout() 
        
        self.year_input = QComboBox()
        self.year_input.setFixedWidth(100)
        current_year = QDate.currentDate().year()
        for i in range(10):
            self.year_input.addItem(str(current_year - i))

        # Month ComboBox for selecting months
        self.month_input = QComboBox()
        self.month_input.setFixedWidth(100)
        months = ["January", "February", "March", "April", "May", "June", 
                  "July", "August", "September", "October", "November", "December"]
        self.month_input.addItems(months)
    
        # Search Button
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.filtered_expense)

        # Add widgets to layout
        layout.addWidget(QLabel("Search by Year and Month:"))
        layout.addWidget(self.year_input)
        layout.addWidget(self.month_input)
        layout.addWidget(search_button)
        
        self.setLayout(layout)


    def filtered_expense(self):
        year = self.year_input.currentText()
        month = self.month_input.currentIndex() + 1

        
        filtered_expenses = self.expense_table.db_client.search_expenses(year, month)
        self.expense_table.clear()

        for expense, price in filtered_expenses:
            self.expense_table.add_expense(expense, price)

class ExpenseInputPanel(QWidget):
    def __init__(self, table, db_client: ExpensesDatabaseClient, update_total_callback, parent=None):
        super().__init__(parent)
        self.table = table
        self.db_client = db_client
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

        update_button = QPushButton("Update Expense")
        update_button.clicked.connect(self.update_selected_expense)

        

        layout.addWidget(QLabel("Expense:"))
        layout.addWidget(self.expense_input)
        layout.addWidget(QLabel("Price:"))
        layout.addWidget(self.price_input)
        layout.addWidget(add_button)
        layout.addWidget(update_button)
        self.setLayout(layout)
    
   

    def add_expense(self):
        expense_name = self.expense_input.text().strip()
        price_text = self.price_input.text().strip()

        if not expense_name or not price_text:
            self.show_error("Please enter both expense and price.")
            return
        try:
            price = float(price_text)
            if price < 0:
                self.show_error("Price cannot be negative.")
                return
            self.db_client.create_expense(expense_name, price)
            self.table.add_expense(expense_name, price)

            self.expense_input.clear()
            self.price_input.clear()
            self.update_total_callback()
        except ValueError:
            self.show_error("Price must be a valid number.")

    def update_selected_expense(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            self.show_error("Please select a row to update.")
            return

        expense_name = self.expense_input.text().strip()
        price_text = self.price_input.text().strip()

        if not expense_name:
            self.show_error("Expense name cannot be empty.")
            return

        try:
            price = float(price_text)
        except ValueError:
            self.show_error("Please enter a valid numeric value for the price.")
            return

        exp_id = self.table.item(selected_row, 0).data(Qt.UserRole)  # Retrieve exp_id
        self.db_client.update_expense(exp_id, expense_name, price)
        self.table.setItem(selected_row, 0, QTableWidgetItem(expense_name))
        self.table.setItem(selected_row, 1, QTableWidgetItem(f"{price:.2f}"))

        self.expense_input.clear()
        self.price_input.clear()
        self.update_total_callback()

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

class ExpenseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expense Tracker")
        self.setGeometry(100, 100, 600, 300)

        # Initialize the database client here
        self.client = client

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        self.menu_bar = ExpenseMenu(self)
        self.setMenuBar(self.menu_bar)
 
        

        self.expense_table = ExpenseTable(self.client, self)
        self.expense_table.cellChanged.connect(self.update_total) # used for updating the total when 
        #changing the cell by double clicking on it 
        self.search_menu = ExpenseSearch(self.expense_table)

        self.expense_input_panel = ExpenseInputPanel(self.expense_table, self.client, self.update_total, self)
        self.layout.addWidget(self.expense_input_panel)
        self.layout.addWidget(self.search_menu)
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
