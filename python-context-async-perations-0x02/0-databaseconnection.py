#!/usr/bin/python3
"""
Task 0: Custom Class-Based Context Manager for Database Connection
This script defines a DatabaseConnection context manager that automatically
handles opening and closing an SQLite database connection.
"""

import sqlite3


class DatabaseConnection:
    """A custom context manager for SQLite database connections."""

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Open the database connection and return the connection object."""
        self.conn = sqlite3.connect(self.db_name)
        print(f"Opened connection to {self.db_name}")
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        """Ensure the connection is closed properly, even if an exception occurs."""
        if self.conn:
            self.conn.close()
            print(f"Closed connection to {self.db_name}")
        # Returning False allows exceptions (if any) to propagate
        return False


if __name__ == "__main__":
    # Using the custom context manager to fetch users
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print("Users:", results)
