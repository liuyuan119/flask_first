from functools import wraps

from app.home import home
from flask import redirect, render_template, Response, url_for, flash, session


# @home.route("/")
# def index():
#     return "<h1 style='color:green'> this is home.</h1>"

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
    return Response("this is mtest")


@home.route("/")
def index():
    # return "<h1 style='color:green'>我是Home主页面</h1>"
    login_flag = 0
    user_name = ''
    if session.get('user'):
        login_flag = 1
        user_name = session['user']
    return render_template("home/index.html", login_flag=login_flag, username=user_name)


# @home.route("/test/")
# def test():
#     return render_template("home/index.html")


# 用户登录
@home.route("/login/", methods=["GET", "POST"])
def home_login():
    from app.home.forms import LoginForm
    from app.models import User
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data["name"]).first()
        if not user:
            flash("用户名不存在", "err")
            return redirect(url_for('home.home_login'))
        if not user.check_pwd(data["pwd"]):
            flash("密码错误！", "err")
            return redirect(url_for('home.home_login'))
        session["user"] = user.name
        session["user_id"] = user.id
        # return redirect(url_for("home.index"))
        return render_template("home/index.html", login_flag=1, username=user.name)
    return render_template("home/login.html", title="会员登录", form=form)


@home.route("/logout/")
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    return redirect(url_for("home.home_login"))
    # return redirect('/home/login')


@home.route("/register/", methods=["GET", "POST"])
def home_register():
    from app.home.forms import RegisterForm
    from app.models import User
    from app import db
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        from werkzeug.security import generate_password_hash
        user = User(
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            pwd=generate_password_hash(data["pwd"]),

        )
        db.session.add(user)
        db.session.commit()
        from flask import flash
        flash("注册成功！", "ok")
    return render_template("home/register.html", form=form)


@home.route("/wtflogin/")
def home_wtflogin():
    from app.home.forms import LoginForm
    form = LoginForm()
    return render_template("home/wtflogin.html", form=form)


@home.route("/animation/")
def animation():
    return render_template("home/animation.html")


@home.route("/play/")
def play():
    return render_template("home/play.html")


@home.route('/userinfo/')
def user_info():
    return "<h1 style='color:blue'> this is user info.</h1>"


@home.route('/helloworld/')
def hello_world():
    return redirect('/home/userinfo')


@home.route('/add_user/<string:username>/<string:email>/')
def add_user(username, email):
    from app.models import UserInfo
    from app import db
    user = UserInfo(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return Response('ok')
