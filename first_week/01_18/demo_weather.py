# demo_weather.py
import os
import requests
from datetime import datetime, timedelta

SERVICE_KEY = os.environ["KMA_SERVICE_KEY"]

def _safe_base_time():
    """
    기상청 초단기예보는 정시 기준.
    현재 시각 기준으로 가장 가까운 과거 정시 사용
    """
    now = datetime.now() - timedelta(minutes=40)
    return now.strftime("%H") + "00"

def get_weather(nx=60, ny=127):
    base_date = datetime.now().strftime("%Y%m%d")
    base_time = _safe_base_time()

    url = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"
    params = {
        "serviceKey": SERVICE_KEY,
        "pageNo": 1,
        "numOfRows": 100,
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": nx,
        "ny": ny,
    }

    try:
        res = requests.get(url, params=params, timeout=5)
        res.raise_for_status()
        data = res.json()

        items = data["response"]["body"]["items"]["item"]
        weather = {}

        for it in items:
            if it["category"] in ("T1H", "REH", "SKY"):
                weather[it["category"]] = it["fcstValue"]

        return weather

    except Exception as e:
        print("[WARN] Weather API failed, using fallback context")
        return {}  # ← 데모용 fallback


def weather_to_visual_context(weather: dict) -> str:
    temp = int(weather.get("T1H", 20))
    humidity = int(weather.get("REH", 50))
    sky = weather.get("SKY", "1")

    context = []

    if temp >= 28:
        context.append("warm air, vibrant diffusion")
    elif temp <= 5:
        context.append("cold, crisp atmosphere")

    if humidity >= 70:
        context.append("heavy moisture, dense texture")
    else:
        context.append("dry, light particles")

    if sky == "1":
        context.append("clear, bright light")
    elif sky == "4":
        context.append("dark, muted tones")

    return ", ".join(context) if context else "neutral atmospheric context"


if __name__ == "__main__":
    print(get_weather())
    print(weather_to_visual_context(get_weather()))