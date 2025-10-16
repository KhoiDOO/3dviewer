from flask import Flask, jsonify, request, send_from_directory, send_file
import argparse
import json
import os
import datetime

app = Flask(__name__)
app.logger.setLevel('INFO')

# Path to the data_files.json
DATA_FILES_PATH = 'data_files.json'

# Simple in-memory tracking for /data requests so clients can verify the JSON was requested
data_request_info = {
    'count': 0,
    'last_request_time': None,
    'last_request_ip': None,
}

@app.route('/')
def index():
    app.logger.info("Serving index.html to %s", request.remote_addr)
    return send_from_directory('.', 'index.html')

@app.route('/data')
def get_data():
    # Log and update tracking info
    app.logger.info("/data requested from %s - UA: %s", request.remote_addr, request.headers.get('User-Agent'))
    data_request_info['count'] += 1
    # remote_addr may be None in some setups
    data_request_info['last_request_ip'] = request.remote_addr
    data_request_info['last_request_time'] = datetime.datetime.now(datetime.timezone.utc).isoformat() + 'Z'

    try:
        with open(DATA_FILES_PATH, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        app.logger.error("%s not found", DATA_FILES_PATH)
        return "data_files.json not found on server.", 500
    except json.JSONDecodeError as e:
        app.logger.error("Failed to parse %s: %s", DATA_FILES_PATH, e)
        return "data_files.json is invalid.", 500

    return jsonify(data)


@app.route('/data/status')
def data_status():
    """Return simple status about /data requests so the user can confirm index.html requested the JSON."""
    return jsonify(data_request_info)

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