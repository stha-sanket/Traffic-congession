# import cv2
# import numpy as np

# # Load YOLO model
# net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')
# layer_names = net.getLayerNames()
# output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# # Load class names
# with open("coco.names", "r") as f:
#     classes = [line.strip() for line in f.readlines()]

# # Define function to count vehicles
# def count_vehicles(detections, class_ids):
#     vehicle_classes = ["car", "motorbike", "bus", "truck"]
#     vehicle_count = 0
#     for class_id in class_ids:
#         if classes[class_id] in vehicle_classes:
#             vehicle_count += 1
#     return vehicle_count

# # Start video capture (0 for webcam or replace with video file path)
# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Preprocess the frame for YOLO
#     height, width, channels = frame.shape
#     blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
#     net.setInput(blob)
#     detections = net.forward(output_layers)

#     # Parse YOLO outputs
#     class_ids = []
#     confidences = []
#     boxes = []
#     for output in detections:
#         for detection in output:
#             scores = detection[5:]
#             class_id = np.argmax(scores)
#             confidence = scores[class_id]
#             if confidence > 0.5:  # Confidence threshold
#                 center_x = int(detection[0] * width)
#                 center_y = int(detection[1] * height)
#                 w = int(detection[2] * width)
#                 h = int(detection[3] * height)
#                 x = int(center_x - w / 2)
#                 y = int(center_y - h / 2)
#                 boxes.append([x, y, w, h])
#                 confidences.append(float(confidence))
#                 class_ids.append(class_id)

#     # Non-max suppression to eliminate redundant overlapping boxes
#     indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
#     vehicle_count = count_vehicles([boxes[i] for i in indexes.flatten()], [class_ids[i] for i in indexes.flatten()])

#     # Draw bounding boxes and labels
#     for i in indexes.flatten():
#         x, y, w, h = boxes[i]
#         label = f"{classes[class_ids[i]]}: {int(confidences[i] * 100)}%"
#         color = (0, 255, 0)  # Green for bounding boxes
#         cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
#         cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

#     # Display vehicle count on the frame
#     cv2.putText(frame, f"Vehicle Count: {vehicle_count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

#     # Show frame
#     cv2.imshow("Vehicle Detection and Counting", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
#         break

# cap.release()
# cv2.destroyAllWindows()

import cv2
import numpy as np
import requests

# Load YOLO model
net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Load class names
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Define function to count vehicles
def count_vehicles(detections, class_ids, region_x_split):
    vehicle_classes = ["car", "motorbike", "bus", "truck"]
    road1_count = 0
    road2_count = 0
    for i, class_id in enumerate(class_ids):
        if classes[class_id] in vehicle_classes:
            x, y, w, h = detections[i]
            center_x = x + w // 2
            if center_x < region_x_split:  # Vehicles on road 1
                road1_count += 1
            else:  # Vehicles on road 2
                road2_count += 1
    return road1_count, road2_count

# Start video capture (0 for webcam or replace with video file path)
cap = cv2.VideoCapture(0)

ESP32_URL = "http://172.16.1.124
"  # Replace with your ESP32's IP address

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess the frame for YOLO
    height, width, channels = frame.shape
    region_x_split = width // 2  # Split frame into two regions for two roads
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    detections = net.forward(output_layers)

    # Parse YOLO outputs
    class_ids = []
    confidences = []
    boxes = []
    for output in detections:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:  # Confidence threshold
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Non-max suppression to eliminate redundant overlapping boxes
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    detections_filtered = [boxes[i] for i in indexes.flatten()]
    class_ids_filtered = [class_ids[i] for i in indexes.flatten()]

    # Count vehicles on both roads
    road1_count, road2_count = count_vehicles(detections_filtered, class_ids_filtered, region_x_split)

    # Send HTTP request to ESP32 based on vehicle counts
    if road1_count > road2_count:
        requests.get(f"{ESP32_URL}?road=1")  # Turn on traffic light for road 1
    elif road2_count > road1_count:
        requests.get(f"{ESP32_URL}?road=2")  # Turn on traffic light for road 2

    # Draw bounding boxes and labels
    for i in indexes.flatten():
        x, y, w, h = boxes[i]
        label = f"{classes[class_ids[i]]}: {int(confidences[i] * 100)}%"
        color = (0, 255, 0)  # Green for bounding boxes
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Display vehicle count on the frame
    cv2.putText(frame, f"Road 1: {road1_count} | Road 2: {road2_count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Show frame
    cv2.imshow("Vehicle Detection and Counting", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
