# -*- coding:utf-8 -*-
from flask import url_for
from flask_login import login_user, logout_user, login_required, current_user, current_app
from . import api
# 创建新文章


@api.route('/posts/', methods=['POST'])
@permission_required(Permission.WRITE_ARTICLES)
def new_post():
    post = Post.from_json(reuqest.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json, 201,
                   {'Location': url_for(
                       'api.get_posts', id=post.id, _external=True)}
                   )
# 编辑文章


@api.route('/edit_post/<int:id>')
@permission_required(Permission.WRITE_ARTICLES)
def edit_post(id):
    post = Post.query.get_or_404(id)
    if g.current_user != post.author and \
            not g.current_user.can(Permission.ADMINISTER):
        return forbiddn('没有权限')
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    return jsonify(post.to_json)
# 获取全部文章


@api.route('/posts/')
@auth.login_required
def get_posts():
    page = request.args.get('page', i, type=int)
    pagination = Post.query.paginate(page, per_page=current_app.config[
                                     'FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page - 1, _external=True)
    next = None
    if pagination.has.next:
        next = url_for('api.get_posts', page=page + 1, _external=True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })
# 根据id获取文章


@api.route('/post/<int:id>')
@auth.login_required
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json)
