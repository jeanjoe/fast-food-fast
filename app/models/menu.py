from app.models.connection import DatabaseConnection
from datetime import datetime

class MenuModel(DatabaseConnection):

    def __init__(self):
        super().__init__()

    def add_menu(self, admin_id, title, description, price):
        query= """
        INSERT INTO MENUS (admin_id, title, description, price, status, created_at) VALUES
        (%s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (admin_id, title, description, price, True, str(datetime.now())))
        return "Menu added Successfully"

    def get_all_client_menus(self, client_id):
        query= """SELECT * FROM MENUS WHERE USER_ID= %s"""
        self.dict_cursor.execute(query, (client_id,))
        menus = self.dict_cursor.fetchall()
        return menus

    def get_all_single_menu(self, menu_id):
        query= "SELECT * FROM MENUS WHERE ID= %s"
        self.dict_cursor.execute(query, (menu_id,))
        menu = self.dict_cursor.fetchall()
        return menu

    def get_all_menus(self):
        query= "SELECT * FROM MENUS"
        self.dict_cursor.execute(query)
        menus = self.dict_cursor.fetchall()
        return menus
