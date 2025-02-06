import mysql.connector

# MySQL 연결 함수
def get_db_connection():
    connection = mysql.connector.connect(
        host='13.125.124.41',  # MySQL 서버 주소
        user='root',       # MySQL 사용자 이름
        password='1234',  # MySQL 비밀번호
        database='savings_db'   # 사용할 데이터베이스 이름
    )
    return connection

# 카테고리별 모든 트랜잭션을 가져오는 함수
def get_all_transactions(category):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    query = f"SELECT * FROM {category} ORDER BY date DESC"
    cursor.execute(query)
    transactions = cursor.fetchall()

    cursor.close()
    connection.close()
    
    return transactions

# 트랜잭션 추가 함수
def add_transaction(category, description, amount, date, transaction_type):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    query = f"INSERT INTO {category} (description, amount, date, transaction_type) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (description, amount, date, transaction_type))
    
    connection.commit()
    cursor.close()
    connection.close()

# 트랜잭션 수정 함수
def edit_transaction(category, transaction_id, description, amount, date, transaction_type):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    query = f"UPDATE {category} SET description = %s, amount = %s, date = %s, transaction_type = %s WHERE id = %s"
    cursor.execute(query, (description, amount, date, transaction_type, transaction_id))
    
    connection.commit()
    cursor.close()
    connection.close()

# 트랜잭션 삭제 함수
def delete_transaction(category, transaction_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    query = f"DELETE FROM {category} WHERE id = %s"
    cursor.execute(query, (transaction_id,))
    
    connection.commit()
    cursor.close()
    connection.close()
