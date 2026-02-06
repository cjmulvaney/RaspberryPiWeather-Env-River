"""National Weather Service API client for weather forecasts."""
import requests
from typing import Dict, Optional, List
import json
import os


class NWSClient:
    """Client for fetching weather data from National Weather Service API."""

    BASE_URL = "https://api.weather.gov"

    def __init__(self, cache_dir: str = "cache"):
        """Initialize NWS client with caching."""
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

        # User agent required by NWS API
        self.headers = {
            'User-Agent': '(RiverDashboard, contact@example.com)',
            'Accept': 'application/json'
        }

    def fetch_forecast(self, lat: float, lon: float, location_name: str) -> Optional[Dict]:
        """
        Fetch weather forecast for a location.
        Returns dict with current conditions and forecast periods.
        """
        try:
            # Step 1: Get grid point data
            point_url = f"{self.BASE_URL}/points/{lat},{lon}"
            point_response = requests.get(point_url, headers=self.headers, timeout=10)
            point_response.raise_for_status()
            point_data = point_response.json()

            # Extract forecast URL
            forecast_url = point_data['properties']['forecast']
            forecast_hourly_url = point_data['properties']['forecastHourly']

            # Step 2: Get forecast
            forecast_response = requests.get(forecast_url, headers=self.headers, timeout=10)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()

            # Step 3: Get hourly forecast for current conditions
            hourly_response = requests.get(forecast_hourly_url, headers=self.headers, timeout=10)
            hourly_response.raise_for_status()
            hourly_data = hourly_response.json()

            # Parse the data
            result = self._parse_nws_forecast(forecast_data, hourly_data, location_name)

            # Cache the result
            if result:
                self._cache_forecast(location_name, result)

            return result

        except Exception as e:
            print(f"Error fetching NWS data for {location_name}: {e}")
            # Try to load from cache
            return self._load_cached_forecast(location_name)

    def _parse_nws_forecast(self, forecast_data: dict, hourly_data: dict,
                           location_name: str) -> Optional[Dict]:
        """Parse NWS forecast response."""
        try:
            periods = forecast_data['properties']['periods']
            hourly_periods = hourly_data['properties']['periods']

            # Current conditions from first hourly period
            current = hourly_periods[0] if hourly_periods else periods[0]

            result = {
                'location': location_name,
                'current': {
                    'temperature': current['temperature'],
                    'conditions': current['shortForecast'],
                    'wind_speed': current.get('windSpeed', 'N/A'),
                    'wind_direction': current.get('windDirection', 'N/A'),
                    'humidity': current.get('relativeHumidity', {}).get('value', 'N/A'),
                    'icon': self._get_emoji_from_forecast(current['shortForecast'])
                },
                'periods': [],
                'timestamp': current['startTime']
            }

            # Add forecast periods (today, tonight, tomorrow, etc.)
            for period in periods[:7]:  # Next 7 periods
                result['periods'].append({
                    'name': period['name'],
                    'temperature': period['temperature'],
                    'conditions': period['shortForecast'],
                    'detailed_forecast': period['detailedForecast'],
                    'wind_speed': period.get('windSpeed', 'N/A'),
                    'wind_direction': period.get('windDirection', 'N/A'),
                    'humidity': period.get('relativeHumidity', {}).get('value', 'N/A'),
                    'precipitation_chance': period.get('probabilityOfPrecipitation', {}).get('value', 0),
                    'icon': self._get_emoji_from_forecast(period['shortForecast'])
                })

            return result

        except Exception as e:
            print(f"Error parsing NWS forecast for {location_name}: {e}")
            return None

    def _get_emoji_from_forecast(self, forecast: str) -> str:
        """Convert forecast text to weather emoji."""
        forecast_lower = forecast.lower()

        if 'thunder' in forecast_lower or 'storm' in forecast_lower:
            return '⛈️'
        elif 'rain' in forecast_lower or 'shower' in forecast_lower:
            return '🌧️'
        elif 'snow' in forecast_lower:
            return '❄️'
        elif 'cloud' in forecast_lower or 'overcast' in forecast_lower:
            return '☁️'
        elif 'partly' in forecast_lower or 'mostly sunny' in forecast_lower:
            return '⛅'
        elif 'sunny' in forecast_lower or 'clear' in forecast_lower:
            return '☀️'
        else:
            return '🌤️'

    def _cache_forecast(self, location_name: str, data: Dict):
        """Save forecast data to cache file."""
        cache_file = os.path.join(self.cache_dir, f"nws_{location_name.replace(' ', '_')}.json")
        try:
            with open(cache_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error caching forecast for {location_name}: {e}")

    def _load_cached_forecast(self, location_name: str) -> Optional[Dict]:
        """Load forecast data from cache file."""
        cache_file = os.path.join(self.cache_dir, f"nws_{location_name.replace(' ', '_')}.json")
        try:
            if os.path.exists(cache_file):
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                    data['cached'] = True
                    return data
        except Exception as e:
            print(f"Error loading cached forecast for {location_name}: {e}")
        return None

    def fetch_multiple_locations(self, locations: List[tuple]) -> Dict[str, Dict]:
        """
        Fetch forecasts for multiple locations.
        locations: List of (name, state, lat, lon) tuples
        Returns dict: {location_name: forecast_dict}
        """
        results = {}
        for name, state, lat, lon in locations:
            full_name = f"{name}, {state}"
            forecast = self.fetch_forecast(lat, lon, full_name)
            if forecast:
                results[full_name] = forecast
        return results
