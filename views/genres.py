from flask import request
from flask_restx import Resource, Namespace

from dao.model.genre import GenreSchema
from implemented import genre_service
from service.auth import admin_required, auth_required

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        rs = genre_service.get_all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        req_json = request.json
        new_genre = genre_service.create(req_json)
        return f"Created id: {new_genre.id}", 201



@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    @auth_required
    def get(self, gid: int):
        genre = genre_service.get_one(gid)
        sm_d = GenreSchema().dump(genre)
        return sm_d, 200

    @admin_required
    def put(self, gid: int):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = gid
        if genre_service.update(req_json):
            return f"Update id: {gid}", 201
        return "not found", 404

    @admin_required
    def delete(self, gid: int):
        if genre_service.delete(gid):
            return "", 204
        return "not found", 404
