#!/usr/bin/python3
"""
2-lazy_paginate.py
Implements lazy pagination using a generator.
"""

seed = __import__('seed')


def paginate_users(page_size, offset):
    """
    Fetches a page of users starting at the given offset.
    Returns a list of dictionaries.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily fetches pages of users using paginate_users.
    """
    offset = 0
    while True:  # only 1 loop
        page = paginate_users(page_size, offset)
        if not page:  # no more rows
            break
        yield page
        offset += page_size
