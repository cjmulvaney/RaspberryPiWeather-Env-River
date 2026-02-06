"""Overview tab - Quick glance at all data."""
import tkinter as tk
from datetime import datetime
from config.constants import *


class OverviewTab(tk.Frame):
    """Overview tab showing summary of all data."""

    def __init__(self, parent, app_data):
        """Initialize overview tab."""
        super().__init__(parent, bg=BG_COLOR)
        self.app_data = app_data

        # Create scrollable container
        self.canvas = tk.Canvas(self, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.content_frame = tk.Frame(self.canvas, bg=BG_COLOR)
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        # Title
        self.title_label = tk.Label(
            self.content_frame,
            text=f"OVERVIEW (as of {datetime.now().strftime('%I:%M %p')})",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_LARGE, 'bold')
        )
        self.title_label.pack(pady=PADDING)

        # Rivers section
        self.rivers_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        self.rivers_frame.pack(fill=tk.X, padx=PADDING * 2, pady=PADDING)

        self.rivers_title = tk.Label(
            self.rivers_frame,
            text="Rivers:",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold'),
            anchor='w'
        )
        self.rivers_title.pack(fill=tk.X)

        self.rivers_content = tk.Label(
            self.rivers_frame,
            text="Loading river data...",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            anchor='w',
            justify=tk.LEFT
        )
        self.rivers_content.pack(fill=tk.X, padx=PADDING * 2)

        # Weather section
        self.weather_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        self.weather_frame.pack(fill=tk.X, padx=PADDING * 2, pady=PADDING)

        self.weather_title = tk.Label(
            self.weather_frame,
            text="Weather:",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold'),
            anchor='w'
        )
        self.weather_title.pack(fill=tk.X)

        self.weather_content = tk.Label(
            self.weather_frame,
            text="Loading weather data...",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            anchor='w',
            justify=tk.LEFT
        )
        self.weather_content.pack(fill=tk.X, padx=PADDING * 2)

        # Indoor section
        self.indoor_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        self.indoor_frame.pack(fill=tk.X, padx=PADDING * 2, pady=PADDING)

        self.indoor_title = tk.Label(
            self.indoor_frame,
            text="Indoor:",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold'),
            anchor='w'
        )
        self.indoor_title.pack(fill=tk.X)

        self.indoor_content = tk.Label(
            self.indoor_frame,
            text="Reading sensors...",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            anchor='w',
            justify=tk.LEFT
        )
        self.indoor_content.pack(fill=tk.X, padx=PADDING * 2)

        # Configure canvas scrolling
        self.content_frame.bind('<Configure>',
                               lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

    def update_display(self):
        """Update all sections with latest data."""
        # Update timestamp
        self.title_label.config(text=f"OVERVIEW (as of {datetime.now().strftime('%I:%M %p')})")

        # Update rivers
        self._update_rivers()

        # Update weather
        self._update_weather()

        # Update indoor
        self._update_indoor()

    def _update_rivers(self):
        """Update rivers section with pinned river."""
        pinned_river = self.app_data.get('pinned_river')
        river_data = self.app_data.get('river_data', {})

        if pinned_river and pinned_river in river_data:
            data = river_data[pinned_river]
            name = pinned_river[0]  # River name from tuple
            site_data = data

            flow_text = f"{site_data.get('flow_cfs', 'N/A')} CFS" if site_data.get('flow_cfs') else "N/A"
            temp_text = f"{site_data.get('temp_f', 'N/A')}°F" if site_data.get('temp_f') else "N/A"

            # Calculate changes
            flow_change = ""
            if site_data.get('flow_cfs') and site_data.get('flow_24h_ago'):
                change = site_data['flow_cfs'] - site_data['flow_24h_ago']
                arrow = "↑" if change > 0 else "↓"
                flow_change = f" ({arrow} {abs(change):.0f})"

            temp_change = ""
            if site_data.get('temp_f') and site_data.get('temp_24h_ago'):
                change = site_data['temp_f'] - site_data['temp_24h_ago']
                arrow = "↑" if change > 0 else "↓"
                temp_change = f" ({arrow} {abs(change):.1f}°)"

            text = f"★ {name}: {flow_text}{flow_change} • {temp_text}{temp_change}"
            self.rivers_content.config(text=text)
        else:
            self.rivers_content.config(text="No river pinned")

    def _update_weather(self):
        """Update weather section with default town."""
        weather_data = self.app_data.get('weather_data', {})

        if weather_data:
            # Get first location (default)
            first_location = list(weather_data.keys())[0] if weather_data else None

            if first_location and first_location in weather_data:
                data = weather_data[first_location]
                current = data.get('current', {})
                periods = data.get('periods', [])

                temp = current.get('temperature', 'N/A')
                condition = current.get('conditions', 'N/A')

                # Get high/low from today and tonight
                high = periods[0].get('temperature', 'N/A') if len(periods) > 0 else 'N/A'
                low = periods[1].get('temperature', 'N/A') if len(periods) > 1 else 'N/A'

                text = f"{first_location}: {temp}°F, {condition}\n"
                text += f"Next 24hrs: High {high}°F, Low {low}°F"

                self.weather_content.config(text=text)
            else:
                self.weather_content.config(text="No weather data available")
        else:
            self.weather_content.config(text="Loading weather data...")

    def _update_indoor(self):
        """Update indoor section with sensor data."""
        sensor_data = self.app_data.get('sensor_data', {})

        if sensor_data:
            temp = sensor_data.get('temperature', 'N/A')
            humidity = sensor_data.get('humidity', 'N/A')
            pm25 = sensor_data.get('pm25', 'N/A')

            # Get air quality status
            if isinstance(pm25, (int, float)):
                if pm25 <= 12:
                    status = "Good"
                elif pm25 <= 35:
                    status = "Moderate"
                elif pm25 <= 55:
                    status = "Unhealthy for Sensitive"
                elif pm25 <= 150:
                    status = "Unhealthy"
                else:
                    status = "Very Unhealthy"
            else:
                status = "N/A"

            text = f"Home: {temp}°F • {humidity}% • {status}\n"
            text += f"PM2.5: {pm25} µg/m³"

            self.indoor_content.config(text=text)
        else:
            self.indoor_content.config(text="Reading sensors...")
