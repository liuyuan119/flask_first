from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app = Flask(__name__)


app.register_blueprint(home_blueprint, url_prefix="/home")
app.register_blueprint(admin_blueprint, url_prefix="/admin")


app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:1190@127.0.0.1:3306/flask"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SECRET_KEY'] = '123'

db = SQLAlchemy(app)    # 实例化db对象





