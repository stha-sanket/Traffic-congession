from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
import random
import cv2
import numpy as np

app = Flask(__name__)
socketio = SocketIO(app)

# Simulating traffic data (for demo purposes)
hourly_traffic = [random.randint(100, 1000) for _ in range(24)]
daily_traffic = [random.randint(5000, 10000) for _ in range(7)]
estimated_peak_hour = random.randint(0, 23)
estimated_peak_day = random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

# YOLO model setup
net = cv2.dnn.readNet(r'static\yolo\yolov3.weights', r'static\yolo\yolov3.cfg')
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Load class names
with open("static\yolo\coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

def count_vehicles(detections, class_ids):
    vehicle_classes = ["car", "motorbike", "bus", "truck"]
    vehicle_count = 0
    for class_id in class_ids:
        if classes[class_id] in vehicle_classes:
            vehicle_count += 1
    return vehicle_count

def generate_frames():
    cap = cv2.VideoCapture(0)  # Replace with video file path if needed
    while True:
        success, frame = cap.read()
        if not success:
            break

        height, width, _ = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        detections = net.forward(output_layers)

        class_ids = []
        confidences = []
        boxes = []
        for output in detections:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        vehicle_count = count_vehicles([boxes[i] for i in indexes.flatten()], [class_ids[i] for i in indexes.flatten()])

        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = f"{classes[class_ids[i]]}: {int(confidences[i] * 100)}%"
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.putText(frame, f"Vehicle Count: {vehicle_count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/')
def home():
    return render_template('home.html')  # Home page

@app.route('/analytics')
def analytics():
    return render_template('index.html', 
                           hourly_traffic=hourly_traffic, 
                           daily_traffic=daily_traffic,
                           estimated_peak_hour=estimated_peak_hour,
                           estimated_peak_day=estimated_peak_day)

@app.route('/traffic-system')
def traffic_system():
    return render_template('traffic_system.html')  # Traffic system page

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# SocketIO endpoint for real-time updates
@socketio.on('update_data')
def handle_update():
    new_data = {
        "estimated_peak_hour": random.randint(0, 23),
        "estimated_peak_day": random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]),
        "hourly_traffic": [random.randint(100, 1000) for _ in range(24)],
        "daily_traffic": [random.randint(5000, 10000) for _ in range(7)]
    }
    emit('update_graph', new_data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
