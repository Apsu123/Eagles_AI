import cv2
import numpy as np
import os
from TestReplace import rewrite_first_char
import random

split = 0.8

def annotate_dataset(root_folder, output_folder):
    train = True
    for dirpath, dirnames, filenames in os.walk(root_folder):

        # Skip the root folder itself
        if dirpath == root_folder:
            continue
        all_files = []
        for dirpath, _, filenames in os.walk(root_folder):
            for filename in filenames:
                if not filename.lower().endswith(".txt"):
                    full_path = os.path.join(dirpath, filename)
                    all_files.append(full_path)
        all_files.sort()
        print(all_files)
        total_files = sum(len(files) for _, _, files in os.walk(root_folder))
        print(total_files)

        for file in all_files:
            print(file)
            filename = os.path.basename(file)
            # Count total files in the current directory
            train_count = int(total_files * split)
            print(train_count)
            if train:
                item = "train"
                train = False
            else:
                item = "valid"
                train = True

            images = os.path.join(output_folder, item, "images")
            labels = os.path.join(output_folder, item, "labels")

            file_path = file

            # Load binary mask: white = object, black = background
            mask = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

            # Ensure it's binary
            _, binary_mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

            # Find contours
            contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Get bounding box from largest contour
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(largest_contour)
                print(f"Bounding box: x={x}, y={y}, w={w}, h={h}")
            else:
                print("No object found in mask")
                return

            # Assuming known image dimensions
            image_height, image_width = mask.shape

            x_center = (x + w / 2) / image_width
            y_center = (y + h / 2) / image_height
            width = w / image_width
            height = h / image_height

            # Create YOLO annotation format

            os.makedirs(labels, exist_ok=True)
            yolo_annotation = f"0 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
            label_file = os.path.join(labels, os.path.splitext(filename)[0] + ".txt")
            with open(label_file, "w") as f:
                f.write(yolo_annotation + "\n")

            # Copy the file to the images folder
            os.makedirs(images, exist_ok=True)
            image_dest = os.path.join(images, filename)
            if not os.path.exists(image_dest):
                with open(file_path, "rb") as src, open(image_dest, "wb") as dst:
                    dst.write(src.read())

            #all_files.remove(file)  # Remove processed file from list


    TRAIN_VAL = ["train", "valid"]

    for item in TRAIN_VAL:
        images = os.path.join(output_folder, item, "images")
        labels = os.path.join(output_folder, item, "labels")

        for file in os.listdir(images):
            if not "NEG" in file:
                class_id = int(file[0])
            label_file = os.path.join(labels, os.path.splitext(file)[0] + ".txt")
            print(label_file)
            if not os.path.exists(label_file):
                continue
            rewrite_first_char(label_file, None, str(class_id))

        for file in os.listdir(images):
            if "NEG" in file:
                label_file = os.path.join(labels, os.path.splitext(file)[0] + ".txt")
                print(label_file)
                open(label_file, "w").close()
    """
    Convert a binary mask to YOLO format annotation.

    :param mask_path: Path to the binary mask image.
    :param class_id: Class ID for the object in the mask.
    :return: YOLO formatted string with bounding box coordinates.
    """

# Load binary mask: white = object, black = background
if __name__ == "__main__":


    annotate_dataset("/home/apsu/Test/Raw", "/home/apsu/FieldTest/DS")
    print("Annotated dataset.")
