#!/usr/bin/python3
"""
1-batch_processing.py
Implements batch processing for the user_data table.
"""

import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator that fetches rows from user_data table in batches."""
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password',  # replace with your MySQL password
        database='your_database'   # replace with your database name
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    batch = []
    for row in cursor:
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch

    cursor.close()
    conn.close()


def batch_processing(batch_size):
    """Processes each batch to filter users over the age of 25 and yields them."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:  # loop 2
            if user['age'] > 25:
                print(user)
