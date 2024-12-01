import json

from fastapi import FastAPI
from kafka import KafkaConsumer

from endpoints.read_last_forecasting import router as read_last_forcasting
from endpoints.sensors_relations import router as sensor_relations
from endpoints.update_db import router as update_db

from create_db import init_db
from endpoints.update_db import save_to_db, predict_to_db

app = FastAPI()

# Include routers
app.include_router(read_last_forcasting)
app.include_router(sensor_relations)
app.include_router(update_db)


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    init_db()

    bootstrap_servers = 'localhost:9092'
    topic = 'measurements_topic'

    consumer = KafkaConsumer(topic,
                             bootstrap_servers=bootstrap_servers,
                             group_id='my_consumer_group',
                             auto_offset_reset='earliest',  # Start reading from the beginning if no offset is stored
                             enable_auto_commit=False,  # Disable auto-commit to manually control offsets
                             value_deserializer=lambda x: json.loads(x.decode("utf-8"))
                             )

    try:
        for message in consumer:
            print(f"Received message: {message.value}")
            save_to_db(message.value)
            predict_to_db(message.value)
    except KeyboardInterrupt:
        pass

    print("Starting the application...")


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down the application...")
