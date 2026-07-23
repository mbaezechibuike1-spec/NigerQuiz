from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import hashlib

# Don't import from app - use direct imports
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

# These will be set by app.py
db = None
User = None
Question = None
WithdrawRequest = None
Season = None

def init_admin(app_db, app_user, app_question, app_withdraw, app_season):
    global db, User, Question, WithdrawRequest, Season
    db = app_db
    User = app_user
    Question = app_question
    WithdrawRequest = app_withdraw
    Season = app_season

def is_admin():
    return session.get('is_admin', False)

# ============ ADMIN ROUTES ============

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['is_admin'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            return render_template('admin_login.html', error='Invalid credentials!')
    
    return render_template('admin_login.html')

@admin_bp.route('/logout')
def logout():
    session.pop('is_admin', None)
    return redirect(url_for('admin.login'))

@admin_bp.route('/')
def dashboard():
    if not is_admin():
        return redirect(url_for('admin.login'))
    
    total_users = User.query.count()
    total_questions = Question.query.count()
    total_withdrawals = WithdrawRequest.query.count()
    pending_withdrawals = WithdrawRequest.query.filter_by(status='pending').count()
    
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    recent_withdrawals = WithdrawRequest.query.order_by(WithdrawRequest.created_at.desc()).limit(10).all()
    
    return render_template('admin_dashboard.html',
        total_users=total_users,
        total_questions=total_questions,
        total_withdrawals=total_withdrawals,
        pending_withdrawals=pending_withdrawals,
        recent_users=recent_users,
        recent_withdrawals=recent_withdrawals
    )

@admin_bp.route('/users')
def users():
    if not is_admin():
        return redirect(url_for('admin.login'))
    all_users = User.query.order_by(User.score.desc()).all()
    return render_template('admin_users.html', users=all_users)

@admin_bp.route('/questions')
def questions():
    if not is_admin():
        return redirect(url_for('admin.login'))
    all_questions = Question.query.order_by(Question.level).all()
    return render_template('admin_questions.html', questions=all_questions)

@admin_bp.route('/questions/add', methods=['GET', 'POST'])
def add_question():
    if not is_admin():
        return redirect(url_for('admin.login'))
    
    if request.method == 'POST':
        q = Question(
            question=request.form.get('question'),
            option_a=request.form.get('option_a'),
            option_b=request.form.get('option_b'),
            option_c=request.form.get('option_c'),
            option_d=request.form.get('option_d'),
            correct_answer=request.form.get('correct_answer'),
            level=int(request.form.get('level', 1))
        )
        db.session.add(q)
        db.session.commit()
        return jsonify({'success': True})
    
    return render_template('admin_add_question.html')

@admin_bp.route('/questions/delete/<int:q_id>', methods=['POST'])
def delete_question(q_id):
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 401
    
    q = Question.query.get(q_id)
    if q:
        db.session.delete(q)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'error': 'Not found'}), 404

@admin_bp.route('/withdrawals')
def withdrawals():
    if not is_admin():
        return redirect(url_for('admin.login'))
    all_withdrawals = WithdrawRequest.query.order_by(WithdrawRequest.created_at.desc()).all()
    return render_template('admin_withdrawals.html', withdrawals=all_withdrawals)

@admin_bp.route('/withdrawals/approve/<int:w_id>', methods=['POST'])
def approve_withdrawal(w_id):
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 401
    
    w = WithdrawRequest.query.get(w_id)
    if w:
        w.status = 'approved'
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'error': 'Not found'}), 404

@admin_bp.route('/withdrawals/reject/<int:w_id>', methods=['POST'])
def reject_withdrawal(w_id):
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 401
    
    w = WithdrawRequest.query.get(w_id)
    if w:
        w.status = 'rejected'
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'error': 'Not found'}), 404

@admin_bp.route('/stats')
def stats():
    if not is_admin():
        return redirect(url_for('admin.login'))
    
    ranks = {}
    for r in ['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Grand Master', 'Elite Master']:
        ranks[r] = User.query.filter_by(rank=r).count()
    
    return render_template('admin_stats.html',
        total_users=User.query.count(),
        total_questions=Question.query.count(),
        total_withdrawals=WithdrawRequest.query.count(),
        pending_withdrawals=WithdrawRequest.query.filter_by(status='pending').count(),
        approved_withdrawals=WithdrawRequest.query.filter_by(status='approved').count(),
        rejected_withdrawals=WithdrawRequest.query.filter_by(status='rejected').count(),
        ranks=ranks
    )
