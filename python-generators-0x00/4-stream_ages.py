#!/usr/bin/python3
"""
4-stream_ages.py
Compute memory-efficient average age using generators.
"""

import mysql.connector


def stream_user_ages():
    """Generator that yields ages of users one by one."""
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password',  # replace with your MySQL password
        database='your_database'   # replace with your database name
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:  # loop 1
        yield row['age']

    cursor.close()
    conn.close()


def calculate_average_age():
    """Calculates the average age using the generator."""
    total = 0
    count = 0

    for age in stream_user_ages():  # loop 2
        total += age
        count += 1

    average = total / count if count else 0
    print(f"Average age of users: {average:.2f}")


if __name__ == "__main__":
    calculate_average_age()
