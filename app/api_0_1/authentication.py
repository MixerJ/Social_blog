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
# 验证密码，用户令牌


@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token == '':
        g.current_user = AnonymousUser()
        return True
    # 使用令牌登录
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(email=email_or_token)
    if not user:
        return False
    g.current_user = user
    # 不是使用令牌登录
    g.token_used = False
    return user.verify_password(password)
# 生成认真令牌


@api.route('/token')
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('不合法登录验证')
    return jsonify({'token': g.current_user.generate_auth_token(expiration=3600), 'expiration': 3600})
