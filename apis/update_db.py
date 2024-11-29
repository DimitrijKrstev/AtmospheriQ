import os
import json
import requests

import numpy as np
import pandas as pd
import joblib

from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder

def get_next_pm10(stamp, pm10s, pipeline):
    pm10_1 = pm10s[0]
    pm10_2 = pm10s[1]
    pm10_3 = pm10s[2]
    
    hour = int(str(stamp).split('T')[1].split(':')[0])
    minute = int(str(stamp).split('T')[1].split(':')[1])
    second = int(str(stamp).split('T')[1].split(':')[2].split('.')[0])
    
    hour_feature = hour + minute / 60 + second / 3600
    
    month = int(str(stamp).split('T')[0].split('-')[1])
    day = int(str(stamp).split('T')[0].split('-')[2])

    start_of_month = stamp.astype('datetime64[M]')
    start_of_next_month = start_of_month + np.timedelta64(1, 'M')

    days_in_month = (start_of_next_month - start_of_month).astype('timedelta64[D]').astype(int)

    
    month_feature = month + day / days_in_month
    
    return pipeline.predict(np.array([hour_feature, month_feature, pm10_1, pm10_2, pm10_3]).reshape(1, -1))

@app.get("/forecasting_management/update")
async def update_db():
    testing_json = {
        "pm10": range(1, 49),
        "stamp": [np.datetime64("2021-01-01T00:00:00") + np.timedelta64(i * 15, "min") for i in range(48)]
    }
    
    sensor_id = 'nidzo'
    pm10 = testing_json["pm10"]
    stamp = testing_json["stamp"]
    is_predicted = [False] * len(pm10)
    
    current = stamp[-1]
    
    pipeline = joblib.load('../models/model.pkl')
    

    while len(pm10) < 96:
        stamp.append(stamp[-1] + np.timedelta64(15, 'm'))
        next_pm10 = get_next_pm10(stamp[-1], pm10[-3:])
        pm10.append(next_pm10[0])
        is_predicted.append(True)
    
    
    for pm10_value, timestamp, predicted in zip(pm10, stamp, is_predicted):
        requests.post(
            f"http://localhost:8000/forecasting_management/add_data/{sensor_id}/{timestamp}/{pm10_value}/{predicted}"
        )
    
    requests.post(
        f"http://localhost:8000/forecasting_management/add_current/{sensor_id}/{current}"
    )