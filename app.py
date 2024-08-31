from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

mongo_user = os.environ.get("MONGO_INITDB_ROOT_USERNAME", "root")
mongo_pass = os.environ.get("MONGO_INITDB_ROOT_PASSWORD", "example")
mongo_host = os.environ.get("MONGO_HOST", "mongodb-service")
mongo_port = os.environ.get("MONGO_PORT", "27017")

mongo_uri = f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}/?authSource=admin"

client = MongoClient(mongo_uri)

db = client.flask_db

collection = db.data

@app.route('/')
def index():
    return f"Welcome to the Flask app! The current time is: {datetime.now()}"

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        data = request.get_json()
        collection.insert_one(data)
        return jsonify({"status": "Data inserted"}), 201
    elif request.method == 'GET':
        data = list(collection.find({}, {"_id": 0}))
        return jsonify(data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
