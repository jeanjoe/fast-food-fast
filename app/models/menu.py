from app.models.connection import DatabaseConnection
from datetime import datetime

class MenuModel(DatabaseConnection):

    def __init__(self):
        super().__init__()

    def add_menu(self, admin_id, title, description, price):
        try:
            query= """
            INSERT INTO MENUS (admin_id, title, description, price, status, created_at) VALUES
            ({0}, {1}, '{2}', {3}, '{4}', '{5}')
            """.format(admin_id, title, description, price, 1, str(datetime.now()))
            self.cursor.execute(query)
            return "Data Inserted Successfully"
        except Exception as error:
            return "Unable to save error {} ".format(str(error))

    def get_all_client_menus(self, client_id):
        try:
            query= """
            SELECT * FROM MENUS WHERE USER_ID= {}
            """.format(client_id)
            self.cursor.execute(query)
            menus = self.cursor.fetchall()
            return menus
        except Exception as error:
            return str(error)

    def get_all_single_menus(self, menu_id):
        try:
            query= "SELECT * FROM MENUS WHERE ID= {}".format(menu_id)
            self.cursor.execute(query)
            menu = self.cursor.fetchall()
            return menu
        except Exception as error:
            return str(error)

    def get_all_menus(self):
        try:
            query= "SELECT * FROM MENUS"
            self.cursor.execute(query)
            menus = self.cursor.fetchall()
            return menus
        except Exception as error:
            return str(error)
