import sqlite3
from datetime import datetime

import joblib
import numpy as np
import requests
from fastapi import HTTPException, APIRouter

DATABASE = "../db/forecasting.db"

router = APIRouter()

pipeline = joblib.load('../models/model.pkl')


def get_next_pm10(stamp, pm10s):
    """
    predicts the next 15 minute measurement
    """
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


# @router.get("/forecasting_management/update")
# async def update_db():
#     testing_json = {
#         "pm10": range(1, 49),
#         "stamp": [np.datetime64("2021-01-01T00:00:00") + np.timedelta64(i * 15, "m") for i in range(48)]
#     }
#
#     sensor_id = 'nidzo'
#     pm10 = testing_json["pm10"]
#     stamp = testing_json["stamp"]
#     is_predicted = [False] * len(pm10)
#
#     current = stamp[-1]
#
#     while len(pm10) < 96:
#         stamp.append(stamp[-1] + np.timedelta64(15, 'm'))
#         next_pm10 = get_next_pm10(stamp[-1], pm10[-3:], pipeline)
#         pm10.append(next_pm10[0])
#         is_predicted.append(True)
#
#     # adds the dummy data + the predicted values for up 96 in the db
#     for pm10_value, timestamp, predicted in zip(pm10, stamp, is_predicted):
#         requests.post(
#             f"http://localhost:8000/forecasting_management/add_data/{sensor_id}/{timestamp}/{pm10_value}/{predicted}"
#         )
#
#     # ADDS THE LAST REAL VALUE
#     requests.post(
#         f"http://localhost:8000/forecasting_management/add_current/{sensor_id}/{current}"
#     )


# @router.post("/forecasting_management/add_current/{sensor}/{timestamp}")
# def add_current(sensor: str, timestamp: datetime):
#     try:
#         with sqlite3.connect(DATABASE) as conn:
#             cursor = conn.cursor()
#             cursor.execute(
#                 "INSERT OR REPLACE INTO Current (sensor, timestamp) VALUES (?, ?)",
#                 (sensor, timestamp)
#             )
#             conn.commit()
#         return {"message": "Record added to Current table."}
#     except sqlite3.IntegrityError:
#         raise HTTPException(status_code=400, detail="Record already exists.")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#

# @router.post("/forecasting_management/add_data/{sensor}/{timestamp}/{pm10}/{is_predicted}")
# def add_data(sensor: str, timestamp: datetime, pm10: float, is_predicted: bool):
#     try:
#         with sqlite3.connect(DATABASE) as conn:
#             cursor = conn.cursor()
#             cursor.execute(
#                 """
#                 INSERT INTO Data (sensorId, timestamp, pm10, is_predicted)
#                 VALUES (?, ?, ?, ?)
#                 """,
#                 (sensor, timestamp, pm10, is_predicted)
#             )
#             conn.commit()
#
#         return {"message": "Record added to Data table."}
#
#     except sqlite3.IntegrityError:
#         raise HTTPException(status_code=400, detail="Record already exists.")
#
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


def save_to_db(measurement):
    """Save a measurement object to SQLite."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO Data (measurementId, sensorId, timestamp, pm10, is_predicted)
    VALUES (?, ?, ?, ?, ?)
    """, (
        measurement["id"],
        measurement["sensorId"],
        measurement["stamp"],
        measurement["value"],
        False
    ))

    conn.commit()
    conn.close()


def get_last_three_pm10(sensor_id):
    """Retrieve the last three pm10 measurements for a sensor."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT measurementId, sensorId, timestamp, pm10
        FROM Data
        WHERE sensorId = ?
        ORDER BY timestamp DESC
        LIMIT 3
    """, (sensor_id,))

    rows = cursor.fetchall()
    conn.close()

    if len(rows) < 3:
        return None  # Not enough data

    # Ensure the rows are ordered by timestamp ascending
    return sorted(rows, key=lambda row: row[1])


def save_predicted_pm10(measurement_id, sensor_id, timestamp, pm10):
    """Save the predicted pm10 value to the Predicted_Data table."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Predicted_Data (measurementId, sensorId, timestamp, pm10)
        VALUES (?, ?, ?, ?)
    """, (measurement_id, sensor_id, timestamp, pm10))

    conn.commit()
    conn.close()


def predict_to_db(measurement):
    """Predict the next pm10 value and save it to the database."""
    last_measurements = get_last_three_pm10(measurement["sensorId"])

    if not last_measurements:
        print(f"Not enough data to predict for sensor {measurement['sensorId']}.")
        return

    # Extract data for prediction
    pm10s = [row[3] for row in last_measurements]
    last_timestamp = np.datetime64(last_measurements[-1][2])  # Timestamp of the most recent measurement

    # Call the prediction function
    predicted_pm10 = get_next_pm10(last_timestamp, pm10s)[0]  # Assume pipeline.predict returns an array-like result

    # Save the predicted value
    save_predicted_pm10(
        measurement_id=last_measurements[-1][0],
        sensor_id=measurement["sensorId"],
        timestamp=str(last_timestamp + np.timedelta64(15, "m")),
        pm10=predicted_pm10
    )
