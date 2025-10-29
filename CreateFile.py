import os
from os import mkdir

import data
from data import updated_files, old_files


def create_and_write_file(directory, filename, content):
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    # Construct full file path
    filepath = os.path.join(directory, filename)

    # Write content to the file
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)

    print(f"File created at: {filepath}")

def clear_file_contents(filepath):
    try:
        # Open the file in write mode to truncate its contents
        with open(filepath, 'w', encoding='utf-8') as file:
            pass  # Writing nothing effectively clears the file
        print(f"Contents of '{filepath}' have been cleared.")
    except FileNotFoundError:
        print(f"File not found: {filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")


base_path = "/home/apsu/LearningHub/"

def WriteFile(filepath, content):
    try:
        # Open the file in write mode to truncate its contents
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"File '{filepath}' rewritten.")
    except FileNotFoundError:
        print(f"File not found: {filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")


for path, content in updated_files.items():
    Path = os.path.join(base_path, path)
    if os.path.isfile(Path):
        WriteFile(Path, content)
    else:
        create_and_write_file(base_path, path, content)

old_files = updated_files
