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


# 标签添加
@admin.route("/tag/add/", methods=["GET", "POST"])
@check_admin_login
def tag_add():
    from app.admin.forms import TagForm
    from app.models import Tag
    from app import db
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tagnum = Tag.query.filter_by(name=data['name']).count()
        if tagnum == 1:
            flash("标签名已经存在", "err")
            return redirect(url_for("admin.tag_add"))
        # 入库
        tag = Tag(name=data['name'])
        db.session.add(tag)
        db.session.commit()
        flash("添加标签成功", "ok")
        return redirect(url_for("admin.tag_add"))
    return render_template("admin/tag_add.html", form=form)


# 标签列表
@admin.route("/tag/list/<int:page>/", methods=["GET"])
@check_admin_login
def tag_list(page):
    from app.models import Tag
    if page is None:
        page = 1
    page_data = Tag.query.order_by(
        Tag.addtime.desc()  # 按照时间进行降序排序
    ).paginate(page=page, per_page=2)
    return render_template("admin/tag_list.html", page_data=page_data)


# 标签删除
@admin.route("/tag/del/<int:id>/", methods=["GET"])
@check_admin_login
def tag_del(id=None):
    from app.models import Tag
    from app import db
    tag = Tag.query.filter_by(id=id).first_or_404()  # notes: first() or 404()
    db.session.delete(tag)
    db.session.commit()
    flash("删除标签成功", "ok")
    return redirect(url_for("admin.tag_list", page=1))


# 标签修改
@admin.route("/tag/edit/<int:id>", methods=["GET", "POST"])
@check_admin_login
def tag_edit(id=None):
    from app.admin.forms import TagForm
    from app.models import Tag
    from app import db
    form = TagForm()
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(name=data['name']).count()
        if tag_count == 1:
            flash("标签已经存在", "err")
            return redirect(url_for("admin.tag_edit", id=id))
        # 入库
        tag.name = data["name"]
        db.session.add(tag)
        db.session.commit()
        flash("修改标签成功", "ok")
        return redirect(url_for("admin.tag_list", page=1))
    return render_template("admin/tag_edit.html", form=form, tag=tag)
