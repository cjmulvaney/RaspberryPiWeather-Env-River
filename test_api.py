#!/usr/bin/env python3
"""Test script to verify API clients work correctly."""

from data.usgs_api import USGSClient
from data.nws_api import NWSClient

print("=" * 50)
print("API Client Test")
print("=" * 50)

# Test USGS API
print("\n1. Testing USGS River Data API...")
usgs = USGSClient(cache_dir="cache")

# Test with Flathead River at Columbia Falls
site_id = "12363000"
print(f"   Fetching data for site {site_id}...")

try:
    data = usgs.fetch_site_data(site_id)
    if data:
        print("   ✓ Success!")
        print(f"   Flow: {data.get('flow_cfs', 'N/A')} CFS")
        print(f"   Temperature: {data.get('temp_f', 'N/A')}°F")
        print(f"   24h ago flow: {data.get('flow_24h_ago', 'N/A')} CFS")
        print(f"   24h ago temp: {data.get('temp_24h_ago', 'N/A')}°F")
        print(f"   Timestamp: {data.get('timestamp', 'N/A')}")
        print(f"   Cached: {data.get('cached', False)}")
    else:
        print("   ✗ No data returned (this is OK if using cached data)")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test NWS API
print("\n2. Testing NWS Weather Data API...")
nws = NWSClient(cache_dir="cache")

# Test with Polson, MT
lat, lon = 47.6944, -114.1631
print(f"   Fetching forecast for Polson, MT ({lat}, {lon})...")

try:
    data = nws.fetch_forecast(lat, lon, "Polson, MT")
    if data:
        print("   ✓ Success!")
        current = data.get('current', {})
        print(f"   Current temp: {current.get('temperature', 'N/A')}°F")
        print(f"   Conditions: {current.get('conditions', 'N/A')}")
        print(f"   Wind: {current.get('wind_speed', 'N/A')} {current.get('wind_direction', 'N/A')}")
        print(f"   Humidity: {current.get('humidity', 'N/A')}%")

        periods = data.get('periods', [])
        print(f"   Forecast periods: {len(periods)}")
        if periods:
            print(f"   Next period: {periods[0].get('name')} - {periods[0].get('temperature')}°F")

        print(f"   Cached: {data.get('cached', False)}")
    else:
        print("   ✗ No data returned (this is OK if using cached data)")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 50)
print("API Test Complete")
print("Note: API errors are normal if rate limited or offline.")
print("The app will use cached data in those cases.")
print("=" * 50)
