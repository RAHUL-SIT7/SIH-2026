import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "kisan_raksha.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_name TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            crop_type TEXT NOT NULL,
            disease TEXT NOT NULL,
            confidence REAL NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def insert_report(farmer_name, latitude, longitude, crop_type, disease, confidence):
    conn = get_connection()
    cur = conn.execute(
        """
        INSERT INTO reports (farmer_name, latitude, longitude, crop_type, disease, confidence, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (farmer_name, latitude, longitude, crop_type, disease, confidence, datetime.utcnow().isoformat()),
    )
    conn.commit()
    report_id = cur.lastrowid
    conn.close()
    return report_id


def get_all_reports():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM reports ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_recent_reports_near(latitude, longitude, radius_km, days):
    """Returns reports within radius_km of the given point in the last `days` days."""
    from datetime import timedelta
    from geo_utils import haversine_km

    conn = get_connection()
    cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
    rows = conn.execute(
        "SELECT * FROM reports WHERE created_at >= ?", (cutoff,)
    ).fetchall()
    conn.close()

    nearby = []
    for r in rows:
        d = haversine_km(latitude, longitude, r["latitude"], r["longitude"])
        if d <= radius_km:
            item = dict(r)
            item["distance_km"] = round(d, 2)
            nearby.append(item)
    return nearby