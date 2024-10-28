CREATE TABLE expenses (
    exp_id INTEGER PRIMARY KEY,
    expense TEXT NOT NULL,
    price REAL NOT NULL
);

CREATE INDEX idx_expense ON expenses(expense);
CREATE INDEX idx_price ON expenses(price);
