import os
import requests

def get_minutely_forecast(lat, lon, api_key):
    url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {
        "lat": lat,
        "lon": lon,
        "exclude": "current,hourly,daily,alerts",
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "minutely" in data:
            return data["minutely"]
        else:
            print("No minutely data available.")
            return None
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


if __name__ == "__main__":
    # Seoul
    latitude = 37.5665
    longitude = 126.9780
    API_KEY = os.getenv("OWM_API_KEY")

    minutely_data = get_minutely_forecast(latitude, longitude, API_KEY)
    if minutely_data:
        for minute in minutely_data:
            dt = minute["dt"]
            precipitation = minute.get("precipitation", 0)
            print(f"Time: {dt}, Precipitation: {precipitation} mm")