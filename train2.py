from ultralytics import YOLO

model = YOLO("yolov8s.yaml")

model.train(data="/home/apsu/FieldTest/DS5/data.yaml", epochs=100, patience=25, device=0)