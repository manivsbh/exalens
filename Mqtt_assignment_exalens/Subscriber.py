import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient
import redis
from bson import json_util



# MQTT broker settings
broker_address = "localhost"  # Change this if your broker is on a different host
broker_port = 1883

# Redis connection settings
redis_host = "localhost"  # Change this if your Redis is on a different host
redis_port = 6379

# Connect to Redis
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)


# Topics to subscribe to
topics = ["sensors/temperature", "sensors/humidity"]

# MongoDB connection settings
mongo_uri = "mongodb://localhost:27017/"  # Change this if your MongoDB is on a different host
mongo_client = MongoClient(mongo_uri)
db = mongo_client["sensor_data"]
collection = db["sensor_readings"]
print("Sublisher2 , Sublisher3, Sublisher4 ------>")
# Callback when a message is received
def on_message(client, userdata, message):
    payload = json.loads(message.payload.decode())
    collection.insert_one(payload)
    print("Received and stored:", payload)

    # Store latest readings in Redis
    sensor_id = payload["sensor_id"]
    redis_key = f"latest_readings:{sensor_id}"
    redis_key = str(redis_key)
    # redis_data = json.dumps(payload)
    payload = str(payload)
    # redis_data = json.loads(redis_data)
    # print("payload ---------->>>>", str(redis_data))
    print('original payload +++++++++ ', payload)
    print("Sublisher2 , Sublisher3, Sublisher4 ------>")
    print(type(redis_key))
    print(type("readings1"))
    # print(redis_key)
    # redis_client.lpush("readings1", "{'sensor_id': 'sensor001', 'value': 40.33, 'timestamp': '2023-08-22T21:22:25.791719', '_id': ObjectId('64e4d9b9bbb534978b2817a3')}")
    redis_client.lpush(redis_key, payload)
    print("here pushing to redis")
    # while redis_client.scard(redis_key) > 10:
    #     old_messsage = redis_client.spop(redis_key)
    #     print(old_messsage.decode('utf-8'))
    redis_client.ltrim(redis_key, 0, 9)  # Keep only the latest ten readings
    print("trimming down the messages<<<<<")

# Connect to the MQTT broker and set up the message callback
client = mqtt.Client()
client.on_message = on_message
client.connect(broker_address, broker_port)
for topic in topics:
    client.subscribe(topic)

# Start the MQTT loop
client.loop_forever()
