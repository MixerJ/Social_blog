# -*- coding:utf-8 -*-
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorator_function(*args.**kwargs):
            if not g.current_user.can(permission):
                return forbidden('没有权限')
            return f(*args, **kwargs)
        return decorator_function
    return decorator
