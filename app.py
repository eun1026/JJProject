from flask import Flask, render_template, request, redirect, url_for, flash
import model
import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# 기본 페이지 (수입/지출 내역 목록)
@app.route('/')
def index():
    transactions = model.get_all_transactions()  # 데이터베이스에서 모든 거래 내역 가져오기
    
    # 이번 달의 첫 날짜와 마지막 날짜 계산
    today = datetime.date.today()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = today.replace(day=28) + datetime.timedelta(days=4)  # 28일에 4일을 더해 마지막 날을 추정
    last_day_of_month = last_day_of_month - datetime.timedelta(days=last_day_of_month.day)

    # 이번 달 수입 계산
    monthly_income = sum(
        transaction['amount'] for transaction in transactions 
        if transaction['transaction_type'] == 'income' and first_day_of_month <= transaction['date'] <= last_day_of_month
    )
    
    # 이번 달 지출 계산
    monthly_expense = sum(
        transaction['amount'] for transaction in transactions 
        if transaction['transaction_type'] == 'expense' and first_day_of_month <= transaction['date'] <= last_day_of_month
    )
    
    # 남은 돈 계산 (총 수입 - 총 지출)
    remaining_balance = monthly_income - monthly_expense
    
    return render_template('index.html', transactions=transactions, monthly_income=monthly_income, monthly_expense=monthly_expense, remaining_balance=remaining_balance)

# 내역 추가 페이지
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        category = request.form['category']
        description = request.form['description']
        amount = request.form['amount']
        date = request.form['date']
        transaction_type = request.form['transaction_type']
        
        # 데이터베이스에 내역 추가
        model.add_transaction(category, description, amount, date, transaction_type)
        
        flash('내역이 추가되었습니다.', 'success')
        return redirect(url_for('index'))
    
    return render_template('add.html')

# 내역 수정 페이지
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    transaction = model.get_transaction(id)
    
    if request.method == 'POST':
        category = request.form['category']
        description = request.form['description']
        amount = request.form['amount']
        date = request.form['date']
        transaction_type = request.form['transaction_type']
        
        model.update_transaction(id, category, description, amount, date, transaction_type)
        flash('내역이 수정되었습니다.', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit.html', transaction=transaction)

# 내역 삭제
@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    model.delete_transaction(id)
    flash('내역이 삭제되었습니다.', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
