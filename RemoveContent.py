import os
import shutil

def clear_folder_contents(root_path):
    if not os.path.isdir(root_path):
        raise ValueError(f"The path '{root_path}' is not a valid directory.")

    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)  # Remove file or symbolic link
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Remove directory and all its contents
        except Exception as e:
            print(f"Failed to delete {item_path}: {e}")

if __name__ == "__main__":
    folder_path = "/home/apsu/LegoDetect/Annotated"
    clear_folder_contents(folder_path)
    print(f"Contents of '{folder_path}' have been removed.")
