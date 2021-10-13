import sqlite3


class Connection:

    user_fields = ['password', 'first_name', 'last_name', 'birth_date', 'gender',
                   'email', 'phone_no', 'delivery_address', 'billing_address', 'tags']
    payment_fields = ['name_on_card', 'card_number', 'cvv', 'expiry_date']

    def __init__(self):
        """Creates a database connection"""
        self.connection = sqlite3.connect("ECommerce")
        self.cursor_object = self.connection.cursor()

    def create_user(self, user_name, password, first_name, email, **kwargs):
        """Creates user entry in user table"""
        keys = ','.join(kwargs.keys())
        values = ''
        for v in kwargs.values():
            if type(v) == int:
                values += str(v) + ', '
            else:
                values += "'" + v + "'" + ', '
        values = values.rstrip(', ')
        query = f"INSERT INTO users (user_name, password, first_name, email, {keys}) \
         VALUES('{user_name}', '{password}', '{first_name}', '{email}', {values})"
        self.cursor_object.execute(query)
        self.connection.commit()

    def get_user(self, user_name):
        """Gets user info from user table"""
        query = f"SELECT * FROM users WHERE user_name='{user_name}'"
        result = self.cursor_object.execute(query).fetchall()
        print(result)

    def update_user(self, user_name, **kwargs):
        """Updates user info in user table"""
        if len(kwargs) <= 0:
            raise KeyError('No Field To Update')

        for key in kwargs:
            if key not in self.user_fields:
                raise KeyError('Give Valid Field To Update')

        query = "UPDATE users SET "
        for field in self.user_fields:
            if field in kwargs:
                query += f"{field}='{kwargs[field]}',"

        query = query.rstrip(",")
        query += f" WHERE user_name='{user_name}'"
        self.cursor_object.execute(query)
        self.connection.commit()

    def delete_user(self, user_name):
        """Deletes user entry from user table"""
        query = f"DELETE FROM users WHERE user_name='{user_name}'"
        self.cursor_object.execute(query)
        self.connection.commit()

    def create_user_payments(self, user_name, name_on_card, card_number, cvv, expiry_date):
        """Creates user payments entry in payment_information table"""
        fetch = self.cursor_object.execute(f"SELECT id FROM users WHERE user_name='{user_name}'").fetchall()
        user_id = fetch[0][0]
        query = f"INSERT INTO payment_information (user_id, name_on_card, card_number, cvv, expiry_date)  \
                VALUES ('{user_id}', '{name_on_card}', '{card_number}', '{cvv}', '{expiry_date}')"
        self.cursor_object.execute(query)
        self.connection.commit()

    def get_user_payments(self, user_name):
        """Gets user payments info from payment_information table"""
        fetch = self.cursor_object.execute(f"SELECT id FROM users WHERE user_name='{user_name}'").fetchall()
        user_id = fetch[0][0]
        query = f"SELECT * FROM payment_information WHERE user_id='{user_id}'"
        result = self.cursor_object.execute(query).fetchall()
        print(result)

    def update_user_payments(self, user_name, **kwargs):
        """Updates user payments info in payment_information table"""
        if len(kwargs) <= 0:
            raise KeyError('No Field To Update')

        for key in kwargs:
            if key not in self.payment_fields:
                raise KeyError('Give Valid Field To Update')

        fetch = self.cursor_object.execute(f"SELECT id FROM users WHERE user_name='{user_name}'").fetchall()
        user_id = fetch[0][0]
        query = "UPDATE payment_information SET "
        for field in self.payment_fields:
            if field in kwargs:
                query += f"{field}='{kwargs[field]}',"
        query = query.rstrip(",")
        query += f" WHERE user_id='{user_id}'"
        self.cursor_object.execute(query)
        self.connection.commit()

    def delete_user_payments(self, user_name, card_number=None):
        """Deletes user payments entry from payment_information table"""
        fetch = self.cursor_object.execute(f"SELECT id FROM users WHERE user_name='{user_name}'").fetchall()
        user_id = fetch[0][0]
        if card_number is not None:
            query = f"DELETE FROM payment_information WHERE user_id='{user_id}' AND card_number='{card_number}'"
        else:
            query = f"DELETE FROM payment_information WHERE user_id='{user_id}'"
        self.cursor_object.execute(query)
        self.connection.commit()
