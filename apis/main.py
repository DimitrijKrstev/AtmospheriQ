from fastapi import FastAPI
from endpoints.read_last_forecasting import router as read_last_forcasting
from endpoints.sensors_relations import router as sensor_relations
from endpoints.update_db import router as update_db

from create_db import init_db

app = FastAPI()

# Include routers
app.include_router(read_last_forcasting)
app.include_router(sensor_relations)
app.include_router(update_db)


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    init_db()
    print("Starting the application...")


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down the application...")
