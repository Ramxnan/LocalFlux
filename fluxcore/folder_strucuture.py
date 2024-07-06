import os

def print_directory_tree(root_dir, indent=''):
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        if os.path.isdir(item_path):
            print(f"{indent}├── {item}")
            print_directory_tree(item_path, indent + "│   ")
        else:
            print(f"{indent}└── {item}")

# Replace 'path/to/directory' with the actual directory path
directory_path = 'C:\\Users\\raman\\OneDrive - Amrita vishwa vidyapeetham\\ASE\\Projects\\NBA\\NBA_v3\\dev_19.1\\flux\\nba'
print_directory_tree(directory_path)