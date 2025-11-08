#!/usr/bin/python3
import sqlite3
import functools


def with_db_connection(func):
    """
    Decorator that automatically opens and closes a database connection.
    Passes the connection to the decorated function as the first argument.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    """Fetch a user by ID using the provided database connection."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


if __name__ == "__main__":
    user = get_user_by_id(user_id=1)
    print(user)
