import cv2
import os


def ShowBox(image_path, yolo_label_path ):
 # corresponding YOLO annotation file             # how many augmented versions to create

    # === Load Image ===
    image = cv2.imread(image_path)
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width = image.shape[:2]

    # === Load YOLO Annotations ===
    yolo_boxes = []
    with open(yolo_label_path, 'r') as f:
        for line in f.readlines():
            parts = line.strip().split()
            # class_id = int(parts[0])
            x_center, y_center, w, h = map(float, parts[1:])
            yolo_boxes.append([x_center, y_center, w, h])

    # === Prepare for Albumentations ===
    category_ids = [b[0] for b in yolo_boxes]
    bboxes = [b[0:] for b in yolo_boxes]

    print(type(bboxes))
    print(bboxes)
    print(file)

    for box in bboxes:
        x_center = box[0]
        y_center = box[1]
        box_width = box[2]
        box_height = box[3]

        # Denormalize to get pixel values
        x_center *= width
        y_center *= height
        box_width *= width
        box_height *= height

        # Calculate top-left and bottom-right corners
        x1 = int(x_center - box_width / 2)
        y1 = int(y_center - box_height / 2)
        x2 = int(x_center + box_width / 2)
        y2 = int(y_center + box_height / 2)

        # Load the image

        # Draw the rectangle
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Show or save the image
    cv2.imshow(image_path, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

file = "img.png"
images = "/home/apsu/Test/FOR_BG/FOR_BG.png"
labels = f"/home/apsu/Test/Modified/train/labels/aug_68.txt"

ShowBox(images, labels)