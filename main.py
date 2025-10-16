from flask import Flask, jsonify, request, send_from_directory
import argparse
import json
import os

app = Flask(__name__)

# Path to the data_files.json
DATA_FILES_PATH = 'data_files.json'

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/data')
def get_data():
    with open(DATA_FILES_PATH, 'r') as f:
        data = json.load(f)
        print(data)
    return jsonify(data)

@app.route('/object')
def get_object():
    file_path = request.args.get('path')
    print(file_path)
    if not file_path:
        return "File path is required.", 400

    if not os.path.exists(abs_path):
        return "File not found.", 404

    # send_from_directory needs directory and filename separately
    directory, filename = os.path.split(file_path)
    return send_from_directory(directory, filename)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate data_files.json containing paths to OBJ files")
    parser.add_argument("--port", default=8080, help="Port address")
    args = parser.parse_args()
    
    app.run(debug=True, port=args.port)