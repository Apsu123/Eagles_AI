import cv2
import os


def show_boxes_on_images(annotated_dir, train_val):
    for item in train_val:
        images = os.path.join(annotated_dir, item, "images")
        labels = os.path.join(annotated_dir, item, "labels")
        for file in os.listdir(images):
            image_path = os.path.join(images, file)
            yolo_label_path = os.path.join(labels, os.path.splitext(file)[0] + ".txt")
            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width = image.shape[:2]
            yolo_boxes = []
            with open(yolo_label_path, 'r') as f:
                for line in f.readlines():
                    parts = line.strip().split()
                    x_center, y_center, w, h = map(float, parts[1:])
                    Class = parts[0]
                    yolo_boxes.append([x_center, y_center, w, h])
            bboxes = [b[0:] for b in yolo_boxes]
            print(type(bboxes))
            print(bboxes)
            print(file)
            for box in bboxes:
                x_center = box[0]
                y_center = box[1]
                box_width = box[2]
                box_height = box[3]
                x_center *= width
                y_center *= height
                box_width *= width
                box_height *= height
                x1 = int(x_center - box_width / 2)
                y1 = int(y_center - box_height / 2)
                x2 = int(x_center + box_width / 2)
                y2 = int(y_center + box_height / 2)
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.imshow(str(image_path), image)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()

if __name__ == "__main__":
    show_boxes_on_images(
        annotated_dir="/home/apsu/FieldTest/DS",
        train_val=["train", "valid"]
    )
