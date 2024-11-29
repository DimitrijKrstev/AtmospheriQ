import sqlite3
from fastapi import FastAPI, HTTPException
from datetime import datetime

app = FastAPI()

# Database file
DATABASE = "../db/forecasting.db"


@app.get("/get_measurements/{sensor}")
def get_measurements(sensor: str):
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()

            # Get the last current timestamp for the sensor
            cursor.execute(
                """
                SELECT timestamp FROM Current
                WHERE sensor = ?
                ORDER BY timestamp DESC
                LIMIT 1
                """,
                (sensor,),
            )
            current_row = cursor.fetchone()

            if not current_row:
                raise HTTPException(status_code=404, detail="No current data found for the sensor.")

            current_timestamp = current_row[0]

            # Query for measurements
            # 47 before current timestamp
            cursor.execute(
                """
                SELECT * FROM Data
                WHERE sensor = ? AND timestamp < ?
                ORDER BY timestamp DESC
                LIMIT 47
                """,
                (sensor, current_timestamp),
            )
            measurements_before = cursor.fetchall()

            # Record at the current timestamp
            cursor.execute(
                """
                SELECT * FROM Data
                WHERE sensor = ? AND timestamp = ?
                """,
                (sensor, current_timestamp),
            )
            current_measurement = cursor.fetchone()

            # 48 after current timestamp
            cursor.execute(
                """
                SELECT * FROM Data
                WHERE sensor = ? AND timestamp > ?
                ORDER BY timestamp ASC
                LIMIT 48
                """,
                (sensor, current_timestamp),
            )
            measurements_after = cursor.fetchall()

        # Combine the results
        all_measurements = (
            measurements_before[::-1]  # Reverse the "before" list to chronological order
            + ([current_measurement] if current_measurement else [])
            + measurements_after
        )

        return {
            "sensor": sensor,
            "current_timestamp": current_timestamp,
            "measurements": [
                {"sensor": row[0], "timestamp": row[1], "pm10": row[2], "is_predicted": row[3]}
                for row in all_measurements
            ],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
