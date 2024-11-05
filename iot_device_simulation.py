import paho.mqtt.client as mqtt
import random
import time
import json

# MQTT Configuration
BROKER = 'localhost'  # Use IP if not local
PORT = 1884
TOPIC = 'traffic/data'

client = mqtt.Client()

def connect_mqtt():
    client.connect(BROKER, PORT)
    client.loop_start()

def publish_data():
    while True:
        # Simulate sensor data
        data = {
            "sensor_id": f"sensor_{random.randint(1,5)}",
            "vehicle_count": random.randint(0, 20),
            "avg_speed": random.uniform(20, 60),  # km/h
            "timestamp": time.time()
        }
        # Publish to MQTT broker
        client.publish(TOPIC, json.dumps(data))
        print(f"Published data: {data}")
        time.sleep(5)  # Adjust frequency as needed

if __name__ == "__main__":
    connect_mqtt()
    publish_data()
