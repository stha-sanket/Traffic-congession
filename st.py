# import os
# import cv2
# import numpy as np
# import streamlit as st
# import time

# # Load YOLO model
# net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')
# layer_names = net.getLayerNames()
# output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# # Load class names
# with open("coco.names", "r") as f:
#     classes = [line.strip() for line in f.readlines()]

# # Function to count vehicles
# def count_vehicles(detections, class_ids):
#     vehicle_classes = ["car", "motorbike", "bus", "truck"]
#     vehicle_count = 0
#     for class_id in class_ids:
#         if classes[class_id] in vehicle_classes:
#             vehicle_count += 1
#     return vehicle_count

# # Streamlit UI
# st.title("YOLO Object Detection with Vehicle Counting & Labeling")

# # Placeholder for the video feed
# stframe = st.empty()

# # Create a placeholder for the vehicle count that will be updated in place
# vehicle_count_placeholder = st.empty()

# # Initialize vehicle count
# vehicle_count = 0  

# # Video Upload
# video_file = st.file_uploader("Upload Video", type=['mp4', 'avi', 'mov', 'mkv'])

# # Frame skip setting
# frame_skip = 6  # Skip every 5 frames (process every 6th frame)

# # Handle video upload and processing
# if video_file is not None:
#     # Save the uploaded video temporarily
#     video_path = os.path.join("uploads", video_file.name)
#     with open(video_path, "wb") as f:
#         f.write(video_file.read())

#     # Open the uploaded video file
#     cap = cv2.VideoCapture(video_path)

#     frame_counter = 0  # Frame counter to skip frames

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         frame_counter += 1
#         if frame_counter % frame_skip != 0:
#             continue  # Skip every 5th frame

#         # Reduce resolution of the frame (resize to 640x480 or lower if needed)
#         frame = cv2.resize(frame, (640, 480))

#         # Resize to 416x416 for YOLO inference to speed up processing
#         height, width, channels = frame.shape
#         resized_frame = cv2.resize(frame, (416, 416))

#         # Preprocess the frame for YOLO
#         blob = cv2.dnn.blobFromImage(resized_frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
#         net.setInput(blob)
#         detections = net.forward(output_layers)

#         # Parse YOLO outputs
#         class_ids = []
#         confidences = []
#         boxes = []
#         for output in detections:
#             for detection in output:
#                 scores = detection[5:]
#                 class_id = np.argmax(scores)
#                 confidence = scores[class_id]
#                 if confidence > 0.5:  # Confidence threshold
#                     center_x = int(detection[0] * width)
#                     center_y = int(detection[1] * height)
#                     w = int(detection[2] * width)
#                     h = int(detection[3] * height)
#                     x = int(center_x - w / 2)
#                     y = int(center_y - h / 2)
#                     boxes.append([x, y, w, h])
#                     confidences.append(float(confidence))
#                     class_ids.append(class_id)

#         # Non-max suppression to eliminate redundant overlapping boxes
#         indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
#         vehicle_count = count_vehicles([boxes[i] for i in indexes.flatten()], [class_ids[i] for i in indexes.flatten()])

#         # Draw bounding boxes, labels, and confidence
#         for i in indexes.flatten():
#             x, y, w, h = boxes[i]
#             label = f"{classes[class_ids[i]]}: {int(confidences[i] * 100)}%"
#             color = (0, 255, 0)  # Green for bounding boxes
#             cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
#             cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

#         # Display the frame in Streamlit
#         stframe.image(frame, channels="BGR", use_column_width=True)

#         # Update the vehicle count under the video feed (only update value)
#         vehicle_count_placeholder.write(f"Vehicle Count: {vehicle_count}")

#         # Add a small delay to avoid high CPU usage
#         time.sleep(0.1)

#     cap.release()

# # Webcam Stream
# webcam_button = st.button("Start Webcam")

# if webcam_button:
#     stframe = st.empty()  # Create a placeholder for the webcam stream
#     vehicle_count_placeholder = st.empty()  # Create a placeholder for the vehicle count
#     video_streaming = True
#     cap = cv2.VideoCapture(0)  # Use the webcam
    
#     frame_counter = 0  # Frame counter to skip every 5th frame

#     while video_streaming:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         frame_counter += 1
#         if frame_counter % frame_skip != 0:
#             continue  # Skip every 5th frame

#         # Reduce resolution of the frame (resize to 640x480 or lower if needed)
#         frame = cv2.resize(frame, (640, 480))

#         # Resize to 416x416 for YOLO inference to speed up processing
#         height, width, channels = frame.shape
#         resized_frame = cv2.resize(frame, (416, 416))

#         # Preprocess the frame for YOLO
#         blob = cv2.dnn.blobFromImage(resized_frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
#         net.setInput(blob)
#         detections = net.forward(output_layers)

#         # Parse YOLO outputs
#         class_ids = []
#         confidences = []
#         boxes = []
#         for output in detections:
#             for detection in output:
#                 scores = detection[5:]
#                 class_id = np.argmax(scores)
#                 confidence = scores[class_id]
#                 if confidence > 0.5:  # Confidence threshold
#                     center_x = int(detection[0] * width)
#                     center_y = int(detection[1] * height)
#                     w = int(detection[2] * width)
#                     h = int(detection[3] * height)
#                     x = int(center_x - w / 2)
#                     y = int(center_y - h / 2)
#                     boxes.append([x, y, w, h])
#                     confidences.append(float(confidence))
#                     class_ids.append(class_id)

#         # Non-max suppression to eliminate redundant overlapping boxes
#         indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
#         vehicle_count = count_vehicles([boxes[i] for i in indexes.flatten()], [class_ids[i] for i in indexes.flatten()])

#         # Draw bounding boxes, labels, and confidence
#         for i in indexes.flatten():
#             x, y, w, h = boxes[i]
#             label = f"{classes[class_ids[i]]}: {int(confidences[i] * 100)}%"
#             color = (0, 255, 0)  # Green for bounding boxes
#             cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
#             cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

#         # Display the frame in Streamlit
#         stframe.image(frame, channels="BGR", use_column_width=True)

#         # Update the vehicle count under the video feed (only update value)
#         vehicle_count_placeholder.write(f"Vehicle Count: {vehicle_count}")

#         # Add a small delay to avoid high CPU usage
#         time.sleep(0.1)

#     cap.release()

import os
import cv2
import numpy as np
import streamlit as st
import time
import requests  # To send HTTP requests to ESP32

# Load YOLO model
net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Load class names
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Function to count vehicles
def count_vehicles(detections, class_ids):
    vehicle_classes = ["car", "motorbike", "bus", "truck"]
    vehicle_count = 0
    for class_id in class_ids:
        if classes[class_id] in vehicle_classes:
            vehicle_count += 1
    return vehicle_count

# ESP32 IP (replace with your ESP32 IP address)
ESP32_URL = "http://172.16.1.124"  # Example IP, update with actual IP

# Streamlit UI
st.title("YOLO Object Detection with Vehicle Counting & Labeling")

# Placeholder for the video feed
stframe = st.empty()

# Create a placeholder for the vehicle count that will be updated in place
vehicle_count_placeholder = st.empty()

# Initialize vehicle count
vehicle_count = 0  

# Video Upload
video_file = st.file_uploader("Upload Video", type=['mp4', 'avi', 'mov', 'mkv'])

# Frame skip setting
frame_skip = 6  # Skip every 5 frames (process every 6th frame)

# Handle video upload and processing
if video_file is not None:
    # Save the uploaded video temporarily
    video_path = os.path.join("uploads", video_file.name)
    with open(video_path, "wb") as f:
        f.write(video_file.read())

    # Open the uploaded video file
    cap = cv2.VideoCapture(video_path)

    frame_counter = 0  # Frame counter to skip frames

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_counter += 1
        if frame_counter % frame_skip != 0:
            continue  # Skip every 5th frame

        # Reduce resolution of the frame (resize to 640x480 or lower if needed)
        frame = cv2.resize(frame, (640, 480))

        # Resize to 416x416 for YOLO inference to speed up processing
        height, width, channels = frame.shape
        resized_frame = cv2.resize(frame, (416, 416))

        # Preprocess the frame for YOLO
        blob = cv2.dnn.blobFromImage(resized_frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
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
        vehicle_count = count_vehicles([boxes[i] for i in indexes.flatten()], [class_ids[i] for i in indexes.flatten()])

        # Draw bounding boxes, labels, and confidence
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = f"{classes[class_ids[i]]}: {int(confidences[i] * 100)}%"
            color = (0, 255, 0)  # Green for bounding boxes
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Display the frame in Streamlit
        stframe.image(frame, channels="BGR", use_column_width=True)

        # Update the vehicle count under the video feed (only update value)
        vehicle_count_placeholder.write(f"Vehicle Count: {vehicle_count}")

        # Send HTTP request to ESP32 to control traffic light based on vehicle count
        if vehicle_count > 10:  # Example threshold to turn on traffic light for road 1
            requests.get(f"{ESP32_URL}?road=1")
        elif vehicle_count <= 10:  # Else, turn on traffic light for road 2
            requests.get(f"{ESP32_URL}?road=2")

        # Add a small delay to avoid high CPU usage
        time.sleep(0.1)

    cap.release()

# Webcam Stream
webcam_button = st.button("Start Webcam")

if webcam_button:
    stframe = st.empty()  # Create a placeholder for the webcam stream
    vehicle_count_placeholder = st.empty()  # Create a placeholder for the vehicle count
    video_streaming = True
    cap = cv2.VideoCapture(0)  # Use the webcam
    
    frame_counter = 0  # Frame counter to skip every 5th frame

    while video_streaming:
        ret, frame = cap.read()
        if not ret:
            break

        frame_counter += 1
        if frame_counter % frame_skip != 0:
            continue  # Skip every 5th frame

        # Reduce resolution of the frame (resize to 640x480 or lower if needed)
        frame = cv2.resize(frame, (640, 480))

        # Resize to 416x416 for YOLO inference to speed up processing
        height, width, channels = frame.shape
        resized_frame = cv2.resize(frame, (416, 416))

        # Preprocess the frame for YOLO
        blob = cv2.dnn.blobFromImage(resized_frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
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
        vehicle_count = count_vehicles([boxes[i] for i in indexes.flatten()], [class_ids[i] for i in indexes.flatten()])

        # Draw bounding boxes, labels, and confidence
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = f"{classes[class_ids[i]]}: {int(confidences[i] * 100)}%"
            color = (0, 255, 0)  # Green for bounding boxes
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Display the frame in Streamlit
        stframe.image(frame, channels="BGR", use_column_width=True)

        # Update the vehicle count under the video feed (only update value)
        vehicle_count_placeholder.write(f"Vehicle Count: {vehicle_count}")

        # Send HTTP request to

