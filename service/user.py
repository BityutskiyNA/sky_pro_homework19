import base64
import calendar
import datetime
import hashlib
import hmac
import jwt
from flask_restx import abort
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS, ALGO, SECRET_HERE
from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_hash(self, password):
        hash_p = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), PWD_HASH_SALT, PWD_HASH_ITERATIONS)
        return base64.b64encode(hash_p)

    def create(self, user_d):
        password = user_d.get("password")
        user_d['password'] = self.get_hash(password)
        return self.dao.create(user_d)

    def update(self, user_d):
        self.dao.update(user_d)
        return self.dao

    def delete(self, user_d):
        self.dao.delete(user_d)

    def get_all(self):
        users = self.dao.get_all()
        return users

    def auth_by_name(self, data ):
        name = data.get("username")
        users = self.dao.get_one_by_name(name)

        if not users:
            return {"error": "Неверные учётные данные"}, 401

        other_password = data.get("password")
        for user in users:
            if self.test_hash(user.password, other_password) == True:
                tokens = self.returb_token(user)
                return tokens, 201
        return {"error": "Неверные учётные данные"}, 401


    def auth_by_refresh_token(self, data ):
        refresh_token = data.get("refresh_token")
        try:
            token = jwt.decode(refresh_token, SECRET_HERE, algorithm=ALGO)
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)


        user = self.dao.get_one_by_name(token['username'])

        if not user:
            return {"error": "Неверные учётные данные"}, 401

        tokens = self.returb_token(user[0])
        return tokens, 201

    def test_hash(self, password_hash, other_password):
        return hmac.compare_digest(password_hash,self.get_hash(other_password))


    def returb_token(self, user):
        data_auth = {
            "username": user.username,
            "role": user.role
        }
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data_auth["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data_auth, SECRET_HERE, algorithm=ALGO)
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data_auth["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data_auth, SECRET_HERE, algorithm=ALGO)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}

        return tokens