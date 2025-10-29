import os

def list_subfolders(root_dir):
    for entry in os.listdir(root_dir):
        full_path = os.path.join(root_dir, entry)
        if os.path.isdir(full_path):
            print(f"Folder: {entry}")

def main(root_directory):
    list_subfolders(root_directory)

# Replace with your desired root directory
if __name__ == "__main__":
    root_directory = "/home/apsu/LegoDetect/TestSet"
    main(root_directory)
