import cv2
import os
net = cv2.dnn_TextDetectionModel_EAST("frozen_east_text_detection.pb")
net.setInputParams(1.0, (320,320), (123.68,116.78,103.94), True)
net.setNMSThreshold(0.4)
net.setConfidenceThreshold(0.9)

if cv2.cuda.getCudaEnabledDeviceCount() > 0:
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
else:
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

for file in os.listdir("/home/apsu/Futuristic_Wallpapers (Copy)"):
    file_path = os.path.join("/home/apsu/Futuristic_Wallpapers (Copy)", file)

    boxes, _ = net.detect(cv2.imread(file_path))
    has_text = len(boxes)>0
    if has_text:
        print(f"Text detected in {file}")
        os.remove(file_path)
    else:
        print(f"No text detected in {file}")