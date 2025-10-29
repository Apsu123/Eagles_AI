import os
import cv2
from rembg import remove
import numpy as np
import albumentations as A
import argparse
import csv
import random
from Get_Images import get_images_with_colors2, download_image as download_image2
from AddBG import add_background_to_foreground
from transparent import make_image_transparent
from Resize import resize_image
from PIL import Image
from GetIDS import serials
from RemoveContent import clear_folder_contents, clear_file_content, copy_folder_contents


def get_random_cell_from_column_a(csv_path):
    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        column_a = [row[0] for row in reader if row]
        # Skip empty rows
    if not column_a:
        return None
    return str(random.choice([cell for cell in column_a if cell.isdigit()]))


# === Main Augmentation Function ===
def augment_image2(image_path, output_dir, num_augmented, idx):
    count = 0
    # === Load Image (with alpha if present) ===
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        return
    if image.shape[-1] == 4:
        # RGBA image
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
    else:
        # No alpha, treat as RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Add alpha channel (fully opaque)
        alpha_channel = np.ones(image_rgb.shape[:2], dtype=np.uint8) * 255
        image_rgb = np.dstack((image_rgb, alpha_channel))
    height, width = image_rgb.shape[:2]

    # === Define Augmentation ===
    transform = A.Compose([
        A.RandomBrightnessContrast(brightness_limit=0.3, contrast_limit=0, p=1),
        # A.HorizontalFlip(p=0.5),
        # A.Rotate(limit=20, p=0.5),
        # A.Affine(scale=(0.1, 0.3), translate_percent={"x": (-0.5, 0.5), "y": (-0.5, 0.5)}, fit_output=False, p=1),
    ])

    # === Augmentation Loop ===
    for i in range(num_augmented):
        print(image_path)
        try:
            aug = transform(image=image_rgb)
        except ValueError as e:
            print(f"ValueError for {image_path}: {e}")
            # Remove problematic image and label files
            if os.path.exists(image_path):
                os.remove(image_path)
            break  # Skip further augmentation for this file

        aug_image = aug['image']

        # Save image as PNG to preserve transparency
        output_image_path = os.path.join(output_dir, f'aug_{idx}_{i}.png')
        # Ensure RGBA order for saving
        if aug_image.shape[-1] == 4:
            aug_image_bgra = cv2.cvtColor(aug_image, cv2.COLOR_RGBA2BGRA)
        else:
            # Add alpha if missing
            rgb = aug_image[..., :3]
            alpha = np.ones(rgb.shape[:2], dtype=np.uint8) * 255
            aug_image_bgra = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
            aug_image_bgra = np.dstack((aug_image_bgra, alpha))
        cv2.imwrite(output_image_path, aug_image_bgra)

    count += num_augmented

    print(f"✅ Saved {num_augmented} augmented images to: {output_dir}")



def augment_image(image_path, output_dir, num_augmented, idx):
    count = 0
    # === Load Image (with alpha if present) ===
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        return
    if image.shape[-1] == 4:
        # RGBA image
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
    else:
        # No alpha, treat as RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Add alpha channel (fully opaque)
        alpha_channel = np.ones(image_rgb.shape[:2], dtype=np.uint8) * 255
        image_rgb = np.dstack((image_rgb, alpha_channel))
    height, width = image_rgb.shape[:2]

    # === Define Augmentation ===
    transform = A.Compose([
        A.HorizontalFlip(p=0.5),
        A.Rotate(limit=20, p=0.5),
        A.Affine(scale=(0.1, 0.3), translate_percent={"x": (-0.5, 0.5), "y": (-0.5, 0.5)}, fit_output=False, p=1),
    ])

    # === Augmentation Loop ===
    for i in range(num_augmented):
        print(image_path)
        try:
            aug = transform(image=image_rgb)
        except ValueError as e:
            print(f"ValueError for {image_path}: {e}")
            # Remove problematic image and label files
            if os.path.exists(image_path):
                os.remove(image_path)
            break  # Skip further augmentation for this file

        aug_image = aug['image']

        # Save image as PNG to preserve transparency
        output_image_path = os.path.join(output_dir, f'aug_{idx}_{i}.png')
        # Ensure RGBA order for saving
        if aug_image.shape[-1] == 4:
            aug_image_bgra = cv2.cvtColor(aug_image, cv2.COLOR_RGBA2BGRA)
        else:
            # Add alpha if missing
            rgb = aug_image[..., :3]
            alpha = np.ones(rgb.shape[:2], dtype=np.uint8) * 255
            aug_image_bgra = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
            aug_image_bgra = np.dstack((aug_image_bgra, alpha))
        cv2.imwrite(output_image_path, aug_image_bgra)

    count += num_augmented

    print(f"✅ Saved {num_augmented} augmented images to: {output_dir}")


if __name__ == "__main__":
    for i in range(2):
        num_negatives = 50
        NegativeParts = f"/home/apsu/FieldTest/NegativeParts1"
        Negatives_TXT = f"/home/apsu/FieldTest/negatives4.txt"
        Backgrounds = f"/home/apsu/FieldTest/Backgrounds{4+i}"
        clear_folder_contents(NegativeParts)
        #clear_folder_contents(Backgrounds)
        clear_file_content(Negatives_TXT)
        #copy_folder_contents("/home/apsu/FieldTest/Backgrounds4 (Copy)", Backgrounds)
        print(serials)

        IDS = [3023, 3024, 4073, 2780, 54200, 3069, 3004, 3710, 3005, 3020,
               3022, 2412, 6558, 15573, 98138, 3021, 3070, 3003, 3666, 3623,
               11477, 2431, 85984, 4274, 3010, 3001, 3062, 2420, 15068, 43093,
               87580, 3795, 3068, 87079, 3040, 4032, 6636, 15712, 87087, 85861,
               32062, 3622, 4589, 4070, 33291, 3941, 3009, 3460, 99780, 32123,
               63864, 99207, 32028, 4085, 32054, 6091, 11211, 4162, 3039, 2654,
               44728, 3700, 2357, 3660, 3034, 3665, 3713, 4519, 59443, 41740,
               63868, 60478, 98283, 92280, 48336, 30136, 22885, 32064, 92946,
               99206, 99781, 24866, 50950, 61409, 2877, 93273, 3031, 61252,
               25269, 3002, 6541, 4477, 18654, 3673, 11214, 30414, 3245, 62462,
               6536, 32523, 2540, 14769, 88323, 32316, 48729, 53451, 3032, 87994,
               32140, 60483, 32524, 4740, 32000, 60470, 2456, 3832, 4286, 30374,
               32526, 32013, 61678, 24201, 2429, 64567, 64644, 41677, 60474,
               87552, 3065, 40490, 32278, 51739, 60479, 11090, 60592, 18674,
               49668, 18677, 2432, 15392, 3937, 63965, 2450, 3035, 85080, 15535,
               10247, 32525, 2436, 3037, 14704, 15070, 43722, 3958, 298,
               30241, 2453, 32952, 33183, 60477, 60596, 24246, 15462, 3680, 64647,
               60581, 3709, 13547, 6589, 6112, 23969, 3702, 30237, 88930, 32016,
               92950, 32018, 4510, 61184, 60471, 47905, 13965, 11478, 30553,
               41539, 98100, 32530, 30236, 30028, 94925, 75937, 99021, 25214,
               89522, 60485, 18575, 3633, 16770, 32192, 15400, 15461, 56145,
               4600, 4865, 3679, 22888, 50745, 2496, 32056, 87609, 6629, 60476,
               50304, 50305, 32063, 3938, 15332, 30363, 92013, 87081, 32001,
               30165, 64782, 64179, 90194, 13548, 15458, 64799, 32348, 32474,
               2343, 14419, 98282, 2723, 3942, 92907, 3831, 3830, 15391, 30552,
               57895, 6106, 50951, 4490, 32018, 30162, 36841, 87414, 22667,
               30176, 47398, 32014, 30031, 15456, 58247, 3960, 92410, 92738,
               11946, 37352, 76766, 52031, 41854, 3648, 18948, 2462, 92099, 11209]

        for i in range(num_negatives):
            neg = str(random.choice(IDS))
            if neg not in serials:
                print(neg)
                with open(Negatives_TXT, "a") as f:
                    f.write(f"{neg}\n")
            else:
                num_negatives += 1

        get_images_with_colors2(Negatives_TXT, NegativeParts)

        for filename in os.listdir(NegativeParts):
            image_path = (os.path.join(NegativeParts, filename))
            image = Image.open(str(image_path))
            # Get the format
            format = image.format.lower()

            if not filename.endswith("." + format):
                # No extension, add the format as extension
                new_filename = f"{os.path.splitext(filename)[0]}.{format}"
                new_image_path = os.path.join(NegativeParts, new_filename)
                image.save(new_image_path)
                os.remove(image_path)
                image_path = new_image_path

            resize_image(image_path)  # Remove original file if it exists

            num_augmented = 5
        for filename in os.listdir(NegativeParts):
            image_path = os.path.join(NegativeParts, filename)
            make_image_transparent(image_path, image_path)

            augment_image(image_path, NegativeParts, num_augmented, filename)
            os.remove(image_path)

        for filename in os.listdir(Backgrounds):
            print(filename)
            background_path = os.path.join(Backgrounds, filename)
            resize_image(background_path)

        for filename in os.listdir(Backgrounds):
            background_path = os.path.join(Backgrounds, filename)
            for i in range(50):
                neg_images = os.listdir(NegativeParts)
                neg_image = random.choice(neg_images)
                neg_image_path = os.path.join(NegativeParts, neg_image)
                add_background_to_foreground(background_path, neg_image_path, os.path.splitext(background_path)[0] + ".png")