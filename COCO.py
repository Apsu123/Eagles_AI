import os
import json
from PIL import Image

# Paths
images_dir = "/home/apsu/FieldTest/DS5/valid/images"
labels_dir = "/home/apsu/FieldTest/DS5/valid/labels"
classes_file = "/home/apsu/FieldTest/classes.txt"
output_json = "/home/apsu/FieldTest/valid_faster_rcnn_coco.json"

# Load classes
with open(classes_file) as f:
    classes = [line.strip() for line in f.readlines()]

# Initialize COCO structure
coco = {
    "images": [],
    "annotations": [],
    "categories": [{"id": i, "name": name} for i, name in enumerate(classes)]
}

image_id = 1
annotation_id = 1

for label_file in os.listdir(labels_dir):
    print(f"Processing label file: {label_file}")
    if not label_file.endswith(".txt"):
        continue

    image_name = label_file.replace(".txt", ".png")
    image_path = os.path.join(images_dir, image_name)
    if not os.path.exists(image_path):
        continue

    # Image info
    img = Image.open(image_path)
    w, h = img.size
    coco["images"].append({"id": image_id, "file_name": image_name, "width": w, "height": h})

    # Parse labels
    with open(os.path.join(labels_dir, label_file)) as f:
        for line in f:
            cls_id, x, y, bw, bh = map(float, line.split())
            cls_id = int(cls_id)

            print(f"Processing annotation: class_id={cls_id}, x={x}, y={y}, bw={bw}, bh={bh}")

            # Convert to absolute coords
            x_min = (x - bw/2) * w
            y_min = (y - bh/2) * h
            width = bw * w
            height = bh * h

            coco["annotations"].append({
                "id": annotation_id,
                "image_id": image_id,
                "category_id": cls_id,
                "bbox": [x_min, y_min, width, height],
                "area": width * height,
                "iscrowd": 0
            })
            annotation_id += 1

    image_id += 1

# Save JSON
with open(output_json, "w") as f:
    json.dump(coco, f, indent=2)

print(f"Saved COCO annotations to {output_json}")
