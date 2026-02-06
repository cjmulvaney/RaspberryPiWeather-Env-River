"""USGS Water Services API client for river data."""
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import json
import os


class USGSClient:
    """Client for fetching river data from USGS Water Services API."""

    BASE_URL = "https://waterservices.usgs.gov/nwis/iv/"

    def __init__(self, cache_dir: str = "cache"):
        """Initialize USGS client with caching."""
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def fetch_site_data(self, site_id: str) -> Optional[Dict]:
        """
        Fetch current and 24-hour data for a site.
        Returns dict with: flow_cfs, flow_24h_ago, temp_f, temp_24h_ago, timestamp
        """
        try:
            # Request last 25 hours of data
            period = "P1D"  # Last 1 day

            # Parameter codes: 00060 = discharge (cfs), 00010 = temperature (C)
            params = {
                'format': 'json',
                'sites': site_id,
                'parameterCd': '00060,00010',
                'period': period
            }

            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Parse the response
            result = self._parse_usgs_response(data, site_id)

            # Cache the result
            if result:
                self._cache_site_data(site_id, result)

            return result

        except Exception as e:
            print(f"Error fetching USGS data for {site_id}: {e}")
            # Try to load from cache
            return self._load_cached_data(site_id)

    def _parse_usgs_response(self, data: dict, site_id: str) -> Optional[Dict]:
        """Parse USGS JSON response."""
        try:
            time_series = data['value']['timeSeries']

            result = {
                'site_id': site_id,
                'flow_cfs': None,
                'flow_24h_ago': None,
                'temp_f': None,
                'temp_24h_ago': None,
                'timestamp': None,
                'error': None
            }

            for series in time_series:
                variable_code = series['variable']['variableCode'][0]['value']
                values = series['values'][0]['value']

                if not values:
                    continue

                # Get current (most recent) value
                current = values[-1]
                current_value = float(current['value'])
                current_time = current['dateTime']

                # Get 24h ago value (approximately)
                value_24h = None
                if len(values) > 1:
                    # Look for value ~24 hours ago
                    target_time = datetime.fromisoformat(current_time.replace('Z', '+00:00')) - timedelta(hours=24)

                    closest_value = None
                    closest_diff = None

                    for val in values:
                        val_time = datetime.fromisoformat(val['dateTime'].replace('Z', '+00:00'))
                        diff = abs((val_time - target_time).total_seconds())

                        if closest_diff is None or diff < closest_diff:
                            closest_diff = diff
                            closest_value = float(val['value'])

                    value_24h = closest_value

                # Discharge (CFS)
                if variable_code == '00060':
                    result['flow_cfs'] = round(current_value, 1)
                    result['flow_24h_ago'] = round(value_24h, 1) if value_24h else None

                # Temperature (Celsius to Fahrenheit)
                elif variable_code == '00010':
                    temp_f = (current_value * 9/5) + 32
                    result['temp_f'] = round(temp_f, 1)

                    if value_24h is not None:
                        temp_24h_f = (value_24h * 9/5) + 32
                        result['temp_24h_ago'] = round(temp_24h_f, 1)

                result['timestamp'] = current_time

            return result

        except Exception as e:
            print(f"Error parsing USGS response for {site_id}: {e}")
            return None

    def _cache_site_data(self, site_id: str, data: Dict):
        """Save site data to cache file."""
        cache_file = os.path.join(self.cache_dir, f"usgs_{site_id}.json")
        try:
            with open(cache_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error caching data for {site_id}: {e}")

    def _load_cached_data(self, site_id: str) -> Optional[Dict]:
        """Load site data from cache file."""
        cache_file = os.path.join(self.cache_dir, f"usgs_{site_id}.json")
        try:
            if os.path.exists(cache_file):
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                    data['cached'] = True
                    return data
        except Exception as e:
            print(f"Error loading cached data for {site_id}: {e}")
        return None

    def fetch_multiple_sites(self, site_ids: List[str]) -> Dict[str, Dict]:
        """
        Fetch data for multiple sites.
        Returns dict: {site_id: data_dict}
        """
        results = {}
        for site_id in site_ids:
            data = self.fetch_site_data(site_id)
            if data:
                results[site_id] = data
        return results
