"""Weather Forecast tab - Multi-location weather display."""
import tkinter as tk
from datetime import datetime
from config.constants import *
from config.towns import WEATHER_LOCATIONS
from ui.components import TouchButton


class WeatherTab(tk.Frame):
    """Weather forecast tab with location selection."""

    def __init__(self, parent, app_data):
        """Initialize weather tab."""
        super().__init__(parent, bg=BG_COLOR)
        self.app_data = app_data
        self.selected_location = None

        # Horizontal split: sidebar + content
        self.sidebar = tk.Frame(self, bg=BUTTON_BG, width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        self.sidebar.pack_propagate(False)

        self.content_area = tk.Frame(self, bg=BG_COLOR)
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create sidebar buttons
        self.location_buttons = {}
        self.create_sidebar()

        # Create content area with scrolling
        self.canvas = tk.Canvas(self.content_area, bg=BG_COLOR, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.content_area, orient="vertical", command=self.canvas.yview)
        self.content_frame = tk.Frame(self.canvas, bg=BG_COLOR)

        self.content_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Enable touch scrolling
        from ui.components import enable_touch_scroll
        enable_touch_scroll(self.canvas)

        # Select first location by default
        if WEATHER_LOCATIONS:
            first_location = f"{WEATHER_LOCATIONS[0][0]}, {WEATHER_LOCATIONS[0][1]}"
            self.select_location(first_location)

    def create_sidebar(self):
        """Create town selection buttons in sidebar."""
        weather_data = self.app_data.get('weather_data', {})

        for location_tuple in WEATHER_LOCATIONS:
            name, state, lat, lon = location_tuple
            full_name = f"{name}, {state}"

            # Button frame
            btn_frame = tk.Frame(self.sidebar, bg=BUTTON_BG)
            btn_frame.pack(fill=tk.X, pady=2)

            # Location name
            btn = TouchButton(
                btn_frame,
                text=name,
                command=lambda loc=full_name: self.select_location(loc),
                font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold'),
                width=15,
                anchor='w'
            )
            btn.pack(fill=tk.X, padx=5, pady=2)

            # Current temp and icon
            if full_name in weather_data:
                data = weather_data[full_name]
                current = data.get('current', {})
                temp = current.get('temperature', '?')
                icon = current.get('icon', '')

                info_label = tk.Label(
                    btn_frame,
                    text=f"{temp}°F {icon}",
                    bg=BUTTON_BG,
                    fg=TEXT_COLOR,
                    font=(FONT_FAMILY, FONT_SIZE_SMALL)
                )
                info_label.pack(fill=tk.X, padx=5)
            else:
                info_label = tk.Label(
                    btn_frame,
                    text="Loading...",
                    bg=BUTTON_BG,
                    fg=TEXT_COLOR,
                    font=(FONT_FAMILY, FONT_SIZE_SMALL)
                )
                info_label.pack(fill=tk.X, padx=5)

            self.location_buttons[full_name] = (btn, info_label, btn_frame)

    def select_location(self, location_name):
        """Select a location and display its forecast."""
        self.selected_location = location_name

        # Update sidebar to show selection
        for loc, (btn, info_label, btn_frame) in self.location_buttons.items():
            if loc == location_name:
                btn.config(text=btn['text'] + " ◄──")
                btn_frame.config(bg=ACCENT_COLOR)
                btn.config(bg=ACCENT_COLOR)
                info_label.config(bg=ACCENT_COLOR)
            else:
                # Remove arrow if present
                text = btn['text'].replace(" ◄──", "")
                btn.config(text=text)
                btn_frame.config(bg=BUTTON_BG)
                btn.config(bg=BUTTON_BG)
                info_label.config(bg=BUTTON_BG)

        # Display forecast
        self.display_forecast()

    def display_forecast(self):
        """Display detailed forecast for selected location."""
        # Clear content area
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if not self.selected_location:
            return

        weather_data = self.app_data.get('weather_data', {})

        if self.selected_location not in weather_data:
            error_label = tk.Label(
                self.content_frame,
                text="Weather data not available",
                bg=BG_COLOR,
                fg=ALERT_YELLOW,
                font=(FONT_FAMILY, FONT_SIZE_LARGE)
            )
            error_label.pack(pady=20)
            return

        data = weather_data[self.selected_location]
        current = data.get('current', {})
        periods = data.get('periods', [])

        # Title
        title = tk.Label(
            self.content_frame,
            text=f"{self.selected_location.upper()} FORECAST",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_LARGE, 'bold')
        )
        title.pack(pady=PADDING)

        # Current conditions
        current_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        current_frame.pack(fill=tk.X, padx=PADDING * 2, pady=PADDING)

        current_title = tk.Label(
            current_frame,
            text="Current Conditions:",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold')
        )
        current_title.pack(anchor='w')

        temp = current.get('temperature', 'N/A')
        conditions = current.get('conditions', 'N/A')
        humidity = current.get('humidity', 'N/A')
        wind_speed = current.get('wind_speed', 'N/A')
        wind_direction = current.get('wind_direction', 'N/A')

        current_text = f"{temp}°F, {conditions}\n"
        current_text += f"Humidity: {humidity}% • Wind: {wind_speed} {wind_direction}"

        current_label = tk.Label(
            current_frame,
            text=current_text,
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            justify=tk.LEFT
        )
        current_label.pack(anchor='w', padx=PADDING * 2)

        # Forecast periods
        for period in periods:
            period_frame = tk.Frame(self.content_frame, bg=CARD_BG)
            period_frame.pack(fill=tk.X, padx=PADDING * 2, pady=PADDING)

            # Period name and temp with emoji
            emoji = period.get('icon', '🌤️')
            period_header = tk.Label(
                period_frame,
                text=f"{emoji} {period['name']}: {period['temperature']}°F",
                bg=CARD_BG,
                fg=TEXT_COLOR,
                font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold')
            )
            period_header.pack(anchor='w', padx=PADDING, pady=(PADDING, 0))

            # Conditions
            conditions_text = f"{period['conditions']} • {period['precipitation_chance']}% chance precipitation"
            conditions_label = tk.Label(
                period_frame,
                text=conditions_text,
                bg=CARD_BG,
                fg=TEXT_COLOR,
                font=(FONT_FAMILY, FONT_SIZE_SMALL)
            )
            conditions_label.pack(anchor='w', padx=PADDING)

            # Wind and humidity
            wind_text = f"Wind: {period['wind_speed']} {period['wind_direction']}"
            if period['humidity'] != 'N/A':
                wind_text += f" • Humidity: {period['humidity']}%"

            wind_label = tk.Label(
                period_frame,
                text=wind_text,
                bg=CARD_BG,
                fg=TEXT_COLOR,
                font=(FONT_FAMILY, FONT_SIZE_SMALL)
            )
            wind_label.pack(anchor='w', padx=PADDING, pady=(0, PADDING))

        # Last updated
        timestamp = data.get('timestamp', 'Unknown')
        if timestamp != 'Unknown':
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                timestamp = dt.strftime('%I:%M %p %m/%d')
            except:
                pass

        cached_text = " ⚠️ (cached)" if data.get('cached') else ""
        time_label = tk.Label(
            self.content_frame,
            text=f"Last Updated: {timestamp}{cached_text}",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_SMALL)
        )
        time_label.pack(pady=PADDING)

    def update_display(self):
        """Update display with latest data."""
        # Refresh sidebar with new temps
        self.refresh_sidebar()

        # Refresh forecast if location is selected
        if self.selected_location:
            self.display_forecast()

    def refresh_sidebar(self):
        """Refresh sidebar with updated temperatures."""
        weather_data = self.app_data.get('weather_data', {})

        for loc, (btn, info_label, btn_frame) in self.location_buttons.items():
            if loc in weather_data:
                data = weather_data[loc]
                current = data.get('current', {})
                temp = current.get('temperature', '?')
                icon = current.get('icon', '')
                info_label.config(text=f"{temp}°F {icon}")
            else:
                info_label.config(text="Loading...")
