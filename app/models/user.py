"""Manage users."""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .connection import DatabaseConnection

class User(DatabaseConnection):
    """Manage user DB interaction."""
    def register_user(self, firstname, lastname, email, password, account_type):
        """Register users."""
        query = """
        INSERT INTO USERS (first_name, last_name, email, password, account_type, created_at) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(
            query,
            (
                firstname, lastname, email, generate_password_hash(password), account_type,
                datetime.now()
            )
        )
        return True

    def search_user(self, field, data):
        """Execute search."""
        query = """
        SELECT * FROM USERS WHERE {} = '{}'
        """.format(field, data)
        self.dict_cursor.execute(query)
        return self.dict_cursor.fetchone()

    def signin_user(self, email, password):
        """Sign in a user with the"""
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
        """Check if hashed password matches row password."""
        return check_password_hash(hashed_password, confirm_password)

    def admin_get_orders(self):
        """Get all oders for admin."""
        query = """SELECT * FROM ORDERS"""
        self.dict_cursor.execute(query)
        return self.dict_cursor.fetchall()

    def admin_update_order(self, admin_id, order_id, status):
        """Admin updates specific order status."""
        query = """
        UPDATE ORDERS SET status= %s, approved_by= %s, approved_at= %s WHERE id= %s
        """
        self.cursor.execute(query, (status, admin_id, str(datetime.now()), order_id))
        return True
