"""SQLite database operations for sensor data."""
import sqlite3
import os
from datetime import datetime, timedelta
from typing import List, Tuple, Optional


class SensorDatabase:
    """Manages sensor data storage and retrieval."""

    def __init__(self, db_path: str = "sensor_data.db"):
        """Initialize database connection and create tables if needed."""
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Create tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                temperature REAL,
                humidity REAL,
                pressure REAL,
                gas_resistance REAL,
                pm1 REAL,
                pm25 REAL,
                pm10 REAL
            )
        ''')

        conn.commit()
        conn.close()

    def log_reading(self, temperature: float, humidity: float, pressure: float,
                   gas_resistance: float, pm1: float, pm25: float, pm10: float):
        """Insert a sensor reading into the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO sensor_readings
            (temperature, humidity, pressure, gas_resistance, pm1, pm25, pm10)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (temperature, humidity, pressure, gas_resistance, pm1, pm25, pm10))

        conn.commit()
        conn.close()

    def get_readings(self, hours: int = 24) -> List[Tuple]:
        """
        Retrieve sensor readings from the last N hours.
        Returns list of tuples: (timestamp, temp, humidity, pressure, gas, pm1, pm25, pm10)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cutoff_time = datetime.now() - timedelta(hours=hours)

        cursor.execute('''
            SELECT timestamp, temperature, humidity, pressure,
                   gas_resistance, pm1, pm25, pm10
            FROM sensor_readings
            WHERE timestamp >= ?
            ORDER BY timestamp ASC
        ''', (cutoff_time,))

        results = cursor.fetchall()
        conn.close()

        return results

    def get_latest_reading(self) -> Optional[Tuple]:
        """Get the most recent sensor reading."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT timestamp, temperature, humidity, pressure,
                   gas_resistance, pm1, pm25, pm10
            FROM sensor_readings
            ORDER BY timestamp DESC
            LIMIT 1
        ''')

        result = cursor.fetchone()
        conn.close()

        return result
