import psycopg2
from app.view import app

app.config.from_object('config')

class DatabaseConnection:

    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                database=app.config['DB_NAME'],
                user=app.config['DB_USER'],
                password=app.config['DB_PASS'],
                host=app.config['DB_HOST'],
                port=app.config['DB_PORT']
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            
        except Exception as identifier:
            print(identifier)