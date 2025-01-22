from flask import Flask, render_template, request, redirect, url_for, session, flash
from model import DBManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 세션을 위한 비밀 키

# 데이터베이스 연결 객체 생성
db_manager = DBManager()

# 홈 화면 (첫 화면)
@app.route('/')
def home():
    return render_template('home.html')

# 회원가입 화면
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # 중복된 사용자 확인
        if db_manager.get_user_by_username(username):
            flash('이미 존재하는 사용자입니다.')
            return redirect(url_for('signup'))
        
        # 새 사용자 저장
        db_manager.create_user(username, password)
        flash('회원가입 성공!')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

# 로그인 화면
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # 사용자 로그인 확인
        user = db_manager.get_user_by_credentials(username, password)
        if user:
            session['user_id'] = user[0]  # 사용자 ID는 첫 번째 컬럼에 있음
            flash('로그인 성공!')
            return redirect(url_for('goal_list'))
        else:
            flash('아이디 또는 비밀번호가 틀렸습니다.')
    
    return render_template('login.html')

# 저축 목표 설정 화면
@app.route('/goal', methods=['GET', 'POST'])
def goal():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # 로그인하지 않은 경우 로그인 화면으로 이동
    
    if request.method == 'POST':
        name = request.form['goal_name']
        amount = request.form['goal_amount']
        deadline = request.form['goal_deadline']
        cycle = request.form['goal_savings_cycle']
        
        # 목표 저장
        db_manager.create_goal(session['user_id'], name, amount, deadline, cycle)
        flash('저축 목표가 저장되었습니다.')
        return redirect(url_for('goal_list'))
    
    return render_template('goal.html')

# 저축 목표 목록 화면
@app.route('/goal_list')
def goal_list():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # 로그인하지 않은 경우 로그인 화면으로 이동
    
    goals = db_manager.get_goals_by_user_id(session['user_id'])
    return render_template('goal_list.html', goals=goals)

# 애플리케이션 실행
if __name__ == '__main__':
    app.run(debug=True)
