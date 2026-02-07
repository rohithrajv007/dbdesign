import mysql.connector


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "expense_tracker"
}

schema_sql = [

"""
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)
""",

"""
CREATE TABLE IF NOT EXISTS categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    type ENUM('Income','Expense'),
    icon_name VARCHAR(50)
)
""",

"""
CREATE TABLE IF NOT EXISTS password_resets (
    reset_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    reset_token TEXT NOT NULL,
    expiry_time DATETIME NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
)
""",

"""
CREATE TABLE IF NOT EXISTS income (
    income_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category_id INT,
    amount DECIMAL(10,2) NOT NULL,
    source VARCHAR(100),
    date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
)
""",

"""
CREATE TABLE IF NOT EXISTS budgets (
    budget_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    amount_limit DECIMAL(10,2) NOT NULL,
    month_year DATE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE(user_id, category_id, month_year),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
)
""",

"""
CREATE TABLE IF NOT EXISTS expenses (
    expense_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category_id INT,
    amount DECIMAL(10,2) NOT NULL,
    description TEXT,
    payment_mode VARCHAR(20),
    date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE SET NULL
)
""",

"""
CREATE INDEX idx_expenses_user ON expenses(user_id)
""",

"""
CREATE INDEX idx_expenses_date ON expenses(date)
"""
]


def setup_database():
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )

        cursor = conn.cursor()

        # Create DB if not exists
        cursor.execute("CREATE DATABASE IF NOT EXISTS expense_tracker")
        cursor.execute("USE expense_tracker")

        for query in schema_sql:
            cursor.execute(query)

        conn.commit()
        cursor.close()
        conn.close()

        print("✅ MySQL Database setup completed successfully!")

    except Exception as e:
        print("❌ Error:", e)


if __name__ == "__main__":
    setup_database()
