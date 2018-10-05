"""Manage admin Menu."""
from datetime import datetime
from app.models.connection import DatabaseConnection

class MenuModel(DatabaseConnection):
    """manage Database."""
    def add_menu(self, admin_id, title, description, price):
        """Admin Adds to menu."""
        query = """
        INSERT INTO MENUS (admin_id, title, description, price, status, created_at) VALUES
        (%s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (admin_id, title, description, price, True, str(datetime.now())))
        return "Menu added Successfully"

    def get_all_client_menus(self, client_id):
        """Get all client menus."""
        query = """SELECT * FROM MENUS WHERE USER_ID= %s"""
        self.dict_cursor.execute(query, (client_id,))
        menus = self.dict_cursor.fetchall()
        return menus

    def get_all_single_menu(self, menu_id):
        """Get a single menu."""
        query = "SELECT * FROM MENUS WHERE ID= %s"
        self.dict_cursor.execute(query, (menu_id,))
        menu = self.dict_cursor.fetchall()
        return menu

    def get_all_menus(self):
        """Get all the menus"""
        query = "SELECT * FROM MENUS"
        self.dict_cursor.execute(query)
        menus = self.dict_cursor.fetchall()
        return menus
