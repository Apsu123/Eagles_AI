import os
import shutil
import argparse

def clear_folder_contents(root_path):
    if not os.path.isdir(root_path):
        raise ValueError(f"The path '{root_path}' is not a valid directory.")

    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        except Exception as e:
            print(f"Failed to delete {item_path}: {e}")

def clear_file_content(file_path):
    """Remove all content from the specified text file."""
    if not os.path.isfile(file_path):
        raise ValueError(f"The path `{file_path}` is not a valid file.")
    with open(file_path, "w"):
        pass

def copy_folder_contents(src_folder, dest_folder):
    """
    Copy all contents from src_folder to dest_folder.
    """
    if not os.path.isdir(src_folder):
        raise ValueError(f"The path '{src_folder}' is not a valid directory.")
    os.makedirs(dest_folder, exist_ok=True)
    for item in os.listdir(src_folder):
        src_item = os.path.join(src_folder, item)
        dest_item = os.path.join(dest_folder, item)
        if os.path.isdir(src_item):
            shutil.copytree(src_item, dest_item, dirs_exist_ok=True)
        else:
            shutil.copy2(src_item, dest_item)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clear contents of specified directories.")
    parser.add_argument("folders", nargs="+", help="Paths of folders to clear")

    args = parser.parse_args()

    for folder_path in args.folders:
        try:
            clear_folder_contents(folder_path)
            print(f"Contents of '{folder_path}' have been removed.")
        except Exception as e:
            print(f"Error clearing '{folder_path}': {e}")
