from flask import request
from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from implemented import director_service
from service.auth import admin_required, auth_required

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        rs = director_service.get_all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        req_json = request.json
        new_director = director_service.create(req_json)
        return f"Created id: {new_director.id}", 201


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    @auth_required
    def get(self, did):
        r = director_service.get_one(did)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, did: int):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = did
        if director_service.update(req_json):
            return f"Update id: {did}", 201
        return "not found", 404

    @admin_required
    def delete(self, did: int):
        if director_service.delete(did):
            return "", 204
        return "not found", 404
