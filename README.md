# 3D Object Viewer

A simple web application for viewing 3D objects (.obj files) using Three.js.

## Setup

1. First, prepare the data by generating `data_files.json`:

```bash
# For local development (paths will be relative to current directory)
python construct.py --relative

# If serving from a different directory, specify the server root:
python construct.py --relative --server-root /path/to/server/root
```

2. Start a local web server:

```bash
# Using Python's built-in HTTP server
python -m http.server 8080
```

3. Open your browser and navigate to `http://localhost:8080`

## Features

- Select a dataset from the dropdown menu
- Navigate through 3D models using Previous/Next buttons or arrow keys
- Switch between view modes: Surface, Wireframe, or Both
- Automatic centering and scaling of models
- Interactive 3D view with orbit controls

## File Structure

- `index.html`: The main web application
- `data.json`: Contains dataset paths configuration
- `data_files.json`: Generated file with actual object file paths (run `construct.py` to create)
- `construct.py`: Script to scan directories and generate `data_files.json`

## Requirements

- Web browser with WebGL support
- Three.js (loaded from CDN)

## Troubleshooting

If models don't load, check that:

1. The file paths in `data_files.json` are accessible from the web server
2. For local files, make sure to run `construct.py` with the `--relative` flag
3. Check browser console for errors
4. Ensure your browser supports WebGL and has it enabled

## Notes

- The application uses Three.js's OBJLoader to load .obj files
- File paths in `data_files.json` must be accessible to the browser (use server-relative paths)