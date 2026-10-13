import os
import pymysql
from dotenv import load_dotenv

load_dotenv()


class MySQLConnection:
    def __init__(self, db):
        self.connection = pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", db),
            port=int(os.getenv("DB_PORT", "3306")),
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, data or {})
            if query.strip().upper().startswith("SELECT"):
                return list(cursor.fetchall())
            if query.strip().upper().startswith("INSERT"):
                return cursor.lastrowid
            return cursor.rowcount


def connectToMySQL(db):
    return MySQLConnection(db)
