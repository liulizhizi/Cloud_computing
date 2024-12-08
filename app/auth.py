# auth.py
from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from app.models import db, User

bcrypt = Bcrypt()

def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # 检查用户是否已存在
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify(message="User already exists"), 400

    # 密码加密
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # 创建新用户
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    try:
        db.session.commit()
        return jsonify(message="User registered successfully"), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify(message="Username already taken"), 400

def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # 查找用户
    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        # 登录成功，生成 JWT token
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message="Invalid credentials"), 401

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
