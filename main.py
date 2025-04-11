import requests
from datetime import datetime

# Configuration - Replace with your details
LOCATION = "New York"  # Example: "London" or "Chicago"


def get_weather_forecast():
    # Fetch weather data from wttr.in
    url = f"https://wttr.in/{LOCATION}?format=%C+%t+%w"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.text.strip()
        return f"Weather for {LOCATION}:\n{data}"
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {str(e)}"


def display_forecast(forecast):
    # Display the weather forecast on the screen
    print(f"Weather Forecast for {LOCATION} - {datetime.now().strftime('%Y-%m-%d')}")
    print(forecast)


if __name__ == "__main__":
    print("Fetching weather forecast...")
    forecast = get_weather_forecast()
    
    if not forecast.startswith("Error"):
        display_forecast(forecast)
    else:
        print(forecast)
