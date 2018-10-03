from app.models.connection import DatabaseConnection

class Migration(DatabaseConnection):
    """Create Database tables."""
    def __init__(self):
        super().__init__()

    def create_tables(self):
        """Create Database Tables."""
        try:
            query = [
            """
            CREATE TABLE IF NOT EXISTS USERS (
                ID SERIAL PRIMARY KEY,
                FIRST_NAME VARCHAR(50) NOT NULL,
                LAST_NAME VARCHAR(50) NOT NULL,
                EMAIL VARCHAR(50) NOT NULL UNIQUE,
                PHONE VARCHAR(20) NULL,
                ACCOUNT_TYPE VARCHAR(50) NOT NULL, 
                PASSWORD VARCHAR(191) NOT NULL,
                CREATED_AT TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS MENUS (
                ID SERIAL PRIMARY KEY,  
                ADMIN_ID INT NOT NULL,
                FOREIGN KEY (ADMIN_ID) REFERENCES USERS (ID),
                TITLE VARCHAR(100) NOT NULL, 
                PRICE INT NOT NULL,
                DESCRIPTION TEXT,
                STATUS BOOLEAN DEFAULT TRUE,
                CREATED_AT TIMESTAMP 
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS ORDERS (
                ID SERIAL PRIMARY KEY,  
                MENU_ID INT NOT NULL,
                FOREIGN KEY (MENU_ID) REFERENCES MENUS (ID),
                USER_ID INT NOT NULL,
                FOREIGN KEY (USER_ID) REFERENCES USERS (ID),
                LOCATION VARCHAR(50) NOT NULL, 
                QUANTITY INT NOT NULL,
                APPROVED_AT TIMESTAMP DEFAULT NULL,
                APPROVED_BY INT NULL,
                STATUS VARCHAR(50) NOT NULL,
                FOREIGN KEY (APPROVED_BY) REFERENCES USERS (ID),
                CREATED_AT TIMESTAMP 
            )
            """
            ]
            for query in query:
                self.cursor.execute(query)

            return True
                
        except Exception as error:
            return str(error)

    def drop_table(self, tables=list):
        """Drop list of tables."""
        for table in tables:
            query = """
            DROP TABLE IF EXISTS {0} CASCADE
            """.format(table)
            self.cursor.execute(query)
        self.connection.close()
        return True
    
    def truncate_tables(self, tables=list):
        """Truncate tables."""
        for table in tables:
            query = """TRUNCATE TABLE {} CASCADE""".format(table)
            self.cursor.execute(query)
        return True
