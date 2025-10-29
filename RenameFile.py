import os
from PIL import Image

def add_extension(folder_path):
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
            if format == 'jpeg':
                format = 'jpg'
            new_filename = filename + "." + format

            new_full_path = os.path.join(folder_path, new_filename)

            os.rename(full_path, new_full_path)

            print(f"Renamed: {filename} -> {new_filename}")

def process_rename(serials_path, base_folder):
    with open(serials_path, 'r') as file:
        # Loop through each line in the file
        for line_number, line in enumerate(file, start=1):
            # Remove trailing newline characters
            clean_line = line.strip()

            folder = os.path.join(base_folder, line)
            add_extension(folder)

# Example usage
if __name__ == "__main__":

    add_extension(
        folder_path="/home/apsu/FuturisticBGS"
    )


    """
    FOR EAGLE'S AI
    
        TRAIN_VAL = ["train", "valid"]
        output_folder = "/home/apsu/Test/Modified"
    
        for item in TRAIN_VAL:
            images = os.path.join(output_folder, item, "images")
    
            add_extension(
                folder_path=images
            )"""
