from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, Regexp
from app.models import User

"""
登陆表单
1. 账号  name
2. 密码  pwd
3. 登陆按钮
"""


class LoginForm(FlaskForm):
    name = StringField(label="账号",
                       validators=[DataRequired("请输入账号信息")],
                       description="账号",
                       render_kw={
                           "class": "form-control",
                           "placeholder": "请输入账号",
                       }
                       )
    pwd = PasswordField(label="密码",
                        validators=[DataRequired("请输入密码信息")],
                        description="密码",
                        render_kw={
                            "class": "form-control",
                            "placeholder": "请输入密码",
                        }
                        )
    submit = SubmitField(
        "登录",
        render_kw={
            "class": "btn btn-primary btn-success",
        }
    )

    def validate_name(self, field):
        name = field.data
        user_count = User.query.filter_by(name=name).count()
        if user_count == 0:
            raise ValidationError("此账号不存在！--func")



'''
注册表单
1. 用户名:name
2. 邮箱：email
3. 手机: phone
4. 密码：pwd
5. 重置密码：repwd
6. 注册按钮
'''


class RegisterForm(FlaskForm):
    name = StringField(
        label="用户名",
        validators=[DataRequired("对不起，请输入非空用户名")],
        description="用户名",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入用户名",
        }
    )
    email = StringField(
        label="邮箱",
        validators=[
            DataRequired("请输入非空邮箱"),
            Email("请输入有效邮箱，格式不对！")
        ],
        description="邮箱",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入邮箱",
        }
    )
    phone = StringField(
        label="手机",
        validators=[
            DataRequired("请输入非空手机号码"),
            Regexp("1[35678]\\d{9}", message="手机号码格式不正确")
        ],
        description="手机",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入手机号码",
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[DataRequired("请输入非空密码")],
        description="密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入密码",
        }
    )
    repwd = PasswordField(
        label="确认密码",
        validators=[
            DataRequired("请输入非空确认密码"),
            EqualTo("pwd", message="两次输入密码不正确！")
        ],
        description="确认密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入确认密码",
        }
    )
    submit = SubmitField(
        "注册",
        render_kw={
            "class": "btn btn-lg btn-success",
        }
    )

    def validate_name(self, field):
        name = field.data
        user = User.query.filter_by(name=name)
        user_count = user.count()
        if user_count == 1:
            raise ValidationError("用户名已经存在.")

    # def validate_email(self, field):
    #     email = field.data
    #     user_count = User.query.filter_by(email=email).count()
    #     if user_count == 1:
    #         raise ValidationError("用户名已经存在.")
    #
    # def validate_phone(self, field):
    #     phone = field.data
    #     user_count = User.query.filter_by(phone=phone).count()
    #     if user_count == 1:
    #         raise ValidationError("用户名已经存在.")
