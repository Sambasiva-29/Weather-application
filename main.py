
# Author: Samba siva

import requests
import sqlite3
import json
import os
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()





class Config:
    
    API_KEY = os.getenv("OPENWEATHER_API_KEY", "1aa35ea86e073f5700710477e90f1e5f")
    
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    
    # Data Configuration
    DATABASE_PATH = "weather_data.db"
    LOG_FILE = "weather_logs.txt"
    
    @classmethod
    def validate_config(cls):
        
        if not cls.API_KEY:
            print("\n" + "="*60)
            print("ERROR: API KEY NOT FOUND")
            print("="*60)
            print("Please follow these steps:")
            print("\n1. Create a file named '.env' in the same folder")
            print("2. Add this line to the file:")
            print("   OPENWEATHER_API_KEY=your_api_key_here")
            print("\n3. Get your FREE API key from:")
            print("   https://openweathermap.org/api")
            print("\n4. Sign up -> Verify email -> Get API key")
            print("\n5. Replace 'your_api_key_here' with your actual key")
            print("="*60)
            return False
        
        # it Tests if API key is valid
        test_url = f"{cls.BASE_URL}?q=London&appid={cls.API_KEY}"
        try:
            response = requests.get(test_url, timeout=5)
            if response.status_code == 401:
                print("\n" + "="*60)
                print("INVALID API KEY")
                print("="*60)
                print("Your API key is not working. Possible reasons:")
                print("1. Key not activated yet (wait 2-3 hours)")
                print("2. Wrong key entered")
                print("3. Key has expired")
                print("\nGet a new key from: https://openweathermap.org/api")
                print("="*60)
                return False
        except:
            pass  
        
        return True



class DatabaseHandler:
    # it controls all database operations 
    
    def __init__(self):
        self.db_path = Config.DATABASE_PATH
        self._create_tables()
    
    def _create_tables(self):
        
        os.makedirs('data', exist_ok=True)  
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create weather_data table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS weather_data (
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
            ''')
            
            # Creates indexes
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_city ON weather_data(city)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON weather_data(timestamp)')
            
            conn.commit()
    
    def save_weather_data(self, weather_info):
        # stores weather data to database
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO weather_data 
                    (city, country, temperature, feels_like, humidity, pressure, 
                     weather_condition, wind_speed, timestamp, api_response)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    weather_info['city'],
                    weather_info['country'],
                    weather_info['temperature'],
                    weather_info['feels_like'],
                    weather_info['humidity'],
                    weather_info['pressure'],
                    weather_info['weather_condition'],
                    weather_info['wind_speed'],
                    weather_info['timestamp'],
                    json.dumps(weather_info['api_response'])
                ))
                
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Database error: {e}")
            return False
    
    def get_recent_searches(self, limit=10):
        """Retrieve recent weather searches"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT city, country, temperature, weather_condition, timestamp
                    FROM weather_data 
                    ORDER BY created_at DESC 
                    LIMIT ?
                ''', (limit,))
                
                return cursor.fetchall()
                
        except Exception as e:
            print(f"Database error: {e}")
            return []
    
    def get_city_history(self, city_name):
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT city, temperature, weather_condition, timestamp
                    FROM weather_data 
                    WHERE city = ? 
                    ORDER BY created_at DESC
                ''', (city_name,))
                
                return cursor.fetchall()
                
        except Exception as e:
            print(f"Database error: {e}")
            return []



class WeatherFetcher:
    #gets weather data from OpenWeatherMap 
    
    def __init__(self):
        self.api_key = Config.API_KEY
        self.base_url = Config.BASE_URL
        self.db_handler = DatabaseHandler()
    
    def fetch_weather(self, city_name):
        
        try:
            
            if not city_name or not isinstance(city_name, str):
                return {"error": "Invalid city name."}
            
            
            params = {
                'q': city_name,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            
            print(f"\nConnecting to OpenWeatherMap API...")
            response = requests.get(self.base_url, params=params, timeout=10)
            
            
            if response.status_code == 401:
                return {"error": "Invalid API key. Please check your .env file"}
            elif response.status_code == 404:
                return {"error": f"City '{city_name}' not found."}
            elif response.status_code != 200:
                return {"error": f"API Error {response.status_code}: {response.text}"}
            
            response.raise_for_status()
            
            
            data = response.json()
            
            
            weather_info = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'weather_condition': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed'],
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'api_response': data
            }
            
            
            if self.db_handler.save_weather_data(weather_info):
                self._log_to_file(f"Saved data for {city_name}")
            
            return weather_info
            
        except requests.exceptions.ConnectionError:
            return {"error": "No internet connection. Please check your network."}
        except requests.exceptions.Timeout:
            return {"error": "Request timed out. Try again."}
        except Exception as e:
            return {"error": f"Error: {str(e)}"}
    
    def display_weather(self, weather_data):
        # shows weather information
        if 'error' in weather_data:
            print(f"\n{weather_data['error']}")
            return
        
        print("\n" + "="*60)
        print(f"WEATHER FOR {weather_data['city']}, {weather_data['country']}")
        print("="*60)
        print(f"Temperature:    {weather_data['temperature']}°C")
        print(f"Feels Like:      {weather_data['feels_like']}°C")
        print(f"Condition:       {weather_data['weather_condition'].title()}")
        print(f"Humidity:        {weather_data['humidity']}%")
        print(f"Pressure:        {weather_data['pressure']} hPa")
        print(f"Wind Speed:      {weather_data['wind_speed']} m/s")
        print(f"Time:            {weather_data['timestamp']}")
        print("="*60)
        print("Data logged to database successfully!")
        print("="*60)
    
    def _log_to_file(self, message):
        
        try:
            os.makedirs('logs', exist_ok=True)
            with open(Config.LOG_FILE, 'a') as f:
                f.write(f"[{datetime.now()}] {message}\n")
        except:
            pass



class WeatherApplication:
    
    
    def __init__(self):
        self.weather_fetcher = WeatherFetcher()
        self.db_handler = DatabaseHandler()
    
    def display_menu(self):
        
        print("\n" + "="*60)
        print("WEATHER DATA LOGGER - FLIPKART INTERNSHIP TASK")
        print("="*60)
        print("1. Check Weather for City")
        print("2. View Recent Searches")
        print("3. View City History")
        print("4. Check API Status")
        print("5. Exit")
        print("="*60)
    
    def check_weather(self):
        
        city = input("\nEnter city name: ").strip()
        if not city:
            print("Please enter a city name")
            return
        
        print(f"\nFetching weather for {city}...")
        weather = self.weather_fetcher.fetch_weather(city)
        self.weather_fetcher.display_weather(weather)
    
    def view_recent_searches(self):
        
        print("\n" + "="*60)
        print(" RECENT WEATHER SEARCHES")
        print("="*60)
        
        searches = self.db_handler.get_recent_searches()
        
        if not searches:
            print("No searches yet. Check weather for a city first!")
        else:
            for i, (city, country, temp, condition, time) in enumerate(searches, 1):
                print(f"{i}. {city}, {country}")
                print(f"     {temp}°C |   {condition.title()}")
                print(f"   {time}")
                print("-" * 50)
    
    def view_city_history(self):
        
        city = input("\nEnter city name: ").strip()
        if not city:
            print("Please enter a city name")
            return
        
        history = self.db_handler.get_city_history(city)
        
        print("\n" + "="*60)
        print(f"HISTORY FOR {city.upper()}")
        print("="*60)
        
        if not history:
            print(f"No history found for {city}")
        else:
            for i, (city_name, temp, condition, time) in enumerate(history, 1):
                print(f"{i}. {temp}°C | {condition.title()}")
                print(f"   {time}")
                print("-" * 50)
    
    def check_api_status(self):
        
        print("\n" + "="*60)
        print("API CONFIGURATION STATUS")
        print("="*60)
        
        if Config.API_KEY:
            masked_key = Config.API_KEY[:8] + "..." + Config.API_KEY[-4:]
            print(f"API Key: {masked_key}")
        else:
            print("API Key: Not configured")
        
        print(f"Base URL: {Config.BASE_URL}")
        print(f"Database: {Config.DATABASE_PATH}")
        print(f"Log File: {Config.LOG_FILE}")
        print("="*60)
        
        
        print("\n🔍 Testing API connection...")
        try:
            test_url = f"{Config.BASE_URL}?q=London&appid={Config.API_KEY}"
            response = requests.get(test_url, timeout=5)
            if response.status_code == 200:
                print("API Connection: SUCCESS")
            else:
                print(f"API Connection: FAILED (Code: {response.status_code})")
        except Exception as e:
            print(f"API Connection: FAILED ({e})")
    
    def run(self):
        
        print("\n" + "="*60)
        print("WEATHER DATA LOGGER STARTING...")
        print("="*60)
        
        
        if not Config.validate_config():
            print("\nApplication cannot start. Please fix the issues above.")
            input("\nPress Enter to exit...")
            return
        
        print("\n Configuration validated successfully!")
        print(" Database initialized!")
        print(" Ready to fetch weather data!\n")
        
        
        while True:
            self.display_menu()
            
            try:
                choice = input("\nEnter choice (1-5): ").strip()
                
                if choice == '1':
                    self.check_weather()
                elif choice == '2':
                    self.view_recent_searches()
                elif choice == '3':
                    self.view_city_history()
                elif choice == '4':
                    self.check_api_status()
                elif choice == '5':
                    print("\nThank you for using Weather Data Logger!")
                    print("Goodbye!")
                    break
                else:
                    print(" Invalid choice. Enter 1-5")
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n Application interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}")



def main():
    
    try:
        
        try:
            import requests
            from dotenv import load_dotenv
        except ImportError:
            print("\nMissing required packages!")
            print("Install them with: pip install requests python-dotenv")
            return
        
        
        app = WeatherApplication()
        app.run()
        
    except Exception as e:
        print(f"\nFatal error: {e}")
        print("Please check your setup and try again.")

if __name__ == "__main__":
    main()