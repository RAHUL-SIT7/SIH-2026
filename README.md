# Kisan Raksha Network — SIH26131 Demo

**Problem Statement:** SIH26131 — Early detection and management of crop diseases and pest infestations (Government of Maharashtra)

## What makes this different from Plantix / PlantVillage-style apps

Most existing apps stop at: photo → disease name. This demo shows the
full unique pipeline:

1. **Detect** — leaf photo → disease classification with an explanation
   (what pattern triggered the result), not just a label.
2. **Predict** — a **risk engine** combines a 5-day weather forecast
   (humidity/temp/rainfall favorability) with **community reports** in a
   5km radius over the last 7 days to output a 0–100 outbreak risk score
   *before* symptoms show up on a given farmer's own crop.
3. **Report** — a confirmed detection is submitted to the shared
   network.
4. **Network effect** — that report immediately raises the risk score
   for every other nearby farmer's next `/predict-risk` call, and shows
   up on the live community heatmap. This is the core differentiator —
   demonstrated live by submitting a report and re-running the risk
   prediction (score visibly increases).

## Project structure

```
demo/
├── backend/
│   ├── main.py            # FastAPI app & routes
│   ├── detection.py       # image classification (heuristic stand-in for MobileNetV3/TFLite)
│   ├── risk_engine.py     # core differentiator: weather + community risk scoring
│   ├── weather_service.py # OpenWeatherMap integration w/ offline simulation fallback
│   ├── database.py        # SQLite storage for community reports
│   ├── geo_utils.py       # haversine distance for radius queries
│   ├── models.py          # Pydantic schemas
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    └── index.html         # single-page demo UI (upload, risk check, map)
```

## How to run

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Then open **http://localhost:8000/app** in a browser — this serves the
frontend and talks to the API on the same port.

API docs (auto-generated, useful for judges/demo): **http://localhost:8000/docs**

## Note on the ML model in this demo

`detection.py` uses a lightweight color-pattern heuristic instead of a
trained model, because training a real MobileNetV3 on the PlantVillage
dataset needs GPU + dataset download not available in this sandboxed
environment. The API contract (`/detect` endpoint, request/response
shape) is already set up so you can drop in real TFLite inference later
without changing anything else — see the comment at the top of
`detection.py` and the `ml-training/` folder structure discussed
earlier for where the real training script goes.

## Note on weather data

`weather_service.py` calls the real OpenWeatherMap One Call API if you
set `OPENWEATHER_API_KEY` in a `.env` file (copy `.env.example`). If no
key is set, it automatically falls back to a deterministic simulated
forecast (seeded by location) so the risk engine still works fully
offline for demos/judging.

## Next steps to extend

- Swap `detection.py` internals for real TFLite inference (see earlier plan)
- Move SQLite → PostgreSQL + PostGIS for production-scale radius queries
- Add Firebase Cloud Messaging so risk alerts push automatically instead of on-demand
- Add regional-language voice interface (STT/TTS)
# SIH-2026
