# app.py
from flask import Flask
from flask_jwt_extended import JWTManager
from app.models import db
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "super secret key"
# 初始化扩展
db.init_app(app)
jwt = JWTManager(app)

# 创建数据库表
with app.app_context():
    db.create_all()

from app.routes import routes_bp as routes_app
# 注册路由
app.register_blueprint(routes_app)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
