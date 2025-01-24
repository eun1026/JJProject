import mysql.connector
from datetime import datetime

class DBManager:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="board_db2"
        )
        self.cursor = self.connection.cursor(dictionary=True)

    # 로그인 처리
    def login_user(self, username, password):
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        user = self.cursor.fetchone()
        return user

    # 회원가입 처리
    def register_user(self, username, password):
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        self.cursor.execute(query, (username, password))
        self.connection.commit()

    # 사용자 트랜잭션 목록 가져오기
    def get_transactions(self, user_id):
        query = "SELECT * FROM transactions WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        transactions = self.cursor.fetchall()
        return transactions

    # 트랜잭션 추가
    def add_transaction(self, description, amount, user_id):
        query = "INSERT INTO transactions (description, amount, user_id, created_at) VALUES (%s, %s, %s, %s)"
        created_at = datetime.now()
        self.cursor.execute(query, (description, amount, user_id, created_at))
        self.connection.commit()

    # 트랜잭션 수정
    def update_transaction(self, transaction_id, description, amount):
        query = "UPDATE transactions SET description = %s, amount = %s WHERE id = %s"
        self.cursor.execute(query, (description, amount, transaction_id))
        self.connection.commit()

    # 트랜잭션 삭제
    def delete_transaction(self, transaction_id):
        query = "DELETE FROM transactions WHERE id = %s"
        self.cursor.execute(query, (transaction_id,))
        self.connection.commit()

    # 트랜잭션 단건 조회
    def get_transaction(self, transaction_id):
        query = "SELECT * FROM transactions WHERE id = %s"
        self.cursor.execute(query, (transaction_id,))
        return self.cursor.fetchone()
