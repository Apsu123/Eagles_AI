import cv2
import os
from PIL import Image

def resize_image(image_path, width=640, height=640):
    # Load the image with OpenCV
    img_cv = cv2.imread(image_path)

    if img_cv is None:
        print(f"Error: Could not read image {image_path}")
        return

    # Resize the image
    resized = cv2.resize(img_cv, (width, height), interpolation=cv2.INTER_CUBIC)

    # Save the resized image back to the same path
    cv2.imwrite(image_path, resized)



def resize_and_rename_images(root_folder, serials_path, width=640, height=640):
    image_id = 0
    class_id = 0
    bg_idx = 0
    is_positive = True

    classes = []
    with open(serials_path, 'r') as lines:
        serials = [line.strip() for line in lines if line.strip()]
        for line in serials:

            if "neg" in serials_path:
                dir_path = os.path.join(root_folder, f"NEG{line}")

            else:
                dir_path = os.path.join(root_folder, line)


            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    file_path = os.path.join(root, file)

                    # open with PIL to get the original format
                    img_pil = Image.open(file_path)
                    fmt = img_pil.format.lower()
                    if fmt == "jpeg":
                        fmt = "jpg"

                    if "NEG" in file_path:
                        new_file = f"NEG_{image_id}_img.{fmt}"
                        is_positive = False

                    elif "Background" in file_path:

                        new_file = f"BG{bg_idx}.{fmt}"
                        bg_idx += 1

                    else:

                        new_file = f"{class_id}_{image_id}_img.{fmt}"

                    print(file_path)
                    print(new_file)
                    image_id += 1

                    # load with OpenCV, resize, and overwrite
                    img_cv = cv2.imread(str(file_path))
                    resized = cv2.resize(img_cv, (width, height), interpolation=cv2.INTER_CUBIC)

                    if os.path.isfile(file_path):
                        os.remove(file_path)

                    cv2.imwrite(os.path.join(dir_path, new_file), resized)

                if is_positive:
                    class_id += 1


if __name__ == "__main__":
    root_folder = "/home/apsu/Predict/RealWordTest"

    for filename in os.listdir(root_folder):
        path = os.path.join(root_folder, filename)
        resize_image(path)
