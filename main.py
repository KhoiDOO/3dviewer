from flask import Flask, jsonify, request, send_from_directory
import argparse
import json
import os

app = Flask(__name__)

# Path to the data_files.json
DATA_FILES_PATH = 'data_files.json'
# The root directory for the object files.
# The paths in data_files.json are like '../quadgen/...'
# We assume this script is in '3dviewer' and 'quadgen' is a sibling directory.
OBJECTS_BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'quadgen'))

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

    # We need to construct a safe path to the object file.
    # The file path is relative to the project root.
    # We construct an absolute path and then check if it's within the project.
    
    # The base directory for resolving file paths is the directory containing this script.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the full path
    abs_path = os.path.abspath(os.path.join(base_dir, file_path))

    # Security check: ensure the path is within the intended directory
    # This prevents directory traversal attacks.
    # We check against the parent of the script's directory.
    allowed_base_dir = os.path.abspath(os.path.join(base_dir, '..'))
    if not abs_path.startswith(allowed_base_dir):
        return "Forbidden: Access is denied.", 403

    if not os.path.exists(abs_path):
        return "File not found.", 404

    # send_from_directory needs directory and filename separately
    directory, filename = os.path.split(abs_path)
    return send_from_directory(directory, filename)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate data_files.json containing paths to OBJ files")
    parser.add_argument("--port", default=8080, help="Port address")
    args = parser.parse_args()
    
    app.run(debug=True, port=args.port)