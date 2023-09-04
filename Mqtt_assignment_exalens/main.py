from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
import json
import redis
app = FastAPI()
import ast
import datetime

# MongoDB connection settings
mongo_uri = "mongodb://localhost:27017/"  # Change this if your MongoDB is on a different host
mongo_client = MongoClient(mongo_uri)
db = mongo_client["sensor_data"]
collection = db["sensor_readings"]

#Redis connection settings
redis_host = "localhost"  # Change this if your Redis is on a different host
redis_port = 6379

# Connect to Redis
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

@app.get("/fetch_readings")
async def fetch_readings(start: str = Query(...), end: str = Query(...)):
    try:
        start_date = datetime.date.fromisoformat(start)
        end_date = datetime.date.fromisoformat(end)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    readings = collection.find({
        "timestamp": {
            "$gte": start_date,
            "$lte": end_date
        }
    })
    return json.loads(json.dumps(list(readings)))

@app.get("/latest_readings/{sensor_id}")
async def fetch_latest_readings(sensor_id: str):
    redis_key = f"latest_readings:{sensor_id}"
    latest_readings = redis_client.lrange(redis_key, 0, -1)
    print("latest_readings---------,,,,,<<<<< ", latest_readings)
    # return ast.literal_eval(json.dumps([json.loads(reading) for reading in latest_readings]))
    return latest_readings
