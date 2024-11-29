import sqlite3
from fastapi import FastAPI, HTTPException
from datetime import datetime

app = FastAPI()

# Database file
DATABASE = "../db/forecasting.db"

# Function to initialize the database and create tables
def init_db():
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
                sensor TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                pm10 REAL NOT NULL,
                is_predicted BOOLEAN NOT NULL,
                PRIMARY KEY (sensor, timestamp)
            )
        """)
        conn.commit()

# Initialize the database on startup
@app.on_event("startup")
def startup_event():
    init_db()

@app.post("forecasting_management/add_current/{sensor}/{timestamp}")
def add_current(sensor: str, timestamp: datetime):
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO Current (sensor, timestamp) VALUES (?, ?)",
                (sensor, timestamp)
            )
            conn.commit()
        return {"message": "Record added to Current table."}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Record already exists.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("forecasting_management/add_data/{sensor}/{timestamp}/{pm10}/{is_predicted}")
def add_data(sensor: str, timestamp: datetime, pm10: float, is_predicted: bool):
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO Data (sensor, timestamp, pm10, is_predicted)
                VALUES (?, ?, ?, ?)
                """,
                (sensor, timestamp, pm10, is_predicted)
            )
            conn.commit()
            
        return {"message": "Record added to Data table."}
    
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Record already exists.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
