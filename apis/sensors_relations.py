import os
import json
import requests

import numpy as np
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder

load_dotenv()
app = FastAPI()

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a)) 
    km = 6367 * c
    return km


class Sensor:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id

        sensors_closest = []

    def get_distance(self, other_sensor):
        
        return haversine(self.x, self.y, other_sensor.x, other_sensor.y)
    
    def generate_closest(self, sensors, limit=5):
        assert limit > 0, "Limit must be greater than 0"
        
        self.sensors_closest = sorted(sensors, key=lambda x: self.get_distance(x))[:limit]
        
    def to_json(self):
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "sensors_closest": [
                {
                    "id": sensor.id, 
                    "distance": self.get_distance(sensor)
                }
                
                for sensor in self.sensors_closest
            ]
        }
        
    

@app.get("/sensor_relations/{num_relations}")
async def say_hello(num_relations: int):
    pulse_username = os.getenv("PULSE_USERNAME")
    pulse_password = os.getenv("PULSE_PASSWORD")
    city_name = os.getenv("CITY_NAME")
    
    response = requests.get(f"https://{city_name}.pulse.eco/rest/sensor", auth=(pulse_username, pulse_password))
    response = response.json()
    
    # Load the data into a pandas dataframe
    sensors_df = pd.DataFrame(response)
    sensors_df = sensors_df[['sensorId', 'position']]
    
    # Extract the x and y coordinates
    sensors_df['x'] = sensors_df['position'].apply(lambda x: float(x.split(',')[0]))
    sensors_df['y'] = sensors_df['position'].apply(lambda x: float(x.split(',')[1]))
    
    # Generate the list of sensors
    sensors_list = []
    
    for row in sensors_df.itertuples():
        id = row.sensorId
        x = row.x
        y = row.y

        sensor = Sensor(x, y, id)
        sensors_list.append(sensor)

    # Generate the closest sensors
    for idx, sensor in enumerate(sensors_list):
        sensor.generate_closest(sensors_list[:idx] + sensors_list[idx+1:], limit=num_relations)
    
    
    return jsonable_encoder([sensor.to_json() for sensor in sensors_list])
