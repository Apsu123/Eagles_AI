import os

def remove_text_files(root_folder):
    """
    Remove all .txt files from the specified root folder and its subdirectories.

    :param root_folder: The root directory from which to remove .txt files.
    """
    if not os.path.isdir(root_folder):
        raise ValueError(f"The path '{root_folder}' is not a valid directory.")

    for dirpath, dirnames, filenames in os.walk(root_folder):
        for file in filenames:
            if file.endswith(".txt"):
                file_path = os.path.join(dirpath, file)
                os.remove(file_path)

if __name__ == "__main__":

    root_folder = "/home/apsu/Test/Raw"
    remove_text_files(root_folder)
