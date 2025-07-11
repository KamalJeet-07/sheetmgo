from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB Atlas URI (Replace with your actual URI)
uri = "mongodb://kamaljeet07:Kamal%40%23@cluster0-shard-00-00.9call.mongodb.net:27017,cluster0-shard-00-01.9call.mongodb.net:27017,cluster0-shard-00-02.9call.mongodb.net:27017/?ssl=true&replicaSet=atlas-y36f67-shard-0&authSource=admin&retryWrites=true&w=majority"
client = MongoClient(uri)
db = client["wel"]
collection = db["sheet"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/load-cells', methods=['GET'])
def load_cells():
    data = collection.find()
    cell_data = {item['cell_id']: item['value'] for item in data}
    return jsonify(cell_data)

@app.route('/update-cell', methods=['POST'])
def update_cell():
    data = request.get_json()
    cell_id = data['cell_id']
    value = data['value']

    collection.update_one(
        {"cell_id": cell_id},
        {"$set": {"value": value}},
        upsert=True
    )
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
