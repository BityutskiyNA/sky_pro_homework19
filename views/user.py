from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service

users_ns = Namespace('users')


@users_ns.route('/')
class UsersView(Resource):
    def get(self):
        rs = user_service.get_all()
        res = UserSchema(many=True).dump(rs)
        return res, 200

    def post(self):
        req_json = request.json
        user = user_service.create(req_json)
        return "", 201, {"location": f"/movies/{user.id}"}


@users_ns.route('/<int:u_id>')
class UserView(Resource):
    def put(self, u_id):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = u_id
        user_service.update(req_json)
        return "", 204

    def delete(self, u_id):
        user_service.delete(u_id)
        return "", 204
