import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

# Configuration - Replace with your details
LOCATION = "New York,US"  # Example: "London,UK" or "Chicago,US"
OPENWEATHER_API_KEY = (
    "your_openweather_api_key"  # Get from https://openweathermap.org/api
)
EMAIL_FROM = "your_email@gmail.com"
EMAIL_TO = "recipient_email@example.com"
EMAIL_PASSWORD = "your_email_password"  # Use app-specific password if using Gmail
SMTP_SERVER = "smtp.gmail.com"  # Change if not using Gmail
SMTP_PORT = 587


def get_weather_forecast():
    # Get hourly forecast for the next 48 hours (API returns 48 hours by default)
    from urllib.parse import quote
    encoded_api_key = quote(OPENWEATHER_API_KEY)
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={LOCATION}&appid={encoded_api_key}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Extract hourly temperature data for next 24 hours
        forecasts = []
        now = datetime.now()
        end_time = now + timedelta(hours=24)
        
        for forecast in data["list"]:
            forecast_time = datetime.fromtimestamp(forecast["dt"])
            if forecast_time <= end_time:
                temp = forecast["main"]["temp"]
                time_str = forecast_time.strftime("%Y-%m-%d %H:%M")
                forecasts.append(f"{time_str}: {temp}°C")
        
        return "\n".join(forecasts)
    
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {str(e)}"
    

def send_email(forecast):
    # Create email message
    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg["Subject"] = f"Weather Forecast for {LOCATION} - Next 24 Hours"
    
    body = f"Weather Forecast for {LOCATION}:\n\n{forecast}"
    msg.attach(MIMEText(body, "plain"))
    
    # Send email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {str(e)}")


if __name__ == "__main__":
    print("Fetching weather forecast...")
    forecast = get_weather_forecast()
    
    if not forecast.startswith("Error"):
        print("Sending email...")
        send_email(forecast)
    else:
        print(forecast)
