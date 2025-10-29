from ultralytics import YOLO
import cv2
import os

model = YOLO("Small.pt")

new = True
show = True
images_dir = "/home/apsu/Predict/Test2"

count = 0


for file in os.listdir(images_dir):
    image_path = os.path.join(images_dir, file)

    results = model(source=image_path, show=True, conf=0.05, save=show)

if show:
    print("Now showing the predictions...")

    for file in os.listdir("/home/apsu/TrainModel/runs/detect/predict14"):

        image_path = os.path.join("/home/apsu/TrainModel/runs/detect/predict14", file)
        # Load the image
        image = cv2.imread(image_path)

        scale_x = 0.5  # Scale width to 50%
        scale_y = 0.5  # Scale height to 50%

        # Resize the image
        #image = cv2.resize(image, None, fx=scale_x, fy=scale_y, interpolation=cv2.INTER_LINEAR)

        # Display the image in a window
        cv2.imshow('Image Window', image)

        # Wait for a specific time (e.g., 2000 milliseconds = 2 seconds)
        cv2.waitKey(0)

        # Close all OpenCV windows
        cv2.destroyAllWindows()
