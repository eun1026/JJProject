from flask import Flask, render_template, request, redirect, url_for, flash
import model

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # flash 메시지에 필요한 비밀 키 설정

# 홈 페이지
@app.route('/')
def home():
    life_transactions = model.get_all_transactions('life')
    event_transactions = model.get_all_transactions('event')
    goal_transactions = model.get_all_transactions('goal')
    save_transactions = model.get_all_transactions('save')
    
    return render_template('home.html', 
                           life_transactions=life_transactions, 
                           event_transactions=event_transactions,
                           goal_transactions=goal_transactions,
                           save_transactions=save_transactions)

# 카테고리 관리 페이지
@app.route('/index')
def index():
    return render_template('index.html')

# 생활 관리 페이지
@app.route('/life')
def life():
    transactions = model.get_all_transactions('life')
    return render_template('life.html', transactions=transactions)

# 이벤트 관리 페이지
@app.route('/event')
def event():
    transactions = model.get_all_transactions('event')
    return render_template('event.html', transactions=transactions)

# 목표 관리 페이지
@app.route('/goal')
def goal():
    transactions = model.get_all_transactions('goal')
    return render_template('goal.html', transactions=transactions)

# 저축 관리 페이지
@app.route('/save')
def save():
    transactions = model.get_all_transactions('save')
    return render_template('save.html', transactions=transactions)

# 새로운 항목 추가 페이지
@app.route('/add/<category>', methods=['GET', 'POST'])
def add(category):
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        date = request.form['date']

        model.add_transaction(category, description, amount, date, 'expense')  # 'expense'는 예시입니다
        flash("새로운 항목이 성공적으로 추가되었습니다.", "success")
        return redirect(url_for(category))  # 해당 카테고리 페이지로 리다이렉트
    
    return render_template('add.html', category=category)

# 수정 페이지
@app.route('/edit/<category>/<int:transaction_id>', methods=['GET', 'POST'])
def edit(category, transaction_id):
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        date = request.form['date']

        model.edit_transaction(category, transaction_id, description, amount, date, 'expense')
        flash("항목이 수정되었습니다.", "success")
        return redirect(url_for(category))

    transaction = model.get_all_transactions(category)
    transaction = next((item for item in transaction if item['id'] == transaction_id), None)
    
    return render_template('edit.html', category=category, transaction=transaction)

# 삭제 기능
@app.route('/delete/<category>/<int:transaction_id>', methods=['GET'])
def delete(category, transaction_id):
    model.delete_transaction(category, transaction_id)
    flash("항목이 삭제되었습니다.", "error")
    return redirect(url_for(category))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
