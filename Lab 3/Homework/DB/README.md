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
from expenses_db_client import ExpensesDatabaseClient

# Initialize the database client
client = ExpensesDatabaseClient()

# Create some expenses
client.create_expense("Lunch", 12.50)
client.create_expense("Books", 30.00)

# Retrieve all expenses
expenses = client.read_expenses()
print("All Expenses:", expenses)

# Update an expense
if expenses:
    client.update_expense(expenses[0][0], expense="Lunch with coffee", price=15.00)

# Read updated expenses
updated_expenses = client.read_expenses()
print("Updated Expenses:", updated_expenses)

# Delete an expense
if updated_expenses:
    client.delete_expense(updated_expenses[1][0])

# Read final expenses
final_expenses = client.read_expenses()
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

Each function commits changes to the SQLite database, making the updates permanent.

### Summary

With this setup:
- You can install and set up SQLite.
- Use the `ExpensesDatabaseClient` class for structured, object-oriented CRUD interactions with the SQLite database.
  
This setup allows easy management of expense records and can be adapted for other data structures or requirements by extending the `ExpensesDatabaseClient` class. Let me know if you’d like additional features!