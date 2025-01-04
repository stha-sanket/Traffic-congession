import os
import cv2
import numpy as np
from flask import Flask, render_template, Response, request, jsonify
import threading

# Initialize Flask app
app = Flask(__name__)

# Configuration for video upload
UPLOAD_FOLDER = 'uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Max file size of 100MB

# Load YOLO model
net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Load class names
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Global flags and variables
video_streaming = False
frame_rate = 2  # Process every 2nd frame
frame_count = 0
current_frame = None
frame_lock = threading.Lock()

# Function to count vehicles
def count_vehicles(detections, class_ids):
    vehicle_classes = ["car", "motorbike", "bus", "truck"]
    vehicle_count = 0
    for class_id in class_ids:
        if classes[class_id] in vehicle_classes:
            vehicle_count += 1
    return vehicle_count

# Video capture thread
def capture_frames():
    global current_frame
    cap = cv2.VideoCapture(0)  # Using webcam
    while video_streaming:
        ret, frame = cap.read()
        if not ret:
            break
        with frame_lock:
            current_frame = frame
    cap.release()

# Video processing function for generating frames
def generate_frames():
    global frame_count, current_frame
    while video_streaming:
        with frame_lock:
            if current_frame is None:
                continue  # Skip if no frame is available
            frame = current_frame

        if frame_count % frame_rate == 0:
            # Preprocess the frame for YOLO
            height, width, channels = frame.shape
            blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
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

            # Draw bounding boxes and labels
            for i in indexes.flatten():
                x, y, w, h = boxes[i]
                label = f"{classes[class_ids[i]]}: {int(confidences[i] * 100)}%"
                color = (0, 255, 0)  # Green for bounding boxes
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # Display vehicle count on the frame
            cv2.putText(frame, f"Vehicle Count: {vehicle_count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        frame_count += 1
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            break
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# Check if file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to upload a video
@app.route('/upload_video', methods=['POST'])
def upload_video():
    try:
        if 'file' not in request.files:
            return jsonify(success=False, message="No file part"), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify(success=False, message="No selected file"), 400

        if file and allowed_file(file.filename):
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(video_path)
            print(f"File saved to {video_path}")

            # Here you can process the uploaded video file (e.g., with OpenCV or your existing code)
            # For simplicity, we're skipping that step, but you can process the video as needed.

            return jsonify(success=True)

        return jsonify(success=False, message="Invalid file type"), 400

    except Exception as e:
        print(f"Error uploading file: {e}")
        return jsonify(success=False, message="An error occurred during the upload."), 500

# Route to display the homepage
@app.route('/')
def index():
    global video_streaming
    video_streaming = False  # Stop the video when the page is loaded
    return render_template('index.html')

# Route to start the video stream
@app.route('/start_video', methods=['POST'])
def start_video():
    global video_streaming
    video_streaming = True  # Start streaming

    # Start the capture thread for video feed
    capture_thread = threading.Thread(target=capture_frames)
    capture_thread.start()

    return jsonify(success=True)

# Route to stop the video stream
@app.route('/stop_video', methods=['POST'])
def stop_video():
    global video_streaming
    video_streaming = False  # Stop streaming
    return jsonify(success=True)

# Route to stream the video feed
@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
