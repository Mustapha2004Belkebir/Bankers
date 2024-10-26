import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QTableWidget, QTableWidgetItem, 
    QLineEdit, QLabel, QPushButton, QMenuBar, QMenu
)
from PyQt5.QtCore import Qt

class ExpenseApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Expense Tracker")
        self.setGeometry(100, 100, 600, 300)

        # Create a central widget and set it as the central widget of the QMainWindow
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a vertical layout for the central widget
        layout = QVBoxLayout(central_widget)

        # Create a menu bar
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        
        file_menu = QMenu("File", self)
        edit_menu = QMenu("Edit", self)
        help_menu = QMenu("Help", self)
        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(edit_menu)
        menu_bar.addMenu(help_menu)

        # Create the top panel for input fields and add button
        top_panel = QHBoxLayout()
        layout.addLayout(top_panel)

        # Create labels and text fields for "Expense" and "Price"
        expense_label = QLabel("Expense:")
        self.expense_input = QLineEdit()
        self.expense_input.setFixedWidth(150)

        price_label = QLabel("Price:")
        self.price_input = QLineEdit()
        self.price_input.setFixedWidth(100)

        # Create the button to add expenses
        add_button = QPushButton("Add Expense")
        add_button.clicked.connect(self.add_expense)

        # Add widgets to the top panel
        top_panel.addWidget(expense_label)
        top_panel.addWidget(self.expense_input)
        top_panel.addWidget(price_label)
        top_panel.addWidget(self.price_input)
        top_panel.addWidget(add_button)

        # Create the table to display expenses
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Expense", "Price"])
        layout.addWidget(self.table)

        # Create the bottom panel for displaying the total
        total_label = QLabel("Total:")
        self.total_value = QLabel("0.00")
        total_layout = QHBoxLayout()
        total_layout.addWidget(total_label)
        total_layout.addWidget(self.total_value)
        layout.addLayout(total_layout)

        # Initialize with default data
        self.table.setRowCount(3)
        initial_data = [("Veg", 40.0), ("Fruit", 70.0), ("Fuel", 60.0)]
        for row, (expense, price) in enumerate(initial_data):
            self.table.setItem(row, 0, QTableWidgetItem(expense))
            self.table.setItem(row, 1, QTableWidgetItem(str(price)))
        
        self.update_total()

    def add_expense(self):
        # Get the values from the input fields
        expense_name = self.expense_input.text().strip()
        price_text = self.price_input.text().strip()

        # Add a new row to the table
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(expense_name))
        self.table.setItem(row_position, 1, QTableWidgetItem(price_text))

        # Clear the input fields
        self.expense_input.clear()
        self.price_input.clear()

        # Update the total
        self.update_total()

    def update_total(self):
        # Calculate the total price
        total = 0.0
        for row in range(self.table.rowCount()):
            price_item = self.table.item(row, 1)
            if price_item:
                total += float(price_item.text())
        self.total_value.setText(f"{total:.2f}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpenseApp()
    window.show()
    sys.exit(app.exec_())
