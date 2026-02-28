import requests
import pandas as pd
import logging
from datetime import datetime
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_api_key():
    """Retrieves API key from environment variables."""
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        logger.error("OPENWEATHER_API_KEY not found in .env file")
    return api_key

def fetch_weather(city, api_key, units='metric'):
    """Fetches weather data for a single city from OpenWeatherMap API."""
    url = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        'q': city,
        'appid': api_key,
        'units': units  # metric = Celsius, imperial = Fahrenheit
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 404:
            logger.warning(f"City not found: {city}")
            return None
        elif response.status_code == 401:
            logger.error(f"Invalid API key for city: {city}")
            return None
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch {city}: {e}")
        return None

def parse_weather_data(data, units='metric'):
    """Parses API response into a clean dictionary."""
    if not data:
        return None
    
    temp_unit = '°C' if units == 'metric' else '°F'
    speed_unit = 'm/s' if units == 'metric' else 'mph'

    return {
        'City': data['name'],
        'Country': data['sys']['country'],
        'Temperature': f"{data['main']['temp']}{temp_unit}",
        'Feels Like': f"{data['main']['feels_like']}{temp_unit}",
        'Humidity': f"{data['main']['humidity']}%",
        'Weather': data['weather'][0]['description'].title(),
        'Wind Speed': f"{data['wind']['speed']} {speed_unit}",
        'Pressure': f"{data['main']['pressure']} hPa",
        'Sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
        'Sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M'),
        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def save_to_file(df, filename, output_format='excel'):
    """Saves DataFrame to Excel or CSV."""
    try:
        if output_format == 'excel':
            df.to_excel(filename, index=False, sheet_name='Weather Data')
        else:
            df.to_csv(filename, index=False, encoding='utf-8-sig')
        logger.info(f"Successfully saved {len(df)} records to {filename}")
    except Exception as e:
        logger.error(f"Failed to save file: {e}")

def main():
    # Load configuration
    api_key = get_api_key()
    if not api_key:
        return
    
    cities_str = os.getenv('CITIES', 'London,New York,Tokyo')
    cities = [c.strip() for c in cities_str.split(',')]
    output_format = os.getenv('OUTPUT_FORMAT', 'excel')
    units = 'metric'  # Change to 'imperial' for Fahrenheit
    
    logger.info(f"Starting Weather API Exporter for {len(cities)} cities...")
    
    results = []
    
    for i, city in enumerate(cities):
        logger.info(f"[{i+1}/{len(cities)}] Fetching: {city}")
        
        data = fetch_weather(city, api_key, units)
        parsed = parse_weather_data(data, units)
        
        if parsed:
            results.append(parsed)
        
        # Be polite to the API (rate limiting)
        time.sleep(0.5)
    
    if results:
        df = pd.DataFrame(results)
        
        # Display in terminal
        print("\n" + "="*80)
        print(df.to_string(index=False))
        print("="*80 + "\n")
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        ext = 'xlsx' if output_format == 'excel' else 'csv'
        filename = f'weather_data_{timestamp}.{ext}'
        
        save_to_file(df, filename, output_format)
        logger.info("Exporter finished successfully.")
    else:
        logger.error("No valid data to export.")

if __name__ == "__main__":
    main()