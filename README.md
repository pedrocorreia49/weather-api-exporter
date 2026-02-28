# 🌤️ Weather API Data Exporter

A robust Python script that fetches live weather data from OpenWeatherMap API and exports it to Excel/CSV.

🚀 Features
• Multi-City Monitoring: Fetches data for multiple cities in one run
• Secure Configuration: API keys managed via .env file
• Data Export: Saves clean data to Excel or CSV using Pandas
• Error Handling: Gracefully handles API errors and invalid cities
• Logging: Detailed console logs for monitoring

🛠 Tech Stack
• Python 3.9+
• Requests
• Pandas
• python-dotenv
• OpenPyXL

📖 Usage
# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
OPENWEATHER_API_KEY=your_key_here

# Run exporter
python weather_exporter.py