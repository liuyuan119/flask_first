from flask import render_template, redirect, url_for, flash, session, request

from . import admin
from functools import wraps


# 超级管理员登录装饰器
def check_admin_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login"))
        return func(*args, **kwargs)

    return decorated_function


@admin.route("/")
@check_admin_login
def index():
    # return "<h1 style='color:gray'>管理端Admin的主页面</h1>"
    return render_template("admin/index.html", username=session["admin"])


# 登录
@admin.route("/login/", methods=["POST", "GET"])
# @check_admin_login
def login():
    from app.admin.forms import AdminLoginForm
    from app.models import Admin
    form = AdminLoginForm()

    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data['account']).first()
        if admin == None:
            flash("账号不存在", "err")
            return redirect(url_for("admin.login"))
        if not admin.check_pwd(data['pwd']):
            flash("密码错误", "err")
            return redirect(url_for("admin.login"))
        session["admin"] = data['account']
        return redirect(url_for("admin.index"))
    return render_template("admin/login.html", form=form)


@admin.route("/logout/")
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin.login'))


# 用户注册
@admin.route("/register/", methods=["GET", "POST"])
def home_register():
    from werkzeug.security import generate_password_hash
    from app.admin.forms import AdminRegisterForm
    from app.models import Admin
    from app import db
    form = AdminRegisterForm()
    if form.validate_on_submit():
        data = form.data
        user = Admin(
            name=data['name'],
            pwd=generate_password_hash(data['pwd']),
        )
        db.session.add(user)
        db.session.commit()
        flash("恭喜，管理员注册成功！", "ok")
    return render_template("admin/register.html", title="会员注册", form=form)
