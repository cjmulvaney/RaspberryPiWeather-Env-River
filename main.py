"""
Montana River Dashboard - Main Application
A touchscreen dashboard for Raspberry Pi 5 with 7" display (800x480)
Monitors Montana river conditions, weather forecasts, and indoor environmental sensors.
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
from datetime import datetime

# Import configuration
from config.constants import *
from config.rivers import RIVER_STATIONS
from config.towns import WEATHER_LOCATIONS

# Import data modules
from data.database import SensorDatabase
from data.sensors import SensorReader
from data.usgs_api import USGSClient
from data.nws_api import NWSClient

# Import UI components
from ui.overview_tab import OverviewTab
from ui.river_tab import RiverTab
from ui.weather_tab import WeatherTab
from ui.indoor_tab import IndoorTab
from ui.components import TouchButton

# Platform detection
from utils.platform_detect import is_raspberry_pi, get_platform_name


class RiverDashboard(tk.Tk):
    """Main dashboard application."""

    def __init__(self):
        """Initialize dashboard application."""
        super().__init__()

        # Window configuration
        self.title("Montana River Dashboard")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.configure(bg=BG_COLOR)

        # Make window resizable for development
        self.resizable(True, True)

        # Platform info
        print(f"Running on: {get_platform_name()}")

        # Initialize data storage
        self.app_data = {
            'sensor_data': {},
            'river_data': {},
            'weather_data': {},
            'pinned_river': None,
            'alert_dismissed_until': None
        }

        # Initialize database
        self.database = SensorDatabase("sensor_data.db")

        # Initialize sensor reader
        self.sensor_reader = SensorReader()

        # Initialize API clients
        self.usgs_client = USGSClient(cache_dir="cache")
        self.nws_client = NWSClient(cache_dir="cache")

        # Threading control
        self.running = True
        self.sensor_thread = None
        self.api_thread = None

        # Create UI
        self.create_ui()

        # Start data collection
        self.start_background_threads()

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Load cached data immediately
        self.load_cached_data()

        # Start immediate API fetch in background
        threading.Thread(target=self.fetch_api_data, daemon=True).start()

    def create_ui(self):
        """Create main UI layout."""
        # Top bar
        top_bar = tk.Frame(self, bg=BUTTON_BG, height=TAB_HEIGHT)
        top_bar.pack(fill=tk.X, side=tk.TOP)
        top_bar.pack_propagate(False)

        # Tab buttons
        self.tab_buttons = {}
        tab_frame = tk.Frame(top_bar, bg=BUTTON_BG)
        tab_frame.pack(side=tk.LEFT, fill=tk.Y)

        tabs = ['Overview', 'River Conditions', 'Weather Forecast', 'Indoor Air']
        for tab_name in tabs:
            btn = TouchButton(
                tab_frame,
                text=tab_name,
                command=lambda t=tab_name: self.switch_tab(t),
                font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
                height=2
            )
            btn.pack(side=tk.LEFT, padx=2, fill=tk.Y)
            self.tab_buttons[tab_name] = btn

        # Refresh button
        refresh_btn = TouchButton(
            top_bar,
            text="🔄",
            command=self.manual_refresh,
            font=(FONT_FAMILY, FONT_SIZE_LARGE),
            width=3
        )
        refresh_btn.pack(side=tk.RIGHT, padx=PADDING)

        # Content area
        self.content_area = tk.Frame(self, bg=BG_COLOR)
        self.content_area.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.tabs = {
            'Overview': OverviewTab(self.content_area, self.app_data),
            'River Conditions': RiverTab(self.content_area, self.app_data),
            'Weather Forecast': WeatherTab(self.content_area, self.app_data),
            'Indoor Air': IndoorTab(self.content_area, self.app_data, self.database)
        }

        # Show Overview tab by default
        self.current_tab = 'Overview'
        self.tabs[self.current_tab].pack(fill=tk.BOTH, expand=True)
        self.tab_buttons[self.current_tab].config(bg=ACCENT_COLOR)

        # Alert overlay (hidden by default)
        self.alert_overlay = None

    def switch_tab(self, tab_name):
        """Switch to a different tab."""
        # Hide current tab
        self.tabs[self.current_tab].pack_forget()
        self.tab_buttons[self.current_tab].config(bg=BUTTON_BG)

        # Show new tab
        self.current_tab = tab_name
        self.tabs[tab_name].pack(fill=tk.BOTH, expand=True)
        self.tab_buttons[tab_name].config(bg=ACCENT_COLOR)

        # Update display
        self.tabs[tab_name].update_display()

    def start_background_threads(self):
        """Start background threads for data collection."""
        # Sensor reading thread
        self.sensor_thread = threading.Thread(target=self.sensor_loop, daemon=True)
        self.sensor_thread.start()

        # API update thread
        self.api_thread = threading.Thread(target=self.api_loop, daemon=True)
        self.api_thread.start()

    def sensor_loop(self):
        """Background loop for reading sensors."""
        last_log_time = 0

        while self.running:
            try:
                # Read sensors
                sensor_data = self.sensor_reader.read()
                self.app_data['sensor_data'] = sensor_data

                # Log to database every 60 seconds
                current_time = time.time()
                if current_time - last_log_time >= SENSOR_LOG_INTERVAL:
                    self.database.log_reading(
                        sensor_data['temperature'],
                        sensor_data['humidity'],
                        sensor_data['pressure'],
                        sensor_data['gas_resistance'],
                        sensor_data['pm1'],
                        sensor_data['pm25'],
                        sensor_data['pm10']
                    )
                    last_log_time = current_time

                # Check for air quality alerts
                self.check_air_quality_alert(sensor_data['pm25'])

                # Update UI (must be done in main thread)
                self.after(0, self.update_sensor_display)

            except Exception as e:
                print(f"Error in sensor loop: {e}")

            # Wait before next reading
            time.sleep(SENSOR_DISPLAY_INTERVAL)

    def api_loop(self):
        """Background loop for API updates."""
        while self.running:
            try:
                self.fetch_api_data()
            except Exception as e:
                print(f"Error in API loop: {e}")

            # Wait for next update cycle
            time.sleep(API_UPDATE_INTERVAL)

    def fetch_api_data(self):
        """Fetch data from APIs."""
        print("Fetching API data...")

        # Fetch river data
        try:
            site_ids = [site_id for name, site_id, has_temp in RIVER_STATIONS]
            river_results = self.usgs_client.fetch_multiple_sites(site_ids)

            # Map results back to river info tuples
            for river_info in RIVER_STATIONS:
                name, site_id, has_temp = river_info
                if site_id in river_results:
                    self.app_data['river_data'][river_info] = river_results[site_id]

            print(f"Fetched data for {len(river_results)} river stations")
        except Exception as e:
            print(f"Error fetching river data: {e}")

        # Fetch weather data
        try:
            weather_results = self.nws_client.fetch_multiple_locations(WEATHER_LOCATIONS)
            self.app_data['weather_data'] = weather_results

            print(f"Fetched weather for {len(weather_results)} locations")
        except Exception as e:
            print(f"Error fetching weather data: {e}")

        # Update UI
        self.after(0, self.update_all_displays)

    def load_cached_data(self):
        """Load cached API data on startup."""
        print("Loading cached data...")

        # Load cached river data
        for river_info in RIVER_STATIONS:
            name, site_id, has_temp = river_info
            cached_data = self.usgs_client._load_cached_data(site_id)
            if cached_data:
                self.app_data['river_data'][river_info] = cached_data

        # Load cached weather data
        for name, state, lat, lon in WEATHER_LOCATIONS:
            full_name = f"{name}, {state}"
            cached_data = self.nws_client._load_cached_forecast(full_name)
            if cached_data:
                self.app_data['weather_data'][full_name] = cached_data

        # Update displays
        self.update_all_displays()

    def manual_refresh(self):
        """Manually trigger API refresh."""
        print("Manual refresh triggered")

        # Show updating indicator
        refresh_thread = threading.Thread(target=self.fetch_api_data, daemon=True)
        refresh_thread.start()

    def update_sensor_display(self):
        """Update sensor-related displays."""
        if self.current_tab in ['Overview', 'Indoor Air']:
            self.tabs[self.current_tab].update_display()

    def update_all_displays(self):
        """Update all tab displays."""
        for tab in self.tabs.values():
            if hasattr(tab, 'update_display'):
                tab.update_display()

    def check_air_quality_alert(self, pm25):
        """Check if air quality alert should be shown."""
        if not isinstance(pm25, (int, float)):
            return

        # Check if alert is dismissed
        if self.app_data['alert_dismissed_until']:
            if time.time() < self.app_data['alert_dismissed_until']:
                return
            else:
                self.app_data['alert_dismissed_until'] = None

        # Check if PM2.5 exceeds threshold
        if pm25 >= PM25_ALERT_THRESHOLD:
            # Don't show alert if already on Indoor Air tab
            if self.current_tab == 'Indoor Air':
                return

            # Show alert if not already shown
            if not self.alert_overlay:
                self.after(0, lambda: self.show_alert(pm25))

    def show_alert(self, pm25):
        """Show air quality alert overlay."""
        if self.alert_overlay:
            return

        # Determine severity
        if pm25 <= 55:
            level = "Unhealthy for Sensitive Groups"
            color = ALERT_ORANGE
        elif pm25 <= 150:
            level = "Unhealthy"
            color = ALERT_RED
        else:
            level = "Very Unhealthy"
            color = "#8b0000"

        # Create overlay
        self.alert_overlay = tk.Frame(self, bg=BG_COLOR, relief=tk.RAISED, borderwidth=3)
        self.alert_overlay.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=500, height=200)

        # Title
        title = tk.Label(
            self.alert_overlay,
            text="⚠️  AIR QUALITY ALERT",
            bg=BG_COLOR,
            fg=color,
            font=(FONT_FAMILY, FONT_SIZE_LARGE, 'bold')
        )
        title.pack(pady=PADDING * 2)

        # Message
        message = tk.Label(
            self.alert_overlay,
            text=f"PM2.5: {pm25} µg/m³ ({level})\nConsider closing windows or running filter",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            justify=tk.CENTER
        )
        message.pack(pady=PADDING)

        # Buttons
        button_frame = tk.Frame(self.alert_overlay, bg=BG_COLOR)
        button_frame.pack(pady=PADDING * 2)

        dismiss_btn = TouchButton(
            button_frame,
            text="Dismiss",
            command=self.dismiss_alert,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM)
        )
        dismiss_btn.pack(side=tk.LEFT, padx=PADDING)

        details_btn = TouchButton(
            button_frame,
            text="View Details",
            command=self.view_alert_details,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM)
        )
        details_btn.pack(side=tk.LEFT, padx=PADDING)

    def dismiss_alert(self):
        """Dismiss alert for 20 minutes."""
        if self.alert_overlay:
            self.alert_overlay.destroy()
            self.alert_overlay = None

        # Set dismissal time
        self.app_data['alert_dismissed_until'] = time.time() + ALERT_DISMISS_DURATION

    def view_alert_details(self):
        """View details by switching to Indoor Air tab."""
        if self.alert_overlay:
            self.alert_overlay.destroy()
            self.alert_overlay = None

        self.switch_tab('Indoor Air')

    def on_closing(self):
        """Handle application closing."""
        print("Shutting down...")
        self.running = False

        # Wait for threads to finish
        if self.sensor_thread:
            self.sensor_thread.join(timeout=1)
        if self.api_thread:
            self.api_thread.join(timeout=1)

        self.destroy()


def main():
    """Main entry point."""
    print("=" * 50)
    print("Montana River Dashboard")
    print("=" * 50)

    try:
        app = RiverDashboard()
        app.mainloop()
    except Exception as e:
        print("\n" + "=" * 50)
        print("ERROR: Application crashed!")
        print("=" * 50)
        print(f"Error: {e}")
        print("\nFull traceback:")
        import traceback
        traceback.print_exc()
        print("\n" + "=" * 50)
        print("Troubleshooting:")
        print("1. Run: python3 debug_pi.py")
        print("2. Run: ./diagnose.sh")
        print("3. Check: PI_TROUBLESHOOTING.md")
        print("=" * 50)
        import sys
        sys.exit(1)


if __name__ == "__main__":
    main()
