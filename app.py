from flask import Flask, render_template, request, jsonify, send_file
from pymongo import MongoClient
import os, csv
from io import StringIO

app = Flask(__name__)

uri = "mongodb://kamaljeet07:Kamal%40%23@cluster0-shard-00-00.9call.mongodb.net:27017,cluster0-shard-00-01.9call.mongodb.net:27017,cluster0-shard-00-02.9call.mongodb.net:27017/?ssl=true&replicaSet=atlas-y36f67-shard-0&authSource=admin&retryWrites=true&w=majority"
client = MongoClient(uri)
db = client["wel"]
collection = db["sheet"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/load-cells', methods=['GET'])
def load_cells():
    data = collection.find({"type": "cell"})
    meta = collection.find_one({"type": "meta"})
    cell_data = {item['cell_id']: item['value'] for item in data}
    response = {
        "cells": cell_data,
        "rows": meta['rows'] if meta else 10,
        "columns": meta['columns'] if meta else 10
    }
    return jsonify(response)

@app.route('/update-cell', methods=['POST'])
def update_cell():
    data = request.get_json()
    cell_id = data['cell_id']
    value = data['value']

    collection.update_one(
        {"cell_id": cell_id, "type": "cell"},
        {"$set": {"value": value}},
        upsert=True
    )
    return jsonify({"status": "success"})

@app.route('/delete-all', methods=['POST'])
def delete_all():
    collection.delete_many({"type": "cell"})
    return jsonify({"status": "all_deleted"})

@app.route('/update-meta', methods=['POST'])
def update_meta():
    data = request.get_json()
    rows = data.get('rows')
    columns = data.get('columns')
    collection.update_one(
        {"type": "meta"},
        {"$set": {"rows": rows, "columns": columns}},
        upsert=True
    )
    return jsonify({"status": "meta_updated"})

@app.route('/export', methods=['GET'])
def export_csv():
    data = list(collection.find({"type": "cell"}))
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Cell ID', 'Value'])
    for item in data:
        writer.writerow([item['cell_id'], item['value']])
    output.seek(0)
    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name='spreadsheet.csv'
    )

if __name__ == '__main__':
    app.run(debug=True)
