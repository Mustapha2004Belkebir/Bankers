

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
                price REAL NOT NULL,
                date DATE NOT NULL
            );
        ''')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_expense ON expenses(expense);')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_price ON expenses(price);')
        self.connection.commit()
    def create_expense(self, expense: str, price: float, date: str) -> None:
        """Add a new expense to the database with a provided date."""
        self.cursor.execute(
            "INSERT INTO expenses (expense, price, date) VALUES (?, ?, ?);",
            (expense, price, date)
        )
        self.connection.commit()
    def read_all_expenses(self, limit: int, offset: int = 0) -> List[Tuple[int, str, float, str]]:
        """Retrieve expenses from the database with pagination."""
        self.cursor.execute(
            "SELECT * FROM expenses LIMIT ? OFFSET ?;", 
            (limit, offset)
        )
        return self.cursor.fetchall()
    def update_expense(self, exp_id: int, expense: Union[str, None] = None, price: Union[float, None] = None, date: Union[str, None] = None) -> None:
        """Update an expense's details in the database."""
        # Prepare the SQL query based on which parameters are provided
        if expense is not None and price is not None and date is not None:
            self.cursor.execute("UPDATE expenses SET expense = ?, price = ?, date = ? WHERE exp_id = ?;", (expense, price, date, exp_id))
        elif expense is not None and price is not None:
            self.cursor.execute("UPDATE expenses SET expense = ?, price = ? WHERE exp_id = ?;", (expense, price, exp_id))
        elif expense is not None and date is not None:
            self.cursor.execute("UPDATE expenses SET expense = ?, date = ? WHERE exp_id = ?;", (expense, date, exp_id))
        elif price is not None and date is not None:
            self.cursor.execute("UPDATE expenses SET price = ?, date = ? WHERE exp_id = ?;", (price, date, exp_id))
        elif expense is not None:
            self.cursor.execute("UPDATE expenses SET expense = ? WHERE exp_id = ?;", (expense, exp_id))
        elif price is not None:
            self.cursor.execute("UPDATE expenses SET price = ? WHERE exp_id = ?;", (price, exp_id))
        elif date is not None:
            self.cursor.execute("UPDATE expenses SET date = ? WHERE exp_id = ?;", (date, exp_id))
            
        self.connection.commit()

    def search_expenses(self, expense: Union[str, None] = None, price: Union[float, None] = None, year: Union[int, None] = None, month: Union[int, None] = None, limit: int = 10, offset: int = 0) -> List[Tuple[int, str, float, str]]:
        """Search expenses by filtering on expense, price, year, or month with pagination."""
        # Base query
        query = "SELECT * FROM expenses WHERE"
        filters = []
        values = []

        # Add filters based on provided parameters
        if expense is not None:
            filters.append("expense LIKE ?")
            values.append(f"%{expense}%")  # Using LIKE for partial matches
        if price is not None:
            filters.append("price = ?")
            values.append(price)
        if year is not None:
            filters.append("strftime('%Y', date) = ?")
            values.append(str(year))  # Year as string for comparison
        if month is not None:
            filters.append("strftime('%m', date) = ?")
            values.append(f"{month:02d}")  # Format month as two digits (e.g., '01', '02')

        # If no filters are provided, use a base query with pagination
        if not filters:
            query = "SELECT * FROM expenses"
        else:
            # Join filters with AND
            query += " AND ".join(filters)

        # Add pagination
        query += " LIMIT ? OFFSET ?"
        values.extend([limit, offset])

        # Execute the query
        self.cursor.execute(query, values)
        return self.cursor.fetchall()
    def delete_expense(self, exp_id: int) -> None:
        """Delete an expense from the database by ID."""
        self.cursor.execute("DELETE FROM expenses WHERE exp_id = ?;", (exp_id,))
        self.connection.commit()
    def __del__(self):
        """Close the database connection when the instance is deleted."""
        self.connection.close()
