import os
import requests
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class WeatherService:
    """Service for fetching weather data from OpenWeatherMap API."""
    
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        if not self.api_key:
            raise ValueError("OPENWEATHER_API_KEY not found in environment variables")
        
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    def get_weather(self, location: str) -> Dict:
        """
        Get current weather data for a location.
        
        Args:
            location: City name (e.g., "Jakarta")
            
        Returns:
            Dictionary containing weather data
        """
        try:
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract relevant weather information
            weather_info = {
                'location': data['name'],
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'],
                'main': data['weather'][0]['main'],
                'rain_probability': self._calculate_rain_probability(data),
                'raw_data': data
            }
            
            return weather_info
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching weather data: {str(e)}")
        except KeyError as e:
            raise Exception(f"Error parsing weather data: {str(e)}")
    
    def _calculate_rain_probability(self, data: Dict) -> float:
        """
        Calculate rain probability based on weather conditions.
        
        Args:
            data: Raw weather data from API
            
        Returns:
            Rain probability as percentage (0-100)
        """
        # Check if rain data is available
        if 'rain' in data:
            # Rain data available, return high probability
            return 80.0
        
        # Check weather conditions
        main_weather = data['weather'][0]['main'].lower()
        description = data['weather'][0]['description'].lower()
        
        # High probability conditions
        if 'rain' in main_weather or 'rain' in description:
            return 75.0
        elif 'drizzle' in main_weather or 'drizzle' in description:
            return 60.0
        elif 'thunderstorm' in main_weather or 'storm' in description:
            return 85.0
        
        # Medium probability conditions
        elif 'clouds' in main_weather:
            if 'overcast' in description or 'broken' in description:
                return 40.0
            else:
                return 25.0
        
        # Low probability conditions
        elif 'clear' in main_weather or 'sunny' in description:
            return 5.0
        
        # Default for unknown conditions
        return 30.0
    
    def parse_rain_probability(self, weather_data: Dict) -> float:
        """
        Parse rain probability from weather data.
        
        Args:
            weather_data: Weather data dictionary
            
        Returns:
            Rain probability as percentage
        """
        return weather_data.get('rain_probability', 0.0)