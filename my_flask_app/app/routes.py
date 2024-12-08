# routes.py
from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import jwt_required
import app.auth as auth

# 创建 Blueprint 对象
routes_bp = Blueprint('routes', __name__)

# 路由：首页
@routes_bp.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

# 路由：注册
@routes_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return auth.register()
    return render_template('register.html')

# 路由：登录
@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return auth.login()
    return render_template('login.html')

# 路由：修改密码
@routes_bp.route('/change-password', methods=['GET', 'POST'])
@jwt_required()
def change_password():
    if request.method == 'POST':
        return auth.change_password()
    return render_template('change_password.html')

# 路由：删除用户
@routes_bp.route('/delete-user', methods=['GET', 'POST'])
@jwt_required()
def delete_user():
    if request.method == 'POST':
        return auth.delete_user()
    return render_template('delete_user.html')

# 路由：受保护的页面
@routes_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return render_template('protected.html')
