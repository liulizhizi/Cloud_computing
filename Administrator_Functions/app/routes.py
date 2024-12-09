# routes.py
from flask import Blueprint, render_template, request, jsonify, redirect
from flask_jwt_extended import get_jwt_identity, jwt_required, current_user
import app.auth as auth
from app.models import User, db, AccessRecord, Role

# 创建 Blueprint 对象
routes_bp = Blueprint('routes', __name__)

# 首页
@routes_bp.route('/', methods=['GET'])
@routes_bp.route('/home', methods=['GET'])
@jwt_required(optional=True)
def home():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    # 如果是管理员用户，跳到管理员页面，如果不需要可以注释掉
    if user and user.role.admin:
        # 重定向到admin_home
        return redirect('/admin_home')

    user_id = None
    if user:
        user_id = user.id
    # 添加访问记录，如果没有user_id，则为匿名用户
    access_record = AccessRecord(user_id=user_id)
    db.session.add(access_record)
    db.session.commit()

    return render_template('home.html')


# 路由：首页
# @routes_bp.route('/home', methods=['GET'])
# def home():
#     return render_template('home.html')

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



# 添加用户角色
@routes_bp.route('/add-role', methods=['POST'])
def add_role():
    data = request.get_json()
    name = data.get('name')
    admin = data.get('admin')
    new_role = Role(name=name, admin=admin)
    db.session.add(new_role)
    db.session.commit()
    return jsonify(message="Role added successfully"), 201


# 管理员首页（查询记录接口）
@routes_bp.route('/admin_home', methods=['GET'])
@jwt_required(optional=True)
def admin_home():
    current_user = get_jwt_identity()  # 获取身份信息

    user = User.query.filter_by(username=current_user).first()
    # 不是管理员访问这个接口时，重定向到首页
    # 如需测试，请注释掉下面这两行代码
    if not user or user.role.admin is False:
        return redirect("/")

    access_records = AccessRecord.query.order_by(AccessRecord.datetime.desc()).all()
    return render_template('admin_home.html', access_records=access_records)



# 添加访问记录（如果用不到就注释掉）
@routes_bp.route('/add-record', methods=['POST'])
@jwt_required()
def add_record():
    data = request.get_json()
    username = data['username']
    user = User.query.filter_by(username=username).first()
    if user:
        access_record = AccessRecord(user_id=user.id)
        db.session.add(access_record)
        db.session.commit()
        return jsonify(message="Record added successfully"), 200
    else:
        return jsonify(message="User not found"), 404

