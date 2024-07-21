import os
import json
from flask import Flask, request
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId, json_util
from datetime import datetime
from flask_cors import CORS

load_dotenv()

APPLICATION_ROOT = os.getenv("application_root")
MONGODB_URL = os.getenv("mongodb_url")
DB_NAME = os.getenv("db_name")
COLLECTION_NAME = os.getenv("collection_name")
app = Flask(__name__)
CORS(app)


client = MongoClient(MONGODB_URL)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.route(APPLICATION_ROOT + '/', methods=["GET"])
def index():
    return {
        "status": "ok",
        "message": "",
        "version": 1.0
    }, 200

@app.route(APPLICATION_ROOT + '/tasks/', methods=["GET"])
def read():
    #     
    data = collection.find({})
    todos = list(data)
    todosJson = json.loads(json_util.dumps(todos))
    return {
        "status": "ok",
        "message": "",
        "data": todosJson
    }, 200

@app.route(APPLICATION_ROOT + '/tasks/<id>', methods=["GET"])
def read_one_by_id(id):
    
    filter = {
        "_id": ObjectId(id)
    }

    data = collection.find_one(filter)
    todosJson = json.loads(json_util.dumps(data))
    return {
        "status": "ok",
        "message": "",
        "data": todosJson
    }, 200

@app.route(APPLICATION_ROOT + '/tasks/<id>', methods=["PUT"])
def update_one_by_id(id):
    
    data = request.json
    print(data)
    filter = {
        "_id": ObjectId(id)
    }

    payload = {}
    payload.update({"$set": {}})

    curDate = datetime.now().isoformat()

    if 'title' in data:
        payload["$set"].update({'title': data['title']})

    if 'description' in data:
        payload["$set"].update({'description': data['description']})

    if 'title' in data or 'decription' in data:
        payload["$set"].update({'meta.modifiedAt': curDate})

    data = collection.update_one(filter, payload, upsert=False)
    return {
        "status": "ok",
        "message": "Document with ID " + id + " successfully updated."
    }, 200

@app.route(APPLICATION_ROOT + '/tasks/', methods=["POST"])
def create_one():
    data = request.json

    curDate = datetime.now().isoformat()

    data['meta'] = {"createdAt": curDate, "modifiedAt": curDate}

    collection.insert_one(data)
    return {
        "status": "ok",
        "message": ""
    }, 201

@app.route(APPLICATION_ROOT + '/tasks/<id>', methods=["DELETE"])
def delete_one_by_id(id):
    filter = {
        "_id": ObjectId(id)
    }
    res = collection.delete_one(filter)
    if res.deleted_count == 1:
        return {
            "status": "ok",
            "message": "Document with ID " + id + " deleted successfully."
        }, 200
    else:
        return {
            "status": "not found",
            "message": "Document with ID " + id + " not found."
        }, 200

    
if __name__ == '__main__':
    app.run()