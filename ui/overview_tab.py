"""Overview tab - Quick glance at all data with polished card design."""
import tkinter as tk
from datetime import datetime
from config.constants import *


class OverviewTab(tk.Frame):
    """Overview tab showing summary of all data with beautiful card layouts."""

    def __init__(self, parent, app_data):
        """Initialize overview tab."""
        super().__init__(parent, bg=BG_COLOR)
        self.app_data = app_data

        # Create scrollable container
        self.canvas = tk.Canvas(self, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.content_frame = tk.Frame(self.canvas, bg=BG_COLOR)
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        # Enable touch scrolling
        from ui.components import enable_touch_scroll
        enable_touch_scroll(self.canvas)

        # Compact title with emoji and time on same line
        title_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        title_frame.pack(pady=(PADDING, PADDING // 2))

        self.title_label = tk.Label(
            title_frame,
            text=f"📊 OVERVIEW",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold')
        )
        self.title_label.pack(side=tk.LEFT, padx=(PADDING * 2, PADDING))

        self.time_label = tk.Label(
            title_frame,
            text=f"{datetime.now().strftime('%I:%M %p')}",
            bg=BG_COLOR,
            fg=TEXT_MUTED,
            font=(FONT_FAMILY, FONT_SIZE_SMALL)
        )
        self.time_label.pack(side=tk.LEFT)

        # Create card sections
        self._create_river_card()
        self._create_weather_card()
        self._create_indoor_card()

        # Configure canvas scrolling
        self.content_frame.bind('<Configure>',
                               lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

    def _create_river_card(self):
        """Create river information card."""
        # Card container
        card = tk.Frame(
            self.content_frame,
            bg=CARD_BG,
            relief=tk.FLAT,
            borderwidth=0
        )
        card.pack(fill=tk.X, padx=PADDING * 2, pady=PADDING // 2)

        # Header with emoji
        header = tk.Frame(card, bg=CARD_BG)
        header.pack(fill=tk.X, padx=PADDING, pady=(PADDING, PADDING // 2))

        tk.Label(
            header,
            text="🏞️ RIVERS",
            bg=CARD_BG,
            fg=ACCENT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold')
        ).pack(side=tk.LEFT)

        # Content area
        self.river_content_frame = tk.Frame(card, bg=CARD_BG)
        self.river_content_frame.pack(fill=tk.X, padx=PADDING, pady=(0, PADDING))

        # Placeholder label (will be replaced with real data)
        self.river_name_label = tk.Label(
            self.river_content_frame,
            text="No river pinned",
            bg=CARD_BG,
            fg=TEXT_MUTED,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            anchor='w'
        )
        self.river_name_label.pack(fill=tk.X, pady=2)

    def _create_weather_card(self):
        """Create weather information card."""
        # Card container
        card = tk.Frame(
            self.content_frame,
            bg=CARD_BG,
            relief=tk.FLAT,
            borderwidth=0
        )
        card.pack(fill=tk.X, padx=PADDING * 2, pady=PADDING // 2)

        # Header with emoji
        header = tk.Frame(card, bg=CARD_BG)
        header.pack(fill=tk.X, padx=PADDING, pady=(PADDING, PADDING // 2))

        tk.Label(
            header,
            text="🌤️ WEATHER",
            bg=CARD_BG,
            fg=ACCENT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold')
        ).pack(side=tk.LEFT)

        # Content area
        self.weather_content_frame = tk.Frame(card, bg=CARD_BG)
        self.weather_content_frame.pack(fill=tk.X, padx=PADDING, pady=(0, PADDING))

        # Placeholder labels (will be replaced with real data)
        self.weather_location_label = tk.Label(
            self.weather_content_frame,
            text="Loading...",
            bg=CARD_BG,
            fg=TEXT_MUTED,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            anchor='w'
        )
        self.weather_location_label.pack(fill=tk.X, pady=2)

    def _create_indoor_card(self):
        """Create indoor air quality card."""
        # Card container
        card = tk.Frame(
            self.content_frame,
            bg=CARD_BG,
            relief=tk.FLAT,
            borderwidth=0
        )
        card.pack(fill=tk.X, padx=PADDING * 2, pady=PADDING // 2)

        # Header with emoji
        header = tk.Frame(card, bg=CARD_BG)
        header.pack(fill=tk.X, padx=PADDING, pady=(PADDING, PADDING // 2))

        tk.Label(
            header,
            text="🏠 INDOOR AIR",
            bg=CARD_BG,
            fg=ACCENT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold')
        ).pack(side=tk.LEFT)

        # Content area
        self.indoor_content_frame = tk.Frame(card, bg=CARD_BG)
        self.indoor_content_frame.pack(fill=tk.X, padx=PADDING, pady=(0, PADDING))

        # Placeholder labels (will be replaced with real data)
        self.indoor_main_label = tk.Label(
            self.indoor_content_frame,
            text="Reading sensors...",
            bg=CARD_BG,
            fg=TEXT_MUTED,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            anchor='w'
        )
        self.indoor_main_label.pack(fill=tk.X, pady=2)

    def update_display(self):
        """Update all sections with latest data."""
        # Update timestamp
        self.time_label.config(text=f"as of {datetime.now().strftime('%I:%M %p')}")

        # Update rivers
        self._update_rivers()

        # Update weather
        self._update_weather()

        # Update indoor
        self._update_indoor()

    def _update_rivers(self):
        """Update rivers section with pinned river."""
        # Clear existing content
        for widget in self.river_content_frame.winfo_children():
            widget.destroy()

        pinned_river = self.app_data.get('pinned_river')
        river_data = self.app_data.get('river_data', {})

        if pinned_river and pinned_river in river_data:
            data = river_data[pinned_river]
            name = pinned_river[0]  # River name from tuple
            site_data = data

            # River name with star
            name_label = tk.Label(
                self.river_content_frame,
                text=f"★ {name}",
                bg=CARD_BG,
                fg=TEXT_COLOR,
                font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold'),
                anchor='w'
            )
            name_label.pack(fill=tk.X, pady=(0, PADDING // 2))

            # Flow data
            flow_cfs = site_data.get('flow_cfs')
            if flow_cfs:
                flow_frame = tk.Frame(self.river_content_frame, bg=CARD_BG)
                flow_frame.pack(fill=tk.X, pady=2)

                tk.Label(
                    flow_frame,
                    text="💧 Flow:",
                    bg=CARD_BG,
                    fg=TEXT_MUTED,
                    font=(FONT_FAMILY, FONT_SIZE_SMALL),
                    width=10,
                    anchor='w'
                ).pack(side=tk.LEFT)

                # Calculate flow change
                flow_text = f"{flow_cfs:,.0f} CFS"
                flow_color = TEXT_COLOR

                if site_data.get('flow_24h_ago'):
                    change = flow_cfs - site_data['flow_24h_ago']
                    if change > 0:
                        flow_text += f"  ↑ {abs(change):,.0f}"
                        flow_color = RIVER_HIGH
                    elif change < 0:
                        flow_text += f"  ↓ {abs(change):,.0f}"
                        flow_color = RIVER_LOW
                    else:
                        flow_text += "  →"
                        flow_color = RIVER_NORMAL

                tk.Label(
                    flow_frame,
                    text=flow_text,
                    bg=CARD_BG,
                    fg=flow_color,
                    font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold'),
                    anchor='w'
                ).pack(side=tk.LEFT)

            # Temperature data
            temp_f = site_data.get('temp_f')
            if temp_f and temp_f > -100:  # Filter out bad data
                temp_frame = tk.Frame(self.river_content_frame, bg=CARD_BG)
                temp_frame.pack(fill=tk.X, pady=2)

                tk.Label(
                    temp_frame,
                    text="🌡️ Temp:",
                    bg=CARD_BG,
                    fg=TEXT_MUTED,
                    font=(FONT_FAMILY, FONT_SIZE_SMALL),
                    width=10,
                    anchor='w'
                ).pack(side=tk.LEFT)

                # Calculate temp change
                temp_text = f"{temp_f:.1f}°F"
                temp_color = TEXT_COLOR

                if site_data.get('temp_24h_ago') and site_data['temp_24h_ago'] > -100:
                    change = temp_f - site_data['temp_24h_ago']
                    if abs(change) > 0.5:
                        if change > 0:
                            temp_text += f"  ↑ {abs(change):.1f}°"
                            temp_color = WARNING_ORANGE
                        else:
                            temp_text += f"  ↓ {abs(change):.1f}°"
                            temp_color = ACCENT_COLOR

                tk.Label(
                    temp_frame,
                    text=temp_text,
                    bg=CARD_BG,
                    fg=temp_color,
                    font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold'),
                    anchor='w'
                ).pack(side=tk.LEFT)

        else:
            # No river pinned
            tk.Label(
                self.river_content_frame,
                text="⭐ No river pinned",
                bg=CARD_BG,
                fg=TEXT_MUTED,
                font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
                anchor='w'
            ).pack(fill=tk.X)

            tk.Label(
                self.river_content_frame,
                text="Go to River Conditions tab to pin a favorite",
                bg=CARD_BG,
                fg=TEXT_FAINT,
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                anchor='w'
            ).pack(fill=tk.X, pady=(5, 0))

    def _update_weather(self):
        """Update weather section with default town."""
        # Clear existing content
        for widget in self.weather_content_frame.winfo_children():
            widget.destroy()

        weather_data = self.app_data.get('weather_data', {})

        if weather_data:
            # Get first location (default)
            first_location = list(weather_data.keys())[0] if weather_data else None

            if first_location and first_location in weather_data:
                data = weather_data[first_location]
                current = data.get('current', {})
                periods = data.get('periods', [])

                # Location and current conditions
                location_frame = tk.Frame(self.weather_content_frame, bg=CARD_BG)
                location_frame.pack(fill=tk.X, pady=(0, PADDING // 2))

                emoji = current.get('icon', '🌤️')
                temp = current.get('temperature', 'N/A')
                condition = current.get('conditions', 'N/A')

                tk.Label(
                    location_frame,
                    text=f"{emoji} {first_location}",
                    bg=CARD_BG,
                    fg=TEXT_COLOR,
                    font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold'),
                    anchor='w'
                ).pack(side=tk.LEFT)

                # Current temperature - large and prominent
                current_frame = tk.Frame(self.weather_content_frame, bg=CARD_BG)
                current_frame.pack(fill=tk.X, pady=2)

                tk.Label(
                    current_frame,
                    text=f"{temp}°F",
                    bg=CARD_BG,
                    fg=ACCENT_COLOR,
                    font=(FONT_FAMILY, FONT_SIZE_LARGE, 'bold'),
                    anchor='w'
                ).pack(side=tk.LEFT, padx=(0, 10))

                tk.Label(
                    current_frame,
                    text=condition,
                    bg=CARD_BG,
                    fg=TEXT_COLOR,
                    font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
                    anchor='w'
                ).pack(side=tk.LEFT)

                # Next 24 hours high/low
                if len(periods) >= 2:
                    forecast_frame = tk.Frame(self.weather_content_frame, bg=CARD_BG)
                    forecast_frame.pack(fill=tk.X, pady=2)

                    high = periods[0].get('temperature', 'N/A')
                    low = periods[1].get('temperature', 'N/A')

                    tk.Label(
                        forecast_frame,
                        text="Next 24hrs:",
                        bg=CARD_BG,
                        fg=TEXT_MUTED,
                        font=(FONT_FAMILY, FONT_SIZE_SMALL),
                        anchor='w'
                    ).pack(side=tk.LEFT, padx=(0, 10))

                    tk.Label(
                        forecast_frame,
                        text=f"↑ {high}°F",
                        bg=CARD_BG,
                        fg=WARNING_ORANGE,
                        font=(FONT_FAMILY, FONT_SIZE_SMALL, 'bold'),
                        anchor='w'
                    ).pack(side=tk.LEFT, padx=(0, 10))

                    tk.Label(
                        forecast_frame,
                        text=f"↓ {low}°F",
                        bg=CARD_BG,
                        fg=ACCENT_COLOR,
                        font=(FONT_FAMILY, FONT_SIZE_SMALL, 'bold'),
                        anchor='w'
                    ).pack(side=tk.LEFT)

            else:
                tk.Label(
                    self.weather_content_frame,
                    text="No weather data available",
                    bg=CARD_BG,
                    fg=TEXT_MUTED,
                    font=(FONT_FAMILY, FONT_SIZE_MEDIUM)
                ).pack(fill=tk.X)
        else:
            tk.Label(
                self.weather_content_frame,
                text="Loading weather data...",
                bg=CARD_BG,
                fg=TEXT_MUTED,
                font=(FONT_FAMILY, FONT_SIZE_MEDIUM)
            ).pack(fill=tk.X)

    def _update_indoor(self):
        """Update indoor section with sensor data."""
        # Clear existing content
        for widget in self.indoor_content_frame.winfo_children():
            widget.destroy()

        sensor_data = self.app_data.get('sensor_data', {})

        if sensor_data:
            temp = sensor_data.get('temperature', 'N/A')
            humidity = sensor_data.get('humidity', 'N/A')
            pm25 = sensor_data.get('pm25', 'N/A')

            # Get air quality status and color
            if isinstance(pm25, (int, float)):
                if pm25 <= 12:
                    status = "Good"
                    status_color = FOREST_COLOR
                    emoji = "✅"
                elif pm25 <= 35:
                    status = "Moderate"
                    status_color = MODERATE_YELLOW
                    emoji = "⚠️"
                elif pm25 <= 55:
                    status = "Unhealthy for Sensitive"
                    status_color = WARNING_ORANGE
                    emoji = "⚠️"
                elif pm25 <= 150:
                    status = "Unhealthy"
                    status_color = ALERT_RED
                    emoji = "🚨"
                else:
                    status = "Very Unhealthy"
                    status_color = UNHEALTHY_PURPLE
                    emoji = "🚨"
            else:
                status = "N/A"
                status_color = TEXT_MUTED
                emoji = "❓"

            # Main sensor grid
            grid_frame = tk.Frame(self.indoor_content_frame, bg=CARD_BG)
            grid_frame.pack(fill=tk.X, pady=(0, PADDING // 2))

            # Temperature
            temp_frame = tk.Frame(grid_frame, bg=CARD_BG)
            temp_frame.pack(side=tk.LEFT, padx=(0, 20))

            tk.Label(
                temp_frame,
                text="🌡️",
                bg=CARD_BG,
                fg=TEXT_COLOR,
                font=(FONT_FAMILY, FONT_SIZE_LARGE)
            ).pack()

            tk.Label(
                temp_frame,
                text=f"{temp}°F",
                bg=CARD_BG,
                fg=TEXT_COLOR,
                font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold')
            ).pack()

            # Humidity
            humid_frame = tk.Frame(grid_frame, bg=CARD_BG)
            humid_frame.pack(side=tk.LEFT, padx=(0, 20))

            tk.Label(
                humid_frame,
                text="💧",
                bg=CARD_BG,
                fg=TEXT_COLOR,
                font=(FONT_FAMILY, FONT_SIZE_LARGE)
            ).pack()

            tk.Label(
                humid_frame,
                text=f"{humidity}%",
                bg=CARD_BG,
                fg=ACCENT_COLOR,
                font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold')
            ).pack()

            # Air Quality - larger emphasis
            quality_frame = tk.Frame(self.indoor_content_frame, bg=CARD_BG)
            quality_frame.pack(fill=tk.X, pady=PADDING // 2)

            tk.Label(
                quality_frame,
                text=f"{emoji} Air Quality: {status}",
                bg=CARD_BG,
                fg=status_color,
                font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold'),
                anchor='w'
            ).pack(fill=tk.X)

            if isinstance(pm25, (int, float)):
                tk.Label(
                    quality_frame,
                    text=f"PM2.5: {pm25:.1f} µg/m³",
                    bg=CARD_BG,
                    fg=TEXT_MUTED,
                    font=(FONT_FAMILY, FONT_SIZE_SMALL),
                    anchor='w'
                ).pack(fill=tk.X, pady=(2, 0))

        else:
            tk.Label(
                self.indoor_content_frame,
                text="📊 Reading sensors...",
                bg=CARD_BG,
                fg=TEXT_MUTED,
                font=(FONT_FAMILY, FONT_SIZE_MEDIUM)
            ).pack(fill=tk.X)
