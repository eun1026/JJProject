import mysql.connector
import datetime

# DB 연결 설정
def get_db_connection():
    return mysql.connector.connect(
        host="13.125.124.41",  # DB 호스트
        user="root",       # DB 사용자명
        password="1234",  # DB 비밀번호
        database="savings_db"  # 사용하고 있는 DB 이름
    )

# 모든 거래 내역 가져오기
def get_all_transactions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # 딕셔너리 형식으로 반환
    cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
    transactions = cursor.fetchall()
    
    # 날짜를 문자열에서 datetime 객체로 변환
    for transaction in transactions:
        transaction['date'] = transaction['date']  # 여기에서 날짜를 처리 (MySQL에서 날짜 형식이면 문제없음)
    
    cursor.close()
    conn.close()
    return transactions
