import os
from PIL import Image
import random
from Convert import convert_to_png
import shutil

def add_background_to_foreground(
    background_path,
    foreground_path,
    output_image_path,
):
    # Load images
    try:
        background = Image.open(background_path).convert("RGBA")
        foreground = Image.open(foreground_path).convert("RGBA")
    except (Image.UnidentifiedImageError, FileNotFoundError) as e:
        print(f"Error loading images file: {foreground_path}:", e)
        if os.path.exists(background_path):
            os.remove(background_path)
        return
    # Paste foreground onto background at (0, 0) using alpha channel as mask
    background.paste(foreground, foreground)
    background.save(output_image_path)

if __name__ == "__main__":

    """
        background_files = os.listdir("/home/apsu/Test/Backgrounds")

        TRAIN_VAL = ["train", "valid"]
        output_folder = "/home/apsu/TestSet"
        input_folder = "/home/apsu/Test/Modified"
        background_path = "/home/apsu/Test/Backgrounds"
    
        for item in TRAIN_VAL:
            out_images = os.path.join(output_folder, item, "images")
            out_labels = os.path.join(output_folder, item, "labels")

            in_images = os.path.join(input_folder, item, "images")
            in_labels = os.path.join(input_folder, item, "labels")

            os.makedirs(out_images, exist_ok=True)

            for file in os.listdir(in_images):

                foreground_path = os.path.join(in_images, file)
                label_path = os.path.join(in_labels, os.path.splitext(file)[0] + ".txt")

                shutil.copy(label_path, out_labels)

                background_file = random.choice(background_files)
                output_image_path = os.path.join(out_images, file)

                bg_path = os.path.join(background_path, background_file)

                if os.path.exists(label_path):
                    add_background_to_foreground(
                        background_path=bg_path,
                        foreground_path=foreground_path,
                        output_image_path=output_image_path,
                    )"""


"""
CONVERT JPG TO PNG AND DELETE OLD FILES


            for file in os.listdir(in_images):
                if not file.lower().endswith('.png'):
                    convert_jpg_to_png(
                        input_jpg_path=os.path.join(in_images, file),
                        output_png_path=os.path.join(in_images, os.path.splitext(file)[0] + ".png")
                    )"""

"""
DELETE ALL NON-PNG FILES IN BACKGROUND FOLDER
background_files = os.listdir("/home/apsu/Test/Backgrounds")

for file in background_files:
    if not file.lower().endswith('.png'):
      os.remove(os.path.join(str("/home/apsu/Test/Backgrounds/"),file))
"""

