from app.models.connection import DatabaseConnection
from datetime import datetime

class User(DatabaseConnection):

    def __init__(self):
        super().__init__()

    def register_user(self, firstname, lastname, email, phone, password):
        try:
            query = """
            INSERT INTO USERS (first_name, last_name, email, phone, password, created_at) VALUES 
            ('{}', '{}', '{}', '{}', '{}', '{}')
            """.format(firstname, lastname, email, phone, password, datetime.now())
            self.cursor.execute(query)
            return True
        except Exception as error:
            return "Error {}".format(str(error))

    def search_user(self, field, data):
        try:
            query = """
            SELECT * FROM USERS WHERE {} = '{}'
            """.format(field, data)
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            if row:
                return  row
            return False
        except Exception as error:
            return "Unable to search for this user => {} ".format(str(error))