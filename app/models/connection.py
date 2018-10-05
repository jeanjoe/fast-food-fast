"""Databse connection condig"""
import psycopg2
from psycopg2.extensions import AsIs
from psycopg2.extras import RealDictCursor
from app import app
from config import DevelopmentConfig

app.config.from_object(DevelopmentConfig)

class DatabaseConnection:

    def __init__(self):
        self.connection = psycopg2.connect(
            database=app.config['DB_NAME'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASS'],
            host=app.config['DB_HOST'],
            port=app.config['DB_PORT']
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        self.dict_cursor = self.connection.cursor(cursor_factory=RealDictCursor)

    def select_single_column(self, table, field, value):
        """Search specified table column with the value."""
        query = "SELECT * FROM %s WHERE %s = %s"
        self.dict_cursor.execute(query, (AsIs(table), AsIs(field), value))
        return self.dict_cursor.fetchall()