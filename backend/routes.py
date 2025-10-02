from . import app
from db import get_database
import os
import json
from bson import json_util
import requests
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "songs.json")
data: list = json.load(open(json_url))

db = get_database("songs")
songsCollection = db["songs"]

def parse_json(data):
    return json.loads(json_util.dumps(data))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF SONGS
######################################################################


@app.route("/count")
def count():
    try:
        songsCollection.drop()
        songsCollection.insert_many(data)
        count = songsCollection.count_documents({})
        return jsonify({"length": count}), 200
    except requests.exceptions.RequestException as e:
        return {"Message": f"Request failed: {e}"}, 500


######################################################################
# GET ALL SONGS
######################################################################
@app.route("/song", methods=["GET"])
def get_songs():
    try:
        data= list(songsCollection.find({}))
        return jsonify((parse_json(data))), 200
    except requests.exceptions.RequestException as e:
        return {"Message": f"Request failed: {e}"}, 500

######################################################################
# GET A SONG
######################################################################


@app.route("/song/<int:id>", methods=["GET"])
def get_song_by_id(id):
    try:
        data = songsCollection.find_one({"id": id}, {"_id": 0})
        if data:
            return jsonify((parse_json(data))), 200
        return {"Message": "Something went wrong!"}, 404
    except requests.exceptions.RequestException as e:
        return {"Message": f"Request failed: {e}"}, 500


######################################################################
# CREATE A SONG
######################################################################
@app.route("/song", methods=["POST"])
def create_song():
    try:
        post_data = request.get_json()
        if post_data:
            song_id = post_data.get("id")
            data = songsCollection.find_one({"id": song_id})
            if data:
                return {"Message": f"song with id {song_id} already present"}, 302
            
            result = songsCollection.insert_one(post_data)
            if result.acknowledged:
                return jsonify((parse_json(post_data))), 201
        
        return {"Message": "Something went wrong!"}, 404
    except requests.exceptions.RequestException as e:
        return {"Message": f"Request failed: {e}"}, 500

######################################################################
# UPDATE A SONG
######################################################################


@app.route("/song/<int:id>", methods=["PUT"])
def update_song(id):
    try:
        post_data = request.get_json()
        if post_data:
            result = songsCollection.update_one({"id": id}, {"$set": post_data})
            if result.modified_count > 0:
                return jsonify((parse_json(post_data))), 200

        return {"Message": "Something went wrong!"}, 404
    except Exception as e:
        return {"Message": f"Request failed: {e}"}, 500

######################################################################
# DELETE A SONG
######################################################################
@app.route("/song/<int:id>", methods=["DELETE"])
def delete_song(id):
    try:
        result = songsCollection.delete_one({"id": id})
        if result.deleted_count > 0:
            return "", 204

        return {"Message": "Something went wrong!"}, 404
    except Exception as e:
        return {"Message": f"Request failed: {e}"}, 500
