# -*- coding:utf-8 -*-
from flask import Blueprint
api = Blueprint('api', __name__)
from . import authentication, posts, users, comments, errors
from ..models import Permission


@api.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
