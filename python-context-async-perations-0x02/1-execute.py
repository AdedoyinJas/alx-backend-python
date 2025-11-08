#!/usr/bin/python3
"""
Task 1: Reusable Query Context Manager
This script defines a class-based context manager ExecuteQuery
that manages both the database connection and query execution.
"""

import sqlite3


class ExecuteQuery:
    """Context manager to handle database connection and query execution."""

    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params is not None else ()
        self.conn = None
        self.results = None

    def __enter__(self):
        """Open connection, execute query, and return results."""
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        """Ensure the connection is closed properly."""
        if self.conn:
            self.conn.close()
        # Return False so exceptions (if any) are not suppressed
        return False


if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery("users.db", query, params) as results:
        print("Users older than 25:")
        print(results)
