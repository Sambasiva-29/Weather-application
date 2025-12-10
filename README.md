# Weather Data Logger - Flipkart Internship Task

A comprehensive Python application that fetches real-time weather data from the OpenWeatherMap API, stores it in a SQLite database, and provides a user-friendly interface to view historical weather information.

## Features

- Real-time Weather Data: Fetch current weather for any city worldwide.
- Data Persistence: Store weather data in SQLite database with timestamp.
- Search History: View recent searches and city-specific weather history.
- API Status Check: Verify API configuration and connectivity.
- Error Handling: Comprehensive error handling for API failures and network issues.
- Logging: Automatic logging of all weather data fetches.
- Environment Configuration: Secure API key management using .env files.

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/weather-data-logger.git
cd weather-data-logger
```
### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```
### Step 3: Get OpenWeatherMap API Key

1) Go to https://openweathermap.org

2) Sign up for a free account

3) Verify your email address

4) Navigate to the "API Keys" section

5) Generate a new API key (may take 2–3 hours to activate)

### Step 4: Configure Environment
```bash
  OPENWEATHER_API_KEY=your_api_key_here
```
## Usage
 ```bash
 python main.py
  ```
## Project Structure
```bash
weather-data-logger/
│
├── main.py               # Main application file
├── .env                  # Environment variables (create this)
├── weather_data.db       # SQLite database (auto-generated)
├── weather_logs.txt      # Application logs (auto-generated)
├── data/                 # Data folder (auto-generated)
├── logs/                 # Logs folder (auto-generated)
└── README.md             # Project documentation
```
## Database Schema
```bash
weather_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    temperature REAL,
    feels_like REAL,
    humidity INTEGER,
    pressure INTEGER,
    weather_condition TEXT,
    wind_speed REAL,
    timestamp TEXT,
    api_response TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
```
## Sample Weather Output
```bash
============================================================
WEATHER FOR London, GB
============================================================
Temperature: 15.5°C
Feels Like: 14.8°C
Condition: Clear Sky
Humidity: 65%
Pressure: 1013 hPa
Wind Speed: 3.6 m/s
Time: 2024-01-15 14:30:45
============================================================
Data logged to database successfully!
============================================================
```
## Configuration
### Environment Variables
OPENWEATHER_API_KEY — Your OpenWeatherMap API key
### Customization Options
Change database path in Config.DATABASE_PATH

Modify log file location in Config.LOG_FILE

Adjust API timeout settings in WeatherFetcher.fetch_weather()

## Troubleshooting

### API Key Not Working

Wait 2–3 hours after generating the key

Ensure the key is correctly copied to .env

Check for typos

### City Not Found

Verify city name spelling

Use format: City, CountryCode (Example: London, GB)

### Database Errors

Check file permissions

Ensure SQLite is supported on your system

### Network Issues

Check internet connection

Ensure firewall isn’t blocking requests

### Dependencies

requests

python-dotenv

sqlite3 (built-in)

## Screenshots
<img width="1901" height="1079" alt="Image" src="https://github.com/user-attachments/assets/7fee78c0-f763-4501-bd01-9f513e35dbdc" />

<img width="1896" height="481" alt="Image" src="https://github.com/user-attachments/assets/8f1998bd-61e0-4e1d-ac1c-3129782d0cc0" />

<img width="1877" height="789" alt="Image" src="https://github.com/user-attachments/assets/6fc76566-595d-4129-baa2-a0e97d2b4a9d" />

## License

This project was developed as part of the Flipkart Internship Task.
You may modify and reuse it for educational purposes.

## Contributing

1) Fork the repository

2) Create a feature branch:
```bash
git checkout -b feature/AmazingFeature
```
3) commit changes
```bash
git commit -m "Add some AmazingFeature"
```
4)Push branch
```bash
git push origin feature/AmazingFeature
```
5)open pull request

## Author
Samba Siva

Flipkart Internship Task - Python Development
## Acknowledgments
OpenWeatherMap for providing the weather API

Flipkart for the internship opportunity

Python community for excellent documentation and libraries
