from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import random
import time

app = Flask(__name__)
socketio = SocketIO(app)

# Simulating hourly traffic data and daily traffic data
hourly_traffic = [random.randint(100, 1000) for _ in range(24)]  # Hourly traffic for a day (24 hours)
daily_traffic = [random.randint(5000, 10000) for _ in range(7)]  # Daily traffic for a week (7 days)

# Simulate estimated peak hour and peak day (random)
estimated_peak_hour = random.randint(0, 23)
estimated_peak_day = random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

@app.route('/')
def index():
    return render_template('index.html', 
                           hourly_traffic=hourly_traffic, 
                           daily_traffic=daily_traffic,
                           estimated_peak_hour=estimated_peak_hour,
                           estimated_peak_day=estimated_peak_day)

@app.route('/get_dynamic_data')
def get_dynamic_data():
    # Randomly simulate peak hour and peak day dynamically
    estimated_peak_hour = random.randint(0, 23)
    estimated_peak_day = random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    
    # Update the hourly and daily traffic
    global hourly_traffic, daily_traffic
    hourly_traffic = [random.randint(100, 1000) for _ in range(24)]
    daily_traffic = [random.randint(5000, 10000) for _ in range(7)]
    
    return jsonify({
        "estimated_peak_hour": estimated_peak_hour,
        "estimated_peak_day": estimated_peak_day,
        "hourly_traffic": hourly_traffic,
        "daily_traffic": daily_traffic
    })

# SocketIO endpoint for real-time data update
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
