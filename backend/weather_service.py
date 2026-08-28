"""
Weather service for Kisan Raksha Network.

In production this calls the OpenWeatherMap One Call API using a real
OPENWEATHER_API_KEY (see .env.example). For this offline demo/judging
environment (no internet / no API key configured), it falls back to a
deterministic simulated forecast so the risk engine can still be
demonstrated end-to-end.
"""

import os
import random
import math

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
OPENWEATHER_URL = "https://api.openweathermap.org/data/3.0/onecall"


def get_weather_forecast(latitude: float, longitude: float, days: int = 5):
    if OPENWEATHER_API_KEY:
        try:
            import requests

            resp = requests.get(
                OPENWEATHER_URL,
                params={
                    "lat": latitude,
                    "lon": longitude,
                    "appid": OPENWEATHER_API_KEY,
                    "units": "metric",
                    "exclude": "current,minutely,hourly,alerts",
                },
                timeout=5,
            )
            resp.raise_for_status()
            data = resp.json()
            daily = data["daily"][:days]
            return [
                {
                    "day": i + 1,
                    "temp": d["temp"]["day"],
                    "humidity": d["humidity"],
                    "rainfall_mm": d.get("rain", 0),
                }
                for i, d in enumerate(daily)
            ]
        except Exception:
            pass  # fall through to simulation

    return _simulate_forecast(latitude, longitude, days)


def _simulate_forecast(latitude: float, longitude: float, days: int):
    """Deterministic pseudo-forecast seeded by location so demo results
    are reproducible and explainable, not just random."""
    seed = int(abs(latitude * 1000) + abs(longitude * 1000))
    rng = random.Random(seed)

    forecast = []
    for day in range(1, days + 1):
        base_temp = 24 + 6 * math.sin(seed % 10 + day)
        forecast.append(
            {
                "day": day,
                "temp": round(base_temp + rng.uniform(-2, 2), 1),
                "humidity": round(60 + rng.uniform(0, 35), 1),
                "rainfall_mm": round(max(0, rng.uniform(-5, 20)), 1),
            }
        )
    return forecast
def get_soil_and_solar_data(latitude: float, longitude: float, days: int = 7):
    """
    NASA POWER API (free, no key required) — provides real satellite/reanalysis
    data: soil surface wetness (GWETTOP) and solar radiation (ALLSKY_SFC_SW_DWN).
    Used as an additional, independent signal in the risk engine:
    high soil wetness + low solar radiation (cloudy) = favorable for fungal disease.
    """
    from datetime import datetime, timedelta
    import requests

    end_date = datetime.utcnow() - timedelta(days=2)  # POWER data has ~2 day lag
    start_date = end_date - timedelta(days=days)

    url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "parameters": "GWETTOP,ALLSKY_SFC_SW_DWN",
        "community": "AG",
        "longitude": longitude,
        "latitude": latitude,
        "start": start_date.strftime("%Y%m%d"),
        "end": end_date.strftime("%Y%m%d"),
        "format": "JSON",
    }

    try:
        resp = requests.get(url, params=params, timeout=8)
        resp.raise_for_status()
        data = resp.json()["properties"]["parameter"]

        wetness_values = [v for v in data["GWETTOP"].values() if v not in (-999, None)]
        solar_values = [v for v in data["ALLSKY_SFC_SW_DWN"].values() if v not in (-999, None)]

        avg_wetness = sum(wetness_values) / len(wetness_values) if wetness_values else None
        avg_solar = sum(solar_values) / len(solar_values) if solar_values else None

        return {
            "avg_soil_wetness": round(avg_wetness, 3) if avg_wetness is not None else None,
            "avg_solar_radiation": round(avg_solar, 2) if avg_solar is not None else None,
            "source": "NASA POWER (real)",
        }
    except Exception:
        # Offline/no-internet fallback so the demo still runs end-to-end
        seed = int(abs(latitude * 1000) + abs(longitude * 1000))
        import random
        rng = random.Random(seed + 1)
        return {
            "avg_soil_wetness": round(rng.uniform(0.2, 0.8), 3),
            "avg_solar_radiation": round(rng.uniform(3, 7), 2),
            "source": "simulated (offline fallback)",
        }