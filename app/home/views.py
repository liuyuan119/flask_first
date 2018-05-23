from flask import Response, render_template, redirect, url_for, flash, session, request
from werkzeug.security import generate_password_hash

from . import home

from functools import wraps


# 登录装饰器
def check_user_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("home.home_login"))
        return func(*args, **kwargs)

    return decorated_function


@home.route("/test/")
@check_user_login
def mtest():
    return Response("this is mtest fuction.")


@home.route("/")
def index():
    login_flag = 0
    user_name = ''
    if session.get('user'):
        login_flag = 1
        user_name = session['user']
    return render_template("home/index.html", login_flag=login_flag, username=user_name)


@home.route("/add_user/<string:username>/<string:email>/<string:address>/")
def home_add_user(username, email, address):
    # 传入Model层，存储数据库
    from app import db
    from app.models import UserInfo
    user = UserInfo(username=username, email=email, address=address)
    db.session.add(user)
    db.session.commit()
    print('save ok.')
    import json
    data = {'username': username, 'email': email, 'address': address}
    result = {'code': 200, 'message': 'ok', 'data': data}
    return Response(json.dumps(result))


# 用户登录
@home.route("/login/", methods=["GET", "POST"])
def home_login():
    from app.home.forms import LoginForm
    from app.models import User
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        fname = data['name']
        fpwd = data['pwd']
        user = User.query.filter_by(name=fname).first()
        if user == None:
            flash("用户名不存在", "err")
            return redirect(url_for("home.home_login"))
        if not user.check_pwd(fpwd):
            flash("密码验证错误", "err")
            return redirect(url_for("home.home_login"))
        # check login ok
        session['user'] = user.name
        session['usr_id'] = user.id
        return render_template("home/index.html", login_flag=1, username=user.name)
    return render_template("home/login.html", title="用户登录", form=form)


@home.route("/wflogin/")
def home_wflogin():
    from .forms import LoginForm
    login_form = LoginForm()
    return render_template("home/wflogin.html", title="wtform表单登录", form=login_form)


@home.route("/logout/")
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    return redirect(url_for("home.home_login"))


# 用户注册
@home.route("/register/", methods=["GET", "POST"])
def home_register():
    from app.home.forms import RegisterForm
    from app.models import User
    from app import db
    form = RegisterForm()
    print('######form before submit check ####')
    if form.validate_on_submit():
        print('form submit enter.')
        data = form.data
        user = User(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            pwd=generate_password_hash(data['pwd']),
        )
        db.session.add(user)
        db.session.commit()
        flash("恭喜，注册成功！", "ok")
    return render_template("home/register.html", title="会员注册", form=form)


@home.route("/play/")
def play():
    return render_template("home/play.html")


@home.route("/animation/")
def animation():
    return render_template("home/animation.html")
