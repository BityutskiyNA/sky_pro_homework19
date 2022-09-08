import datetime

import jwt
from flask import request, abort

from constants import SECRET_HERE, ALGO


def auth_required(func):
    def wrapper(*args, **kwargs):
        if "Autorization" not in request.headers:
            abort(401)

        data = request.headers.environ['HTTP_AUTORIZATION']
        token = data.split("Bearer ")[-1]

        try:
            jwt.decode(token, SECRET_HERE, algorithms=ALGO)
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        return func(*args, **kwargs)

    return wrapper

def admin_required(func):
    def wrapper(*args, **kwargs):
        if "Autorization" not in request.headers:
            abort(401)

        data = request.headers.environ['HTTP_AUTORIZATION']
        token = data.split("Bearer ")[-1]
        try:
            user = jwt.decode(token, SECRET_HERE, algorithms=ALGO)
            role = user.get("role")
            if role != "admin":
                abort(400)
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        return func(*args, **kwargs)

    return wrapper
