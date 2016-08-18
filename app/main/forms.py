# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, SelectField, BooleanField
from wtforms.validators import Required, Length, Email, Regexp
from ..models import Role, User
from flask_pagedown.fields import PageDownField
# 编辑用户信息表单


class EditProfileForm(Form):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

# 编辑管理员表单


class EditProfileAdminForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(0, 64), Email()])
    username = StringField('用户名', validators=[Required(), Length(
        1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名必须只有字母，数字，下划线，小数点')])
    confirmed = BooleanField('用户激活')
    role = SelectField('角色', coerce=int)
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('居住地', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('保存')

    # 初始话数据
    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    # 验证邮箱是否被注册
    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被注册')

    # 验证用户名是否被使用
    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经被使用')


# 文章表单
class PostForm(Form):
    body = PageDownField('你想写些什么内容呢？', validators=[Required()])
    submit = SubmitField('提交')
# 评论表单


class CommentForm(Form):
    body = PageDownField('你想评论些什么内容呢？', validators=[Required()])
    submit = SubmitField('提交')
