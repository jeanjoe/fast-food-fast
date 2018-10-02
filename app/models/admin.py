from app.models.connection import DatabaseConnection
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(DatabaseConnection):

    def __init__(self):
        super().__init__()

    def register_admin(self, firstname, lastname, email, password):
        try:
            query = """
            INSERT INTO ADMINS (firstname, lastname, email, password, created_at) VALUES 
            ('{}', '{}', '{}', '{}', '{}')
            """.format(firstname, lastname, email, generate_password_hash(password), datetime.now())
            self.cursor.execute(query)
            return True
        except Exception as error:
            return "Error {}".format(str(error))

    def search_admin(self, field, data):
        try:
            query = """
            SELECT * FROM ADMINS WHERE {} = '{}'
            """.format(field, data)
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            if row:
                return  row
            return False
        except Exception as error:
            return "Unable to search for this user => {} ".format(str(error))

    def signin_admin(self, email, password):
        """Sign in a user with email and password."""
        try:
            query = """
            SELECT * FROM ADMINS WHERE email= '{}'
            """.format(email)
            self.cursor.execute(query)
            user = self.cursor.fetchone()
            if user:
                check = self.check_password(user[5], password)
                if check:
                    return user
            return False
        except Exception as error:
            return "Unable to fin this user details. {} ".format(str(error))

    def check_password(self, hashed_password, confirm_password):
        return check_password_hash(hashed_password, confirm_password)