"""
Risk Engine — the core differentiator of Kisan Raksha Network.

Combines THREE independent signal sources:
  1. Short-term weather forecast (OpenWeatherMap) — temp/humidity/rainfall
     favorability for the next 5 days.
  2. NASA POWER satellite/reanalysis data — recent soil wetness and solar
     radiation, an independent real-data confirmation of disease-favorable
     conditions (cloudy + wet soil supports fungal growth).
  3. Community signal — how many nearby farmers reported the same/related
     disease in the last N days -> early warning BEFORE symptoms appear
     on a given farmer's own crop.

Output is a 0-100 risk score with human-readable, source-attributed
reasons, so it stays explainable rather than being a black box.
"""

from weather_service import get_weather_forecast, get_soil_and_solar_data
from database import get_recent_reports_near

# Conditions known to favor common fungal/bacterial crop diseases
FAVORABLE_HUMIDITY_MIN = 75
FAVORABLE_TEMP_RANGE = (20, 30)
RAINFALL_TRIGGER_MM = 10

HIGH_SOIL_WETNESS = 0.55   # GWETTOP scale 0-1
LOW_SOLAR_RADIATION = 4.5  # kWh/m^2/day — low = cloudy

COMMUNITY_RADIUS_KM = 5
COMMUNITY_WINDOW_DAYS = 7


def calculate_outbreak_risk(latitude: float, longitude: float, crop_type: str):
    forecast = get_weather_forecast(latitude, longitude, days=5)
    nasa_data = get_soil_and_solar_data(latitude, longitude, days=7)
    nearby_reports = get_recent_reports_near(
        latitude, longitude, radius_km=COMMUNITY_RADIUS_KM, days=COMMUNITY_WINDOW_DAYS
    )

    score = 0
    reasons = []

    # --- Weather signal (max 35 points) ---
    humid_days = [d for d in forecast if d["humidity"] >= FAVORABLE_HUMIDITY_MIN]
    if humid_days:
        score += 15
        reasons.append(
            f"High humidity (>={FAVORABLE_HUMIDITY_MIN}%) expected on {len(humid_days)} of next 5 days — favorable for fungal spread. [Source: OpenWeatherMap]"
        )

    temp_days = [
        d for d in forecast
        if FAVORABLE_TEMP_RANGE[0] <= d["temp"] <= FAVORABLE_TEMP_RANGE[1]
    ]
    if temp_days:
        score += 10
        reasons.append(
            f"Temperature staying in the {FAVORABLE_TEMP_RANGE[0]}-{FAVORABLE_TEMP_RANGE[1]}°C disease-favorable range for {len(temp_days)} days. [Source: OpenWeatherMap]"
        )

    rain_days = [d for d in forecast if d["rainfall_mm"] >= RAINFALL_TRIGGER_MM]
    if rain_days:
        score += 10
        reasons.append(
            f"Significant rainfall forecast on {len(rain_days)} day(s) — raises leaf-wetness duration. [Source: OpenWeatherMap]"
        )

    # --- NASA POWER signal (max 20 points) — independent real-data confirmation ---
    wetness = nasa_data.get("avg_soil_wetness")
    solar = nasa_data.get("avg_solar_radiation")

    if wetness is not None and wetness >= HIGH_SOIL_WETNESS:
        score += 10
        reasons.append(
            f"Recent soil surface wetness averaging {wetness} (satellite-observed) is high — sustained moisture supports pathogen survival. [Source: {nasa_data['source']}]"
        )

    if solar is not None and solar <= LOW_SOLAR_RADIATION:
        score += 10
        reasons.append(
            f"Low solar radiation averaging {solar} kWh/m²/day (cloudy conditions) — reduces UV-based natural pathogen suppression. [Source: {nasa_data['source']}]"
        )

    # --- Community signal (max 45 points) ---
    same_crop_reports = [r for r in nearby_reports if r["crop_type"].lower() == crop_type.lower()]
    if len(same_crop_reports) >= 5:
        score += 45
        reasons.append(
            f"{len(same_crop_reports)} nearby farmers ({COMMUNITY_RADIUS_KM}km radius) reported disease on {crop_type} in the last {COMMUNITY_WINDOW_DAYS} days — active outbreak cluster."
        )
    elif len(same_crop_reports) >= 2:
        score += 25
        reasons.append(
            f"{len(same_crop_reports)} nearby farmers reported disease on {crop_type} recently — early cluster forming."
        )
    elif len(same_crop_reports) == 1:
        score += 10
        reasons.append("1 nearby report on the same crop — monitor closely.")

    if len(nearby_reports) >= 8:
        score = min(score + 5, 100)
        reasons.append(f"High overall disease-report activity in your area ({len(nearby_reports)} reports).")

    score = min(score, 100)

    if score >= 70:
        level = "HIGH"
        recommendation = "Act now: apply preventive spray/treatment today, do not wait for visible symptoms."
    elif score >= 40:
        level = "MODERATE"
        recommendation = "Increase field monitoring frequency to daily; keep treatment ready."
    else:
        level = "LOW"
        recommendation = "Continue routine monitoring, no immediate action needed."

    if not reasons:
        reasons.append("No significant weather, satellite, or community risk signals detected.")

    return {
        "risk_score": score,
        "risk_level": level,
        "reasons": reasons,
        "recommendation": recommendation,
        "forecast_days": len(forecast),
    }