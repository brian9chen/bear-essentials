from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, id, email, password, firstname, lastname, address, balance=0, is_seller=False):
        self.id = id
        self.email = email
        self.password = password  # Assume this is the hashed password
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.balance = balance
        self.is_seller = is_seller

    @staticmethod
    def get(user_id):
        rows = app.db.execute('''
        SELECT id, email, password, firstname, lastname, address, balance, is_seller
        FROM Users
        WHERE id = :user_id
        ''', user_id=user_id)
        
        return User(*rows[0]) if rows else None

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute('''
        SELECT id, email, password, firstname, lastname, address, balance, is_seller
        FROM Users
        WHERE email = :email
        ''', email=email)
        
        if not rows:
            return None  # Email not found

        # Verify the password
        if not check_password_hash(rows[0][2], password):
            return None  # Incorrect password

        # Return the User object without re-hashing the password
        return User(id=rows[0][0], email=rows[0][1], password=rows[0][2],
                    firstname=rows[0][3], lastname=rows[0][4], address=rows[0][5],
                    balance=rows[0][6], is_seller=rows[0][7])

    @staticmethod
    def email_exists(email):
        rows = app.db.execute('''
        SELECT email
        FROM Users
        WHERE email = :email
        ''', email=email)
        return len(rows) > 0

    @staticmethod
    def register(uid, email, password, firstname, lastname, address, balance=0, is_seller=False):
        try:
            hashed_password = generate_password_hash(password)
            app.db.execute('''
            INSERT INTO Users(id, email, password, firstname, lastname, address, balance, is_seller)
            VALUES(:id, :email, :password, :firstname, :lastname, :address, :balance, :is_seller)
            ''',
            id=uid, email=email, password=hashed_password,
            firstname=firstname, lastname=lastname, address=address,
            balance=balance, is_seller=is_seller)
            return True
        except Exception as e:
            print(str(e))
            return False
