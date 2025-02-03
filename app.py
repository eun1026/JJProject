from flask import Flask, render_template, request, redirect, url_for, session, flash
from model import DBManager
from datetime import datetime

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'your_secret_key'  # 세션 보안 키

# MySQL 접속 객체 초기화
manager = DBManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # 로그인 체크
        user = manager.login_user(username, password)
        if user:
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # 회원가입
        manager.register_user(username, password)
        flash('Registration successful! You can now login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    transactions = manager.get_transactions(session['user_id'])
    return render_template('dashboard.html', transactions=transactions)

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        user_id = session['user_id']
        
        manager.add_transaction(description, amount, user_id)
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_transaction.html')

@app.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    transaction = manager.get_transaction(transaction_id)
    
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        
        manager.update_transaction(transaction_id, description, amount)
        flash('Transaction updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('edit_transaction.html', transaction=transaction)

@app.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    manager.delete_transaction(transaction_id)
    flash('Transaction deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/statistics')
def statistics():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('statistics.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
