from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET ALL PICTURES
######################################################################


@app.route("/picture", methods=["GET"])
def get_pictures():
    """return pictures"""
    if data:
        return jsonify(data), 200
    
    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """return picture by id"""
    if data:
        for picture in data:
            if picture["id"] == id:
                return jsonify(picture), 200
        return {"message": "Not found"}, 404

    return {"message": "Internal server error"}, 500
    
######################################################################
# CREATE A PICTURE
######################################################################


@app.route("/picture", methods=["POST"])
def create_picture():
    """creates picture from body data"""
    picture = request.json
    if not picture:
        return {"message": "Invalid input parameter"}, 422
    if picture["id"] in [x["id"] for x in data]:
        return {"Message": f"picture with id {picture['id']} already present"}, 302
    try:
        data.append(picture)
    except NameError:
        return {"message": "data not defined"}, 500
    return picture, 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """update picture by id"""
    new_picture = request.json
    if not new_picture:
        return {"message": "Invalid input parameter"}, 422
    for picture in data:
        if picture["id"] == id:
            picture.update(new_picture)
    return new_picture, 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """delete picture by id"""
    for picture in data:
        if picture["id"] == id:
            data.remove(picture)
            return "", 204
        return {"message": "picture not found"}, 404
