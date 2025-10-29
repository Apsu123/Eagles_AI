import cv2
import numpy as np
import os


def remove_background_from_folder(folder_path):
            """   for filename in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, filename)
                    if os.path.isfile(file_path):"""

            # Process the file
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    image = cv2.imread(file_path)
                    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                    # Define lower and upper bounds of the background color
                    lower = np.array([240, 240, 240])  # Light gray/white
                    upper = np.array([255, 255, 255])

                    # Create a mask where background pixels are white
                    mask = cv2.inRange(rgb, lower, upper)

                    # Invert mask to get the foreground
                    foreground_mask = cv2.bitwise_not(mask)

                    # Use morphological operations to clean noise
                    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
                    cleaned_mask = cv2.morphologyEx(foreground_mask, cv2.MORPH_OPEN, kernel)
                    cleaned_mask = cv2.morphologyEx(cleaned_mask, cv2.MORPH_DILATE, kernel)

                    # Mask the original image
                    segmented = cv2.bitwise_and(rgb, rgb, mask=cleaned_mask)

                    cv2.imwrite(file_path, cv2.cvtColor(segmented, cv2.COLOR_RGB2BGR))

                    if image is None:
                        print(f"Could not read image: {file_path}")
                        continue

            # Convert to RGB and grayscale

if __name__ == "__main__":

    """

    for subfolder in os.listdir('/home/apsu/FieldTest/Raw'):
        subfolder_path = os.path.join('/home/apsu/FieldTest/Raw', subfolder)
        if os.path.isdir(subfolder_path):"""

#remove_background_from_folder("/home/apsu/lego-black-lord-garmadon-legacy-minifig-torso-973-76382-1708133.jpg")
