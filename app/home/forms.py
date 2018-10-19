from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,FileField,TextAreaField,SelectField,SelectMultipleField
from wtforms.validators import DataRequired,ValidationError,EqualTo,Email,Regexp
from app.models import Admin,Movie,Tag,Auth,Role,User

class LoginForm(FlaskForm):
    """会员登录表单"""

    account = StringField(
        label='账号',
        validators=[
           DataRequired('请输入账号')
        ],
        # 描述
        description='账号',
        # 附加选项
        render_kw={"class":"form-control",
                   "placeholder":"请输入账号",
                   "required":'required'}

    )
    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired('请输入密码')
        ],
        description='密码',
        render_kw={
            "class":"form-control",
            "placeholder":"请输入密码",
            "required":'required'
        }
    )

    submit = SubmitField(
        '登录',
        render_kw={
            "class":"btn btn-primary btn-block btn-flat"
        }
    )

class RegistForm(FlaskForm):
    name = StringField(
        label='昵称',
        validators=[
            DataRequired('请输入昵称！')
        ],
        description='昵称',
        render_kw={
            'class':'form-control input-lg',
            'placeholder':'请输入昵称',
        }
    )
    email = StringField(
        label='邮箱',
        validators=[
            DataRequired('请输入邮箱！'),
            Email('邮箱格式不正确')
        ],
        description='邮箱',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入邮箱',
        }
    )
    phone = StringField(
        label='手机号',
        validators=[
            DataRequired('请输入手机号！'),
            Regexp('1[3458]\\d{9}',message='手机格式不正确')
        ],
        description='手机号',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入手机号',
        }
    )
    pwd= PasswordField(
        label='密码',
        validators=[
            DataRequired('请输入密码！'),
        ],
        description='密码',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入密码',
        }
    )
    repwd = PasswordField(
        label='确认密码',
        validators=[
            DataRequired('请输入确认密码！'),
            EqualTo('pwd',message='两次密码不一致')
        ],
        description='确认密码',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入确认密码',
        }
    )
    submit = SubmitField(
        '注册',
        render_kw={
            "class": "btn btn-lg btn-success btn-block"
        }
    )
    def validate_name(self,field):
        name = field.name
        user = User.query.filter_by(name=name).count()
        if user == 1:
            raise ValidationError('昵称已存在')

    def validate_phone(self, field):
        phone = field.phone
        user = User.query.filter_by(phone=phone).count()
        if user == 1:
            raise ValidationError('昵称已存在')

    def validate_email(self,field):
        email = field.email
        user = User.query.filter_by(email=email).count()
        if user == 1:
            raise ValidationError('昵称已存在')

class UserdetailForm(FlaskForm):

    pass

class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label='旧密码',
        validators=[
            DataRequired('请输入旧密码')
        ],
        description='旧密码',
        render_kw={
            'class':'form-control',
            'placeholder':'请输入旧密码',
        }
    )
    new_pwd = PasswordField(
        label='新密码',
        validators=[
            DataRequired('请输入新密码')
        ],
        description='新密码',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入新密码',
        }
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary"
        }
    )
class CommentForm(FlaskForm):
    content = TextAreaField(
        label='内容',
        validators=[
            DataRequired('请输入内容')
        ],
        description='内容',
        render_kw={
            'id': 'input_content'
        }
    )
    submit = SubmitField(
        '提交评论',
        render_kw={
            "class": "btn btn-success",
            'id':'btn-sub'
        }
    )