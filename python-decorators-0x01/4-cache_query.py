#!/usr/bin/python3
import sqlite3
import functools

query_cache = {}


def with_db_connection(func):
    """
    Decorator that handles opening and closing a database connection.
    Passes the connection to the wrapped function.
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


def cache_query(func):
    """
    Decorator that caches query results based on the SQL query string.
    Avoids redundant database calls.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query")
        if query in query_cache:
            print("Using cached result for query:", query)
            return query_cache[query]

        result = func(*args, **kwargs)
        query_cache[query] = result
        print("Caching result for query:", query)
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """Fetch users and cache results to avoid redundant queries."""
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    # First call caches the result
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print("First call result:", users)

    # Second call reuses cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print("Second call (cached):", users_again)
