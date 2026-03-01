import requests
from config.settings import OPENWEATHER_API_KEY, OPENWEATHER_BASE_URL


def get_weather(city: str) -> str:

    try:
        url = OPENWEATHER_BASE_URL

        params = {
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }

        response = requests.get(url, params=params, timeout=10)

        data = response.json()

        if response.status_code != 200:
            return f"Weather data unavailable for {city}."

        # Extract required fields safely
        city_name = data.get("name", city)
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        condition = data["weather"][0]["description"]

        # Return clean formatted string (VERY IMPORTANT)
        return (
            f"City: {city_name}\n"
            f"Temperature: {temp}°C\n"
            f"Feels Like: {feels_like}°C\n"
            f"Condition: {condition}\n"
            f"Humidity: {humidity}%"
        )

    except Exception as e:
        return f"Error fetching weather data: {str(e)}"