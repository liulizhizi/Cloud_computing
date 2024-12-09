# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # 加载环境变量

class Config:
    JWT_SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if os.getenv('FLASK_ENV') == 'development':
        SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    else:
        db_user = 'root'
        db_pass = '123456'
        db_name = 'db'
        db_host = '34.142.76.43'
        db_port = 3306
        print("running on MySQL")
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"