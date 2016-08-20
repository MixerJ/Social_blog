# -*- coding:utf-8 -*-
from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from ..models import User, AnonymousUser
from . import api
from .errors import forbiddn
# 初始化Flask-HTTPAuth
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email, password):
    if email == '':
        g.current_user = Anonymouse()
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    g.current_user = user
    return user.verify_password(password)
# Flask-HTTPAuth错误处理程序


@auth.error_handler
def auth_error():
    pass
# 保护路由可使用修饰器@auth.required


@api.route('/posts/')
@auth.login_required
def get_posts():
    pass
# 请求前进行认证


@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.confirmed and \
            not g.current_user.is_anonymous:
        return forbiddn('未认证的账号')
