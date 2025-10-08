import os
import json
import argparse

def create_data_files(use_relative_paths=False, server_root=None):
    """
    Generate data_files.json containing OBJ file paths.
    
    Args:
        use_relative_paths: If True, converts absolute paths to relative paths for browser use
        server_root: Base directory to make paths relative to (if use_relative_paths=True)
    """
    data_json = "data.json"
    assert os.path.exists(data_json), f"{data_json} does not exist"
    
    with open(data_json, "r") as f:
        data = json.load(f)

    data_files = {}
    
    for dataset_name in data:
        dataset_path = data[dataset_name]
        assert os.path.exists(dataset_path), f"{dataset_path} does not exist"
        all_files = []
        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                if file.endswith('.obj'):
                    file_path = os.path.join(root, file)
                    
                    # Convert to relative path if requested
                    if use_relative_paths and server_root:
                        try:
                            # Make path relative to the server root
                            rel_path = os.path.relpath(file_path, server_root)
                            file_path = rel_path
                        except ValueError:
                            print(f"Warning: Could not make path relative: {file_path}")
                    
                    all_files.append(file_path)
        
        data_files[dataset_name] = all_files
    
    # Save the data_files.json
    with open("data_files.json", "w") as f:
        json.dump(data_files, f, indent=4)
    
    print(f"Created data_files.json with {sum(len(files) for files in data_files.values())} total OBJ files")
    
    # Output info about datasets
    for dataset_name, files in data_files.items():
        print(f"  - {dataset_name}: {len(files)} OBJ files")
    
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate data_files.json containing paths to OBJ files")
    parser.add_argument("--relative", action="store_true", help="Generate relative paths instead of absolute paths")
    parser.add_argument("--server-root", type=str, default=os.getcwd(),
                        help="Server root directory to use for relative path calculation (default: current dir)")
    
    args = parser.parse_args()
    
    print(f"Generating data_files.json...")
    if args.relative:
        print(f"Using relative paths relative to: {args.server_root}")
    else:
        print("Using absolute paths (may not work in browser)")
    
    create_data_files(use_relative_paths=args.relative, server_root=args.server_root)