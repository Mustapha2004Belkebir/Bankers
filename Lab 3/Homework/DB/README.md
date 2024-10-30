 ## Guide to Installing SQLite and Using the `ExpensesDatabaseClient` Python Client

### 1. Installing SQLite

SQLite is a self-contained, serverless database engine that is simple to set up. Follow these steps for installation on Windows and Linux.

---

#### For Windows

1. **Download SQLite:**
   - Visit the [SQLite download page](https://www.sqlite.org/download.html).
   - Under the "Precompiled Binaries for Windows" section, download the ZIP file for the SQLite tools (e.g., `sqlite-tools-win32-x86-*.zip`).

2. **Extract the ZIP File:**
   - Extract the downloaded ZIP file to a folder (e.g., `C:\sqlite`).

3. **Add SQLite to PATH:**
   - Open the Start menu, search for "Environment Variables," and open it.
   - In the System Properties window, click on "Environment Variables."
   - Under "System variables," find the `Path` variable, select it, and click "Edit."
   - Click "New" and add the path to the SQLite folder (e.g., `C:\sqlite`).
   - Click "OK" to save the changes.

4. **Verify the Installation:**
   - Open Command Prompt and type `sqlite3`.
   - You should see the SQLite prompt (`sqlite>`), indicating that SQLite is installed and ready to use.

---

#### For Linux

1. **Update Package Index:**
   - Open a terminal and update the package index by running:
     ```bash
     sudo apt update
     ```

2. **Install SQLite:**
   - Use the following command to install SQLite:
     ```bash
     sudo apt install sqlite3
     ```

3. **Verify the Installation:**
   - Run the command `sqlite3` in your terminal.
   - You should see the SQLite prompt (`sqlite>`), indicating a successful installation.

---

### 2. Setting Up the Python Client

With SQLite installed, you can now use the `ExpensesDatabaseClient` Python client to manage an SQLite database for storing and interacting with expenses data.

#### Step 1: Install Python (if not already installed)

Ensure Python 3 is installed. You can verify by running:

```bash
python3 --version
```

If Python isn’t installed, download and install it from [Python's official website](https://www.python.org/downloads/).

#### Step 2: Install Required Python Modules

The `ExpensesDatabaseClient` only requires the standard `sqlite3` library, which is included with Python. No additional libraries are needed.

#### Step 3: About the `ExpensesDatabaseClient` Python Client in `DB_Client.py`

This file defines the `ExpensesDatabaseClient` class, which includes methods for basic CRUD operations on the `expenses` table.

#### Step 4: Using the Client in a Script

To use the `ExpensesDatabaseClient`, create another Python file where your main code lives, e.g. `main.py`. This is an example usage of this client:

```python
from DB_Client import ExpensesDatabaseClient

# Initialize the database client
client = ExpensesDatabaseClient()

# Create some expenses with date
client.create_expense("Lunch", 12.50, date="2024-10-30")
client.create_expense("Books", 30.00, date="2024-11-01")
client.create_expense("Groceries", 45.75, date="2024-11-02")

# Retrieve all expenses with pagination (limit 2 per page)
print("Page 1 of Expenses:")
expenses_page_1 = client.read_expenses(limit=2, offset=0)
print(expenses_page_1)

print("Page 2 of Expenses:")
expenses_page_2 = client.read_expenses(limit=2, offset=2)
print(expenses_page_2)

# Update an expense (update date along with expense and price)
if expenses_page_1:
    client.update_expense(expenses_page_1[0][0], expense="Lunch with coffee", price=15.00, date="2024-10-31")

# Read updated expenses to verify changes
updated_expenses = client.read_expenses(limit=10)
print("Updated Expenses:", updated_expenses)

# Search for expenses by filtering on specific fields
print("Search for expenses containing 'Lunch':")
search_results = client.search_expenses(expense="Lunch")
print(search_results)

print("Search for expenses on 2024-11-01:")
search_results_date = client.search_expenses(date="2024-11-01", limit=10, offset=2)
print(search_results_date)

print("Search for expenses with price 45.75:")
search_results_price = client.search_expenses(price=45.75)
print(search_results_price)

# Delete an expense
if updated_expenses:
    client.delete_expense(updated_expenses[1][0])

# Read final expenses to verify deletion
final_expenses = client.read_expenses(limit=10)
print("Final Expenses:", final_expenses)
```

#### Step 5: Running the Script

To run the client and perform CRUD operations, use the following command:

```bash
python main.py
```

### 3. Explanation of CRUD Operations in `ExpensesDatabaseClient`

1. **`create_expense`**: Inserts a new record into the `expenses` table.
2. **`read_expenses`**: Retrieves all rows from the `expenses` table.
3. **`update_expense`**: Updates a specific record identified by `exp_id`.
4. **`delete_expense`**: Deletes a record from the table based on `exp_id`.
5. **`search_expenses`**: Search expenses by filtering on expense, price, and/or date with pagination.

Each function commits changes to the SQLite database, making the updates permanent.

### Summary

With this setup:
- You can install and set up SQLite.
- Use the `ExpensesDatabaseClient` class for structured, object-oriented CRUD interactions with the SQLite database.
  
This setup allows easy management of expense records and can be adapted for other data structures or requirements by extending the `ExpensesDatabaseClient` class. Let me know if you’d like additional features!