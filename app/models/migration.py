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
            CREATE TABLE IF NOT EXISTS ADMINS (
                ID SERIAL PRIMARY KEY,
                FIRSTNAME VARCHAR(50) NOT NULL,
                LASTNAME VARCHAR(50) NOT NULL,
                EMAIL VARCHAR(100) NOT NULL,
                PASSWORD VARCHAR(100) NOT NULL,
                CREATED_AT TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS USERS (
                ID SERIAL PRIMARY KEY,
                FIRST_NAME VARCHAR(50) NOT NULL,
                LAST_NAME VARCHAR(50) NOT NULL,
                EMAIL VARCHAR(50) NOT NULL UNIQUE,
                PHONE VARCHAR(20) NULL,
                PASSWORD VARCHAR(191) NOT NULL,
                CREATED_AT TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS MENUS (
                ID SERIAL PRIMARY KEY,  
                ADMIN_ID INT NOT NULL,
                FOREIGN KEY (ADMIN_ID) REFERENCES ADMINS (ID),
                TITLE VARCHAR(100) NOT NULL, 
                PRICE INT NOT NULL,
                DESCRIPTION TEXT,
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
                APROVED_AT TIMESTAMP DEFAULT NULL,
                APPROVED_BY INT NULL,
                STATUS VARCHAR(50) NOT NULL,
                FOREIGN KEY (APPROVED_BY) REFERENCES ADMINS (ID),
                CREATED_AT TIMESTAMP 
            )
            """
            ]
            for query in query:
                self.cursor.execute(query)
                # print("Table {0} migrated successfuly.".format(query.split()[2].strip()))
        except Exception as error:
            print("Error while migrating table => {}".format(str(error)))
        finally:
            self.connection.close()

    def drop_table(self, tables=list):
        """Drop list of tables."""
        for table in tables:
            try:
                query = """
                DROP TABLE IF EXISTS {0} CASCADE
                """.format(table)
                self.cursor.execute(query)
                print("Table {0} dropped successfuly".format(table))
            except Exception as error:
                print("Error while dropping table {0} => {1}".format(table, str(error)))
        self.connection.close()
