from app.models.connection import DatabaseConnection
from datetime import datetime

class MenuModel(DatabaseConnection):

    def __init__(self):
        super().__init__()

    def add_menu(self, admin_id, title, description, price):
        try:
            query= """
            INSERT INTO MENUS (admin_id, title, description, price, status, created_at) VALUES
            ({}, '{}', '{}', {}, {}, '{}')
            """.format(admin_id, title, description, price, True, str(datetime.now()))
            self.cursor.execute(query)
            return "Data Inserted Successfully"
        except Exception as error:
            print(str(error))
            return "Unable to save error {} ".format(str(error))

    def get_all_client_menus(self, client_id):
        try:
            query= """
            SELECT * FROM MENUS WHERE USER_ID= {}
            """.format(client_id)
            self.dict_cursor.execute(query)
            menus = self.dict_cursor.fetchall()
            return menus
        except Exception as error:
            return str(error)

    def get_all_single_menu(self, menu_id):
        try:
            query= "SELECT * FROM MENUS WHERE ID= {}".format(menu_id)
            self.dict_cursor.execute(query)
            menu = self.dict_cursor.fetchall()
            return menu
        except Exception as error:
            return str(error)

    def get_all_menus(self):
        try:
            query= "SELECT * FROM MENUS"
            self.dict_cursor.execute(query)
            menus = self.dict_cursor.fetchall()
            return menus
        except Exception as error:
            return str(error)
