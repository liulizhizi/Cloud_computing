# auth.py
from flask import request, jsonify,redirect,url_for,flash,session,render_template
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from app.models import db, User
from functools import wraps

bcrypt = Bcrypt()



def register():
    # data = request.get_json()
    username = request.form['username']
    password = request.form['password']

    # 检查用户是否已存在
    user = User.query.filter_by(username=username).first()
    if user:
        flash("User already exists")
        return redirect(url_for('routes.register'))

    # 密码加密
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # 创建新用户
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    try:
        db.session.commit()
        return redirect(url_for('routes.home'))
    except IntegrityError:
        # db.session.rollback()
        message="Username already taken"
        flash(message)
        return redirect(url_for('routes.register'))

def login():
    # data = request.get_json()
    username = request.form['username']
    password = request.form['password']

    # 查找用户
    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        # 登录成功，生成 JWT token
        # access_token = create_access_token(identity=username)
        session['logged_in'] = True
        session['username'] = user.username
        return redirect(url_for('routes.home'))
    else:
        flash("Invalid credentials")
        return redirect(url_for('routes.login'))

def change_password():
    data = request.get_json()
    new_password = data['new_password']
    username = data['username']

    user = User.query.filter_by(username=username).first()
    if user:
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        return jsonify(message="Password updated successfully"), 200
    else:
        return jsonify(message="User not found"), 404

def delete_user():
    data = request.get_json()
    username = data['username']

    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(message="User deleted successfully"), 200
    else:
        return jsonify(message="User not found"), 404
    

