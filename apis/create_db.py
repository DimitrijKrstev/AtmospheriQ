import os
import sqlite3

DATABASE = "../db/forecasting.db"


def init_db():
    # Ensure the directory exists
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Current (
                sensor TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                PRIMARY KEY (sensor, timestamp)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Data (
                measurementId NUMBER NOT NULL,
                sensorId TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                pm10 REAL NOT NULL,
                is_predicted BOOLEAN NOT NULL,
                PRIMARY KEY (measurementId, sensorId, timestamp)
            )
        """)
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Predicted_Data (
                        measurementId NUMBER NOT NULL,
                        sensorId TEXT NOT NULL,
                        timestamp DATETIME NOT NULL,
                        pm10 REAL NOT NULL,
                        PRIMARY KEY (measurementId, sensorId, timestamp)
                    )
                """)
        conn.commit()
