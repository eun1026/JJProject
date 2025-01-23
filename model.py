import mysql.connector
from datetime import datetime

class DBManager:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",  # 본인 MySQL 계정
            password="1234",  # 본인 MySQL 비밀번호
            database="board_db2"
        )
        self.cursor = self.connection.cursor()

    def create_user(self, username, password):
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        self.cursor.execute(query, (username, password))
        self.connection.commit()

    def get_user_by_username(self, username):
        query = "SELECT * FROM users WHERE username = %s"
        self.cursor.execute(query, (username,))
        return self.cursor.fetchone()

    def get_user_by_credentials(self, username, password):
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        return self.cursor.fetchone()

    def create_goal(self, user_id, name, amount, deadline, cycle):
        query = """INSERT INTO goals (user_id, name, amount, deadline, savings_cycle)
                   VALUES (%s, %s, %s, %s, %s)"""
        self.cursor.execute(query, (user_id, name, amount, deadline, cycle))
        self.connection.commit()

    def get_goals_by_user_id(self, user_id):
        query = "SELECT * FROM goals WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()
