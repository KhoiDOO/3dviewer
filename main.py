from flask import Flask, jsonify, request, send_from_directory, send_file
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
    return jsonify(data)

@app.route('/object')
def get_object():
    file_path = request.args.get('path')
    if not file_path:
        return "File path is required.", 400

    # Normalize the path to remove any redundant separators
    file_path = os.path.normpath(file_path)

    # If an absolute path was provided (e.g. /mnt/...), serve it directly
    if os.path.isabs(file_path):
        if not os.path.isfile(file_path):
            return "File not found.", 404
        # Use send_file for absolute paths
        return send_file(file_path)

    # For relative paths, keep the original behavior using send_from_directory
    directory, filename = os.path.split(file_path)
    if not directory:
        directory = '.'
    full_path = os.path.join(directory, filename)
    if not os.path.isfile(full_path):
        return "File not found.", 404
    return send_from_directory(directory, filename)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate data_files.json containing paths to OBJ files")
    parser.add_argument("--port", default=8080, help="Port address")
    args = parser.parse_args()
    
    app.run(debug=True, port=args.port)