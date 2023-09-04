import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

# MQTT broker settings
broker_address = "localhost"  # Change this if your broker is on a different host
broker_port = 1883

# Topics to publish to
temperature_topic = "sensors/temperature"
humidity_topic = "sensors/humidity"

# List of unique sensor IDs
sensor_ids = ["sensor1", "sensor2", "sensor3"]

# Connect to the MQTT broker
client = mqtt.Client()
client.connect(broker_address, broker_port)
print("Publisher , Publisher, Publisher ------>")

while True:
    for sensor_id in sensor_ids:
        # Simulate random sensor readings
        temperature = round(random.uniform(20, 30), 2)
        humidity = round(random.uniform(40, 60), 2)

        # Create JSON payload
        payload = {
            "sensor_id": sensor_id,
            "value": temperature,
            "timestamp": datetime.now().isoformat()
        }
        payload_json = json.dumps(payload)
        print("Publisher2 , Publisher3, Publisher4 ------>")

        # Publish temperature reading
        client.publish(temperature_topic, payload_json)

        # Create JSON payload for humidity
        payload["value"] = humidity
        payload_json = json.dumps(payload)
        print("current payload_jason", payload_json)
        # Publish humidity reading
        client.publish(humidity_topic, payload_json)

    time.sleep(5)  # Wait for 5 seconds before publishing again
