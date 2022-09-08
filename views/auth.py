from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service

auth_ns = Namespace('auth')


@auth_ns.route('/')
class UsersView(Resource):
    def post(self):
        return user_service.auth_by_name(request.json), 200

    def put(self):
        return user_service.auth_by_refresh_token(request.json), 201

