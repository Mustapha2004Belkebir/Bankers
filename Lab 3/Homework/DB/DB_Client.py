

import sqlite3
from typing import List, Tuple, Union

class ExpensesDatabaseClient:
    def __init__(self, db_name: str = 'expenses.db'):
        """Initialize the client and connect to the SQLite database."""
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        """Create the expenses table if it doesn't exist."""
        """These SQL scripts are well documented on ./init/init.sql"""
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                exp_id INTEGER PRIMARY KEY AUTOINCREMENT,
                expense TEXT NOT NULL,
                price REAL NOT NULL
            );
        ''')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_expense ON expenses(expense);')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_price ON expenses(price);')
        self.connection.commit()

    def create_expense(self, expense: str, price: float) -> None:
        """Add a new expense to the database."""
        self.cursor.execute("INSERT INTO expenses (expense, price) VALUES (?, ?);", (expense, price))
        self.connection.commit()

    def read_expenses(self) -> List[Tuple[int, str, float]]:
        """Retrieve all expenses from the database."""
        self.cursor.execute("SELECT * FROM expenses;")
        return self.cursor.fetchall()

    def update_expense(self, exp_id: int, expense: Union[str, None] = None, price: Union[float, None] = None) -> None:
        """Update an expense's details in the database."""
        if expense is not None and price is not None:
            self.cursor.execute("UPDATE expenses SET expense = ?, price = ? WHERE exp_id = ?;", (expense, price, exp_id))
        elif expense is not None:
            self.cursor.execute("UPDATE expenses SET expense = ? WHERE exp_id = ?;", (expense, exp_id))
        elif price is not None:
            self.cursor.execute("UPDATE expenses SET price = ? WHERE exp_id = ?;", (price, exp_id))
        self.connection.commit()

    def delete_expense(self, exp_id: int) -> None:
        """Delete an expense from the database by ID."""
        self.cursor.execute("DELETE FROM expenses WHERE exp_id = ?;", (exp_id,))
        self.connection.commit()

    def __del__(self):
        """Close the database connection when the instance is deleted."""
        self.connection.close()
