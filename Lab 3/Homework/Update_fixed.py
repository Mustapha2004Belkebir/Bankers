import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QTableWidget, QTableWidgetItem, 
    QLineEdit, QLabel, QPushButton, QMenuBar, QMenu, QMessageBox
)
from PyQt5.QtCore import Qt

class ExpenseApp(QMainWindow):
    def __init__(self):
        super().__init__()

        
        self.setWindowTitle("Expense Tracker")
        self.setGeometry(100, 100, 600, 300)

        
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        
        layout = QVBoxLayout(central_widget)

        
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        
        file_menu = QMenu("File", self)
        edit_menu = QMenu("Edit", self)
        help_menu = QMenu("Help", self)
        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(edit_menu)
        menu_bar.addMenu(help_menu)

        
        top_panel = QHBoxLayout()
        layout.addLayout(top_panel)

        expense_label = QLabel("Expense:")
        self.expense_input = QLineEdit()
        self.expense_input.setFixedWidth(150)

        price_label = QLabel("Price:")
        self.price_input = QLineEdit()
        self.price_input.setFixedWidth(100)

        add_button = QPushButton("Add Expense")
        add_button.clicked.connect(self.add_expense)

        update_button = QPushButton("Update Expense")
        update_button.clicked.connect(self.update_selected_expense)

        top_panel.addWidget(expense_label)
        top_panel.addWidget(self.expense_input)
        top_panel.addWidget(price_label)
        top_panel.addWidget(self.price_input)
        top_panel.addWidget(add_button)
        top_panel.addWidget(update_button)

        
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Expense", "Price"])
        layout.addWidget(self.table)

        
        total_label = QLabel("Total:")
        self.total_value = QLabel("0.00")
        total_layout = QHBoxLayout()
        total_layout.addWidget(total_label)
        total_layout.addWidget(self.total_value)
        layout.addLayout(total_layout)

        
        self.table.setRowCount(3)
        initial_data = [("Veg", 40.0), ("Fruit", 70.0), ("Fuel", 60.0)]
        for row, (expense, price) in enumerate(initial_data):
            self.table.setItem(row, 0, QTableWidgetItem(expense))
            self.table.setItem(row, 1, QTableWidgetItem(f"{price:.2f}"))
        
        self.update_total()
        self.table.cellChanged.connect(self.update_total)

    def add_expense(self):
        
        expense_name = self.expense_input.text().strip()
        price_text = self.price_input.text().strip()

        
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(expense_name))
        self.table.setItem(row_position, 1, QTableWidgetItem(price_text))

        
        self.expense_input.clear()
        self.price_input.clear()

        
        self.update_total()

    def update_selected_expense(self):
        
        selected_row = self.table.currentRow()
        
        if selected_row == -1:
            self.show_error("Please select a row to update.")
            return

        
        expense_name = self.expense_input.text().strip()
        price_text = self.price_input.text().strip()

        
        try:
            price = float(price_text)
        except ValueError:
            self.show_error("Please enter a valid numeric value for the price.")
            return

        if not expense_name:
            self.show_error("Expense name cannot be empty.")
            return

        
        self.table.setItem(selected_row, 0, QTableWidgetItem(expense_name))
        self.table.setItem(selected_row, 1, QTableWidgetItem(f"{price:.2f}"))

        
        self.expense_input.clear()
        self.price_input.clear()

        
        self.update_total()

    def update_total(self):
        
        total = 0.0
        for row in range(self.table.rowCount()):
            price_item = self.table.item(row, 1)
            if price_item:
                try:
                    total += float(price_item.text())
                except ValueError:
                   
                    continue
        self.total_value.setText(f"{total:.2f}")

    def show_error(self, message):
        
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Warning)
        error_dialog.setText(message)
        error_dialog.setWindowTitle("Input Error")
        error_dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpenseApp()
    window.show()
    sys.exit(app.exec_())
