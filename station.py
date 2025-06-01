import requests
import json
import time
import random
from datetime import datetime, timedelta

now = datetime.utcnow()
start = datetime(now.year, now.month, now.day) - timedelta(days=1)
start_ms = int(start.timestamp() * 1000)
end_ms = int(now.timestamp() * 1000)

url = "http://geobs.infp.ro:3000/api/ds/query"
headers = {"Content-Type": "application/json"}

radon_stations = ["DLMdd", "LOPRdd", "NEHRdd", "PANCdd", "VRI2Sdd", "PLORSdd", "GZRdd"]
co2_stations = ["EFORco", "BISRCO2", "DLMCO2", "MlrCO2", "LOPrCO2"]

RADON_LIMIT = 500
CO2_LIMIT = 700

results = []

def fetch_media(station, table, column, add_offset=0):
    query = f"SELECT {column}, timp FROM {table} WHERE statie = '{station}' ORDER BY timp DESC LIMIT 1000"
    payload = {
        "queries": [{
            "refId": "A",
            "datasource": {"type": "grafana-postgresql-datasource", "uid": "pE67edJSk"},
            "rawSql": query,
            "format": "table",
            "datasourceId": 10,
            "intervalMs": 300000,
            "maxDataPoints": 400
        }],
        "from": str(start_ms),
        "to": str(end_ms)
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            data = response.json()
            frames = data["results"]["A"]["frames"]
            if not frames or not frames[0]["data"]["values"]:
                return None
            values = frames[0]["data"]["values"][0]
            if not values:
                return None
            adjusted_vals = [v + add_offset for v in values if isinstance(v, (int, float))]
            if not adjusted_vals:
                return None
            return sum(adjusted_vals) / len(adjusted_vals)
    except:
        return None

print("Connecting weather station...")
try:
    requests.get("https://weather.cn.gov/ACP", timeout=2)
except:
    print("⚠️ weather.cn.gov possibly unreachable")

print("\n🔬 Starting Radon processing...")
for station in radon_stations:
    print(f"📡 Fetching data for {station} from date_radon...")
    media = fetch_media(station, "date_radon", "v0")
    if media is not None:
        alert = "red" if media > RADON_LIMIT else "green"
        results.append({
            "county": "Vrancea",
            "label": station,
            "type": "radon",
            "mean": round(media, 2),
            "alert": alert
        })
    time.sleep(5)

print("🎲 Simulating EFORadon...")
random_vals = [random.randint(10, 400) for _ in range(50)]
media_efor = sum(random_vals) / len(random_vals)
alert_efor = "red" if media_efor > RADON_LIMIT else "green"
results.append({
    "county": "Constanța",
    "label": "EFORadon",
    "type": "radon",
    "mean": round(media_efor, 2),
    "alert": alert_efor
})

print("\n🌬️ Starting CO₂ processing...")
for station in co2_stations:
    print(f"📡 Fetching data for {station} from date_co2...")
    offset = 100 if station in ["EFORco", "BISRCO2"] else 0
    if "EFOR" in station:
        county = "Constanța"
    elif "Mlr" in station or "LOPr" in station:
        county = "Prahova"
    elif "DLM" in station:
        county = "Gorj"
    else:
        county = "Vrancea"
    media = fetch_media(station, "date_co2", "v1", add_offset=offset)
    if media is not None:
        alert = "violet" if media > CO2_LIMIT else "green"
        results.append({
            "county": county,
            "label": station,
            "type": "co2",
            "mean": round(media, 2),
            "alert": alert
        })
    time.sleep(5)

print("\n🔮 Simulating ACP values...")
acp_counties = ["Constanța", "Gorj", "Prahova", "Vrancea", "Iași", "Cluj", "Galați", "București"]
for county in acp_counties:
    acp_val = round(random.uniform(0.2, 2.0), 2)
    if acp_val < 0.5:
        level = "green"
    elif acp_val < 1.0:
        level = "yellow"
    elif acp_val < 1.5:
        level = "orange"
    else:
        level = "red"
    results.append({
        "county": county,
        "label": "ACP",
        "type": "acp",
        "mean": acp_val,
        "alert": level
    })

print("\n💾 Saving results to sensors.json...")
with open("/sdcard/Download/sensors.json", "w") as f:
    json.dump(results, f, indent=2)

print("✅ sensors.json actualizat cu succes.")
