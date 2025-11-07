#!/usr/bin/python3
"""
0-stream_users.py
Contains a generator that streams rows from the user_data table one by one.
"""

import mysql.connector

def stream_users():
    """Generator function that fetches rows from user_data table one by one."""
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password',  # replace with your MySQL password
        database='your_database'   # replace with your database name
    )
    cursor = conn.cursor(dictionary=True)  # returns dict instead of tuple

    # Execute query to get all users
    cursor.execute("SELECT * FROM user_data")

    # Yield one row at a time
    for row in cursor:
        yield row

    # Close connection
    cursor.close()
    conn.close()
