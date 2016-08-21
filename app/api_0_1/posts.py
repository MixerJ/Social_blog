# -*- coding:utf-8 -*-
from . import api
# 创建新作者的文章


@api.route('/posts/', methods=['POST'])
def new_post():
    post = Post.from_json(reuqest.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonfy(post.to_json)
