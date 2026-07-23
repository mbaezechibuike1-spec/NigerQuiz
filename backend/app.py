from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta
import os
import json
import random
import hashlib
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'niger-quiz-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

CORS(app)
db = SQLAlchemy(app)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ============ MODELS ============

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    profile_pic = db.Column(db.String(200), default='default.png')
    score = db.Column(db.Integer, default=0)
    rank = db.Column(db.String(50), default='Bronze')
    level = db.Column(db.Integer, default=1)
    season_score = db.Column(db.Integer, default=0)
    total_seasons = db.Column(db.Integer, default=0)
    has_claimed_200 = db.Column(db.Boolean, default=False)
    has_claimed_100k = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(200), nullable=False)
    option_b = db.Column(db.String(200), nullable=False)
    option_c = db.Column(db.String(200), nullable=False)
    option_d = db.Column(db.String(200), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)
    level = db.Column(db.Integer, default=1)

class WithdrawRequest(db.Model):
    __tablename__ = 'withdraws'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    username = db.Column(db.String(80))
    amount = db.Column(db.Integer)
    account_name = db.Column(db.String(100))
    account_number = db.Column(db.String(20))
    bank_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Season(db.Model):
    __tablename__ = 'seasons'
    id = db.Column(db.Integer, primary_key=True)
    season_number = db.Column(db.Integer, unique=True)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

# ============ CREATE TABLES ============

with app.app_context():
    db.create_all()
    print("✅ Database created successfully!")

# ============ IMPORT ADMIN AFTER MODELS ============

try:
    from admin import admin_bp, init_admin
    init_admin(db, User, Question, WithdrawRequest, Season)
    app.register_blueprint(admin_bp)
    print("✅ Admin panel loaded!")
except ImportError:
    print("⚠️ Admin panel not loaded (admin.py not found)")

# ============ HELPERS ============

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return get_user_by_id(user_id)
    return None

def calculate_rank(score):
    if score >= 100000:
        return 'Elite Master'
    elif score >= 50000:
        return 'Grand Master'
    elif score >= 25000:
        return 'Diamond'
    elif score >= 10000:
        return 'Platinum'
    elif score >= 5000:
        return 'Gold'
    elif score >= 2000:
        return 'Silver'
    elif score >= 500:
        return 'Bronze'
    return 'Bronze'

# ============ ROUTES ============

@app.route('/')
def index():
    import sqlite3
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    
    # Get question count
    cursor.execute('SELECT COUNT(*) FROM questions')
    question_count = cursor.fetchone()[0]
    
    # Get total users (if table exists)
    try:
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
    except:
        total_users = 0
    
    conn.close()
    
    # Active players (simulate if no users yet)
    active_players = max(1, total_users + 5)  # Show at least 5 active players
    
    return render_template('index.html', 
        question_count=question_count,
        player_count=active_players,
        total_users=total_users)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    hashed_password = hashlib.sha256(data['password'].encode()).hexdigest()
    new_user = User(
        username=data['username'],
        email=data['email'],
        phone=data['phone'],
        country=data['country'],
        password=hashed_password,
        profile_pic='default.png'
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Registration successful!'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user:
        hashed_password = hashlib.sha256(data['password'].encode()).hexdigest()
        if user.password == hashed_password:
            session['user_id'] = user.id
            session['username'] = user.username
            return jsonify({'success': True, 'user': user.username, 'rank': user.rank})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    if not user:
        return redirect(url_for('index'))
    return render_template('dashboard.html', user=user)

@app.route('/profile')
def profile():
    user = get_current_user()
    if not user:
        return redirect(url_for('index'))
    return render_template('profile.html', user=user)

@app.route('/profile/<username>')
def view_profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return render_template('profile.html', user=user, view_only=True)

@app.route('/api/profile', methods=['GET'])
def api_profile():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not logged in'}), 401
    return jsonify({
        'username': user.username,
        'email': user.email,
        'phone': user.phone,
        'country': user.country,
        'profile_pic': user.profile_pic,
        'score': user.score,
        'rank': user.rank,
        'level': user.level
    })

@app.route('/api/profile/update', methods=['POST'])
def update_profile():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not logged in'}), 401
    data = request.json
    if 'email' in data:
        user.email = data['email']
    if 'phone' in data:
        user.phone = data['phone']
    if 'country' in data:
        user.country = data['country']
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/upload_profile_pic', methods=['POST'])
def upload_profile_pic():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not logged in'}), 401
    if 'profile_pic' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['profile_pic']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    filename = f"user_{user.id}_{datetime.utcnow().timestamp()}.{file.filename.rsplit('.', 1)[1].lower()}"
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    user.profile_pic = filename
    db.session.commit()
    return jsonify({'success': True, 'filename': filename})

@app.route('/quiz')
def quiz():
    if not get_current_user():
        return redirect(url_for('index'))
    return render_template('quiz.html')

@app.route('/api/questions/<int:count>')
def get_questions(count):
    if count > 50:
        count = 50
    questions = Question.query.order_by(db.func.random()).limit(count).all()
    return jsonify([{
        'id': q.id,
        'question': q.question,
        'options': [q.option_a, q.option_b, q.option_c, q.option_d],
        'correct': q.correct_answer,
        'level': q.level
    } for q in questions])

@app.route('/api/submit_quiz', methods=['POST'])
def submit_quiz():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Please login first'}), 401
    data = request.json
    score = data.get('score', 0)
    user.score += score
    user.season_score += score
    user.rank = calculate_rank(user.score)
    user.level = max(1, user.score // 1000)
    db.session.commit()
    response = {'score': score, 'new_total': user.score, 'rank': user.rank, 'level': user.level, 'eligible': False}
    if user.score >= 100000 and not user.has_claimed_100k:
        response['eligible'] = True
        response['amount'] = 100000
    elif user.score >= 200 and not user.has_claimed_200:
        response['eligible'] = True
        response['amount'] = 10000
    return jsonify(response)

@app.route('/api/leaderboard')
def leaderboard():
    top_users = User.query.order_by(User.score.desc()).limit(100).all()
    return jsonify([{
        'username': u.username,
        'score': u.score,
        'rank': u.rank,
        'level': u.level,
        'profile_pic': u.profile_pic,
        'country': u.country
    } for u in top_users])

@app.route('/api/withdraw', methods=['POST'])
def withdraw():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Please login'}), 401
    data = request.json
    amount = data.get('amount', 0)
    if amount == 100000 and user.score >= 100000 and not user.has_claimed_100k:
        user.has_claimed_100k = True
    elif amount == 10000 and user.score >= 200 and not user.has_claimed_200:
        user.has_claimed_200 = True
    else:
        return jsonify({'error': 'Not eligible'}), 400
    w = WithdrawRequest(
        user_id=user.id, username=user.username, amount=amount,
        account_name=data.get('account_name'), account_number=data.get('account_number'),
        bank_name=data.get('bank_name'), phone=data.get('phone')
    )
    db.session.add(w)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/withdrawals')
def get_withdrawals():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not logged in'}), 401
    withdrawals = WithdrawRequest.query.filter_by(user_id=user.id).order_by(WithdrawRequest.created_at.desc()).all()
    return jsonify([{
        'amount': w.amount, 'status': w.status,
        'date': w.created_at.strftime('%Y-%m-%d %H:%M'),
        'account_name': w.account_name, 'bank_name': w.bank_name
    } for w in withdrawals])

@app.route('/api/season')
def get_season():
    current_season = Season.query.filter_by(is_active=True).first()
    if not current_season:
        season_number = Season.query.count() + 1
        current_season = Season(season_number=season_number, end_date=datetime.utcnow() + timedelta(days=90))
        db.session.add(current_season)
        db.session.commit()
    time_left = current_season.end_date - datetime.utcnow()
    return jsonify({
        'season': current_season.season_number,
        'days': time_left.days,
        'hours': time_left.seconds // 3600,
        'minutes': (time_left.seconds % 3600) // 60,
        'is_active': current_season.is_active
    })

@app.route('/api/user/<username>')
def get_user_profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({
        'username': user.username, 'country': user.country,
        'profile_pic': user.profile_pic, 'score': user.score,
        'rank': user.rank, 'level': user.level,
        'total_seasons': user.total_seasons,
        'joined': user.created_at.strftime('%B %Y') if user.created_at else 'N/A'
    })

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("✅ Database initialized!")
    
    # Get question count
    with app.app_context():
        count = Question.query.count()
        print(f"📊 Total questions: {count}")
    
    print("🚀 Starting Niger Quiz Server...")
    print("🌐 Open http://localhost:5000 in your browser")
    app.run(host='0.0.0.0', port=5000, debug=True)
