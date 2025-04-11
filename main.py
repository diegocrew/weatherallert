import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Configuration - Replace with your details
LOCATION = "New York"  # Example: "London" or "Chicago"
EMAIL_FROM = "your_email@gmail.com"
EMAIL_TO = "recipient_email@example.com"
EMAIL_PASSWORD = "your_email_password"  # Use app-specific password if using Gmail
SMTP_SERVER = "smtp.gmail.com"  # Change if not using Gmail
SMTP_PORT = 587


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


def send_email(forecast):
    # Create email message
    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg["Subject"] = f"Weather Forecast for {LOCATION} - {datetime.now().strftime('%Y-%m-%d')}"
    
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
