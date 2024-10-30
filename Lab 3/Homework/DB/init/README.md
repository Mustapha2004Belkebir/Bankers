# Documentation for `init.sql`

## Overview

The `init.sql` file is a SQL script designed to set up an SQLite database with a table named `expenses` and create indexes to improve query performance. This file can be executed to initialize the database structure before performing any operations.

## Contents of `init.sql`

The script contains the following SQL commands:

1. **Create Table**: Creates the `expenses` table if it does not already exist.
   - **Columns**:
     - `exp_id`: An integer that serves as the primary key and auto-increments for each new entry.
     - `expense`: A text field to store the description of the expense (cannot be null).
     - `price`: A real number to store the cost of the expense (cannot be null).
     - `date`: A `YYYY-MM-DD` format date, it should be sent by the consumer of the interface.

2. **Create Indexes**: Creates indexes on the `expense` and `price` columns to optimize search queries.
   - `idx_expense`: An index on the `expense` column to speed up searches based on expense descriptions.
   - `idx_price`: An index on the `price` column to enhance performance for queries involving expense amounts.

## Usage

To use the `init.sql` file:

1. **Ensure SQLite is Installed**: Make sure you have SQLite installed on your system. You can check this by running `sqlite3` in your command line.

2. **Create a New SQLite Database**: If you don't have an existing database, create a new SQLite database file. For example:
   ```bash
   sqlite3 expenses.db
   ```

3. **Execute the SQL Script**: Run the `init.sql` file to set up the database structure:
   ```bash
   sqlite3 expenses.db < path/to/init.sql
   ```
   Replace `path/to/init.sql` with the actual path to your `init.sql` file.

4. **Verify the Setup**: After executing the script, you can verify that the table and indexes have been created by running:
   ```sql
   .tables
   ```
   and
   ```sql
   .schema expenses
   ```

## Example

Here is a complete example of how to initialize your database:

```bash
# Create the SQLite database
sqlite3 expenses.db

# Execute the initialization script
sqlite3 expenses.db < init.sql

# Verify the table and indexes
.tables
.schema expenses
```

## Conclusion

The `init.sql` file provides a simple way to set up the database schema for managing expenses. By executing this script, members can quickly prepare the database for subsequent operations using the provided Python client.
