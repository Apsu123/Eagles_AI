import cv2
import albumentations as A
import matplotlib.pyplot as plt
import os
import numpy as np


def augment_dataset(images_dir, labels_dir, num_augmented=5):
    count = 0
    for file in os.listdir(images_dir):
        image_path = os.path.join(images_dir, file)
        yolo_label_path = os.path.join(labels_dir, os.path.splitext(file)[0] + ".txt")

        # === Load Image (with alpha if present) ===
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if image is None:
            continue
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

        # === Load YOLO Annotations ===
        yolo_boxes = []
        with open(yolo_label_path, 'r') as f:
            for line in f.readlines():
                parts = line.strip().split()
                class_id = int(parts[0])
                x_center, y_center, w, h = map(float, parts[1:])
                yolo_boxes.append([class_id, x_center, y_center, w, h])

        # === Prepare for Albumentations ===
        category_ids = [b[0] for b in yolo_boxes]
        bboxes = [b[1:] for b in yolo_boxes]

        # === Define Augmentation ===
        transform = A.Compose([
            A.HorizontalFlip(p=0.5),
            A.Rotate(limit=20, p=0.5),
            A.Affine(scale=(0.1), translate_percent={"x": (-0.4, 0.4), "y": (-0.4, 0.4)}, fit_output=False, p=1),
            A.RandomBrightnessContrast(brightness_limit=(-0.2,0.2), contrast_limit=0, p=1),
        ], bbox_params=A.BboxParams(format='yolo', label_fields=['category_ids']))

        # === Augmentation Loop ===
        for i in range(num_augmented):
            print(image_path)
            try:
                aug = transform(image=image_rgb, bboxes=bboxes, category_ids=category_ids)
            except ValueError as e:
                print(f"ValueError for {image_path}: {e}")
                # Remove problematic image and label files
                if os.path.exists(image_path):
                    os.remove(image_path)
                if os.path.exists(yolo_label_path):
                    os.remove(yolo_label_path)
                break  # Skip further augmentation for this file

            aug_image = aug['image']
            aug_bboxes = aug['bboxes']
            aug_ids = aug['category_ids']

            # Save image as PNG to preserve transparency
            output_image_path = os.path.join(images_dir, f'aug_{count + i}.png')
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

            # Save YOLO annotation
            output_txt_path = os.path.join(labels_dir, f'aug_{count + i}.txt')
            with open(output_txt_path, 'w') as f:
                for cls, box in zip(aug_ids, aug_bboxes):
                    x, y, w, h = box
                    f.write(f"{cls} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n")

        count += num_augmented

        print(f"✅ Saved {num_augmented} augmented images to: {images_dir}")
        print(f"✅ Saved {num_augmented} augmented labels to: {labels_dir}")
        print("✅ Removed original image:", image_path)


if __name__ == "__main__":

    TRAIN_VAL = ["train", "valid"]
    output_folder = "/home/apsu/Test/Modified"

    for item in TRAIN_VAL:
        images = os.path.join(output_folder, item, "images")
        labels = os.path.join(output_folder, item, "labels")

        print(images, labels)

        augment_dataset(
            images_dir=images,
            labels_dir=labels,
            num_augmented=5
        )
