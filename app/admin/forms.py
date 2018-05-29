from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, Regexp
from app.models import Admin, Tag

tags = Tag.query.all()


class AdminLoginForm(FlaskForm):
    """
    管理员登录表单
    """
    account = StringField(
        label="账号",
        validators=[DataRequired("请输入账号")],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号",
            # "required":"required"
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[DataRequired("请输入密码")],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码",
            # "required":"required"
        }

    )
    submit = SubmitField(
        "登录",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }

    )

    def validate_account(self, field):
        account = field.data
        admin_count = Admin.query.filter_by(name=account).count()
        if admin_count == 0:
            raise ValidationError("此账号不存在！")


class AdminRegisterForm(FlaskForm):
    name = StringField(
        label="管理员用户名",
        validators=[DataRequired("对不起，请输入非空管理员用户名")],
        description="用户名",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入用户名",
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
        "管理员注册",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }

    )


class TagForm(FlaskForm):
    name = StringField(
        label="名称",
        validators=[DataRequired("请输入标签！")],
        description="标签",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placehodler": "请输入标签名称",
        }
    )
    submit = SubmitField(
        "添加标签",
        render_kw={
            "class": "btn btn-primary",
        }
    )


class MovieForm(FlaskForm):
    '''
    电影表单
    '''
    title = StringField(
        label="片名",
        validators=[
            DataRequired("请输入片名！")
        ],
        description="片名",
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "placeholder": "请输入片名"
        }
    )
    url = FileField(
        label="文件",
        validators=[DataRequired("请上传文件")],
        description="文件",
    )
    info = TextAreaField(
        label="简介",
        validators=[DataRequired("请输入简介")],
        description="简介",
        render_kw={
            "class": "form-control",
            "rows": 10,
        }
    )
    logo = FileField(
        label="封面",
        validators=[DataRequired("请输入封面")],
        description="封面",
    )
    star = SelectField(
        label="星级",
        validators=[DataRequired("请选择星级")],
        description="星级",
        coerce=int,
        choices=[(1, "1星"), (2, "2星"), (3, "3星"), (4, "4星"), (5, "5星")],
        render_kw={
            "class": "form-control",
        }
    )
    tag_id = SelectField(
        label="标签",
        validators=[DataRequired("请选择标签")],
        description="标签",
        coerce=int,
        choices=[(v.id, v.name) for v in tags],
        render_kw={
            "class": "form-control",
        }
    )
    area = StringField(
        label="地区",
        validators=[
            DataRequired("请输入地区！")
        ],
        description="地区",
        render_kw={
            "class": "form-control",

            "placeholder": "请输入地区"
        }
    )
    length = IntegerField(
        label="片长",
        validators=[
            DataRequired("请输入片长！")
        ],
        description="片长",
        render_kw={
            "class": "form-control",

            "placeholder": "请输入片长"
        }
    )
    release_time = StringField(
        label="上映时间",
        validators=[
            DataRequired("请输入上映时间！")
        ],
        description="上映时间",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入上映时间",
            "id": "input_release_time",
        }
    )
    submit = SubmitField(
        "提交",
        render_kw={
            "class": "btn btn-primary",
        }

    )
