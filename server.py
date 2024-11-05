from flask import Flask, jsonify, render_template
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)
BROKER = 'localhost'
PORT = 1884
TOPIC = 'traffic/data'
traffic_data = {}

# MQTT Callback Functions
def on_connect(client, userdata, flags, rc):
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    global traffic_data
    data = json.loads(msg.payload.decode())
    sensor_id = data['sensor_id']
    traffic_data[sensor_id] = {
        "vehicle_count": data['vehicle_count'],
        "avg_speed": data['avg_speed'],
        "timestamp": data['timestamp'],
        "signal": adjust_traffic_signal(data['vehicle_count'], data['avg_speed'])
    }

# Adjust signal based on traffic data
def adjust_traffic_signal(vehicle_count, avg_speed):
    if vehicle_count > 10 or avg_speed < 30:
        return "RED"  # High traffic, stop signal
    elif vehicle_count < 5 and avg_speed > 50:
        return "GREEN"  # Low traffic, clear signal
    else:
        return "YELLOW"  # Moderate traffic

# MQTT Client Configuration
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)
client.loop_start()

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/traffic_data')
def get_traffic_data():
    return jsonify(traffic_data)

if __name__ == '__main__':
    app.run(debug=True)
