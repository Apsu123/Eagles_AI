import os
from PIL import Image

def add_jpg_extension(folder_path):
    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)

        # Skip directories
        if os.path.isdir(full_path):
            continue

        # Skip files that already end with .jpg
        if filename.lower().endswith('.jpg') or filename.lower().endswith('.png') or filename.lower().endswith('.webp') or filename.lower().endswith('.jpeg'):
            continue

        else:
            image = Image.open(full_path)
            # Get the format
            format = image.format.lower()
            new_filename = filename + "." + str(format)

            new_full_path = os.path.join(folder_path, new_filename)

            os.rename(full_path, new_full_path)

            print(f"Renamed: {filename} -> {new_filename}")

# Example usage



folder = os.path.join("/home/apsu/PexelsWallpapers")
add_jpg_extension(folder)
