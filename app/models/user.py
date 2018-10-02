from app.models.connection import DatabaseConnection
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(DatabaseConnection):

    def __init__(self):
        super().__init__()

    def register_user(self, firstname, lastname, email, phone, password, account_type):
        try:
            query = """
            INSERT INTO USERS (first_name, last_name, email, phone, password, account_type, created_at) VALUES 
            ('{}', '{}', '{}', '{}', '{}', '{}', '{}')
            """.format(
                firstname, lastname, email, phone, generate_password_hash(password), account_type, 
                datetime.now()
            )
            self.cursor.execute(query)
            return True
        except Exception as error:
            print(str(error))
            return "Error {}".format(str(error))

    def search_user(self, field, data):
        try:
            query = """
            SELECT * FROM USERS WHERE {} = '{}'
            """.format(field, data)
            self.dict_cursor.execute(query)
            row = self.dict_cursor.fetchone()
            if row:
                return  row
            return False
        except Exception as error:
            return "Unable to search for this user => {} ".format(str(error))

    def signin_user(self, email, password):
        """Sign in a user with email and password."""
        query = """
        SELECT * FROM USERS WHERE email= '{}' AND account_type='client'
        """.format(email)
        self.dict_cursor.execute(query)
        user = self.dict_cursor.fetchone()
        if user:
            check = self.check_password(user['password'], password)
            if check:
                return user
        return False

    def signin_admin(self, email, password):
        """Sign in an admin user with email and password."""
        query = """
        SELECT * FROM USERS WHERE email= '{}' AND account_type='admin'
        """.format(email)
        self.dict_cursor.execute(query)
        user = self.dict_cursor.fetchone()
        if user:
            check = self.check_password(user['password'], password)
            if check:
                return user
        return False

    def check_password(self, hashed_password, confirm_password):
        return check_password_hash(hashed_password, confirm_password)

    def admin_get_orders(self):
        query = """SELECT * FROM ORDERS"""
        self.dict_cursor.execute(query)
        return self.dict_cursor.fetchall()

    def admin_update_order(self, admin_id, order_id, status):
        """Admin updates specific order status."""
        query = """
        UPDATE ORDERS SET status= '{}', approved_by= {}, approved_at= '{}' WHERE id= {}
        """.format(status, admin_id, str(datetime.now()), order_id)
        self.cursor.execute(query)
        return True