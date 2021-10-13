import sqlite3
from sqlite3 import Error


def get_connection(db_name):
    """Creates a database connection"""
    connection = None
    try:
        connection = sqlite3.connect(db_name)
        return connection
    except Error as e:
        print(e)
    return connection


def create_table(connection, create_table_sql):
    """Creates a table in database"""
    try:
        cursor_object = connection.cursor()
        cursor_object.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = "ECommerce"

    sql_create_user_table = """ CREATE TABLE IF NOT EXISTS users (   
                                         id INTEGER PRIMARY KEY,
                                         user_name TEXT NOT NULL UNIQUE,
                                         password TEXT NOT NULL,
                                         first_name TEXT NOT NULL,
                                         last_name TEXT,
                                         birth_date TEXT,
                                         gender TEXT,
                                         email TEXT NOT NULL,
                                         phone_no INTEGER,
                                         delivery_address TEXT,
                                         billing_address TEXT,
                                         tags TEXT
                                       ); """

    sql_create_payment_information_table = """ CREATE TABLE IF NOT EXISTS payment_information (
                                                      payment_id INTEGER PRIMARY KEY,
                                                      user_id INTEGER NOT NULL,
                                                      name_on_card TEXT NOT NULL,
                                                      card_number INTEGER NOT NULL,
                                                      cvv INTEGER NOT NULL,
                                                      expiry_date TEXT NOT NULL,     
                                                      FOREIGN KEY (user_id) REFERENCES users (id)                                                                      
                                                      ); """
    connection = get_connection(database)
    if connection is not None:
        create_table(connection, sql_create_user_table)
        create_table(connection, sql_create_payment_information_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()