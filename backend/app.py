from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

import os

app = Flask(__name__)

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/add", methods=["POST"])
def add_user():
    mongo.db.users.insert_one({"name": request.json["name"], "email": request.json["email"]})
    return "User added"

@app.route("/get", methods=["GET"])
def get_user():
    user = mongo.db.users.find_one({"name": "gion"})
    return jsonify({"name": user["name"], "email": user["email"]})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
