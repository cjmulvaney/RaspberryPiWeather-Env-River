"""Overview tab - Quick glance at all data in horizontal layout."""
import tkinter as tk
from datetime import datetime
from config.constants import *


class OverviewTab(tk.Frame):
    """Overview tab showing summary of all data in efficient horizontal layout."""

    def __init__(self, parent, app_data):
        """Initialize overview tab."""
        super().__init__(parent, bg=BG_COLOR)
        self.app_data = app_data

        # NO SCROLLING - Everything fits on one screen
        # Compact title with emoji and time on same line
        title_frame = tk.Frame(self, bg=BG_COLOR)
        title_frame.pack(fill=tk.X, pady=(PADDING // 2, PADDING // 2))

        self.title_label = tk.Label(
            title_frame,
            text=f"📊 OVERVIEW",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold')
        )
        self.title_label.pack(side=tk.LEFT, padx=(PADDING, PADDING // 2))

        self.time_label = tk.Label(
            title_frame,
            text=f"{datetime.now().strftime('%I:%M %p')}",
            bg=BG_COLOR,
            fg=TEXT_MUTED,
            font=(FONT_FAMILY, FONT_SIZE_SMALL)
        )
        self.time_label.pack(side=tk.LEFT)

        # HORIZONTAL LAYOUT - Two columns for better space usage
        columns_frame = tk.Frame(self, bg=BG_COLOR)
        columns_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING)

        # Left column - Rivers and Weather
        left_column = tk.Frame(columns_frame, bg=BG_COLOR)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, PADDING // 2))

        # Right column - Indoor Air
        right_column = tk.Frame(columns_frame, bg=BG_COLOR)
        right_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(PADDING // 2, 0))

        # Create cards in columns
        self._create_river_card(left_column)
        self._create_weather_card(left_column)
        self._create_indoor_card(right_column)

    def _create_river_card(self, parent):
        """Create river information card."""
        card = tk.Frame(parent, bg=CARD_BG, relief=tk.FLAT, borderwidth=0)
        card.pack(fill=tk.BOTH, expand=True, pady=(0, PADDING // 2))

        # Header
        header = tk.Label(
            card,
            text="🏞️ RIVERS",
            bg=CARD_BG,
            fg=ACCENT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_SMALL, 'bold')
        )
        header.pack(fill=tk.X, padx=PADDING // 2, pady=(PADDING // 2, 0))

        # Content
        self.river_content_frame = tk.Frame(card, bg=CARD_BG)
        self.river_content_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING // 2, pady=(0, PADDING // 2))

        # Placeholder
        self.river_name_label = tk.Label(
            self.river_content_frame,
            text="No river pinned",
            bg=CARD_BG,
            fg=TEXT_MUTED,
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            anchor='w'
        )
        self.river_name_label.pack(fill=tk.X, pady=2)

    def _create_weather_card(self, parent):
        """Create weather information card."""
        card = tk.Frame(parent, bg=CARD_BG, relief=tk.FLAT, borderwidth=0)
        card.pack(fill=tk.BOTH, expand=True, pady=(PADDING // 2, 0))

        # Header
        header = tk.Label(
            card,
            text="🌤️ WEATHER",
            bg=CARD_BG,
            fg=ACCENT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_SMALL, 'bold')
        )
        header.pack(fill=tk.X, padx=PADDING // 2, pady=(PADDING // 2, 0))

        # Content
        self.weather_content_frame = tk.Frame(card, bg=CARD_BG)
        self.weather_content_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING // 2, pady=(0, PADDING // 2))

        # Placeholder
        self.weather_location_label = tk.Label(
            self.weather_content_frame,
            text="Loading...",
            bg=CARD_BG,
            fg=TEXT_MUTED,
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            anchor='w'
        )
        self.weather_location_label.pack(fill=tk.X, pady=2)

    def _create_indoor_card(self, parent):
        """Create indoor air quality card - FULL HEIGHT."""
        card = tk.Frame(parent, bg=CARD_BG, relief=tk.FLAT, borderwidth=0)
        card.pack(fill=tk.BOTH, expand=True)

        # Header
        header = tk.Label(
            card,
            text="🏠 INDOOR AIR",
            bg=CARD_BG,
            fg=ACCENT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_SMALL, 'bold')
        )
        header.pack(fill=tk.X, padx=PADDING // 2, pady=(PADDING // 2, 0))

        # Content
        self.indoor_content_frame = tk.Frame(card, bg=CARD_BG)
        self.indoor_content_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING // 2, pady=(0, PADDING // 2))

        # Placeholder
        self.indoor_main_label = tk.Label(
            self.indoor_content_frame,
            text="Reading sensors...",
            bg=CARD_BG,
            fg=TEXT_MUTED,
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
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
        for widget in self.river_content_frame.winfo_children():
            widget.destroy()

        pinned_river = self.app_data.get('pinned_river')
        river_data = self.app_data.get('river_data', {})

        if pinned_river and pinned_river in river_data:
            data = river_data[pinned_river]
            name = pinned_river[0]

            # River name
            name_label = tk.Label(
                self.river_content_frame,
                text=f"★ {name}",
                bg=CARD_BG,
                fg=TEXT_COLOR,
                font=(FONT_FAMILY, FONT_SIZE_SMALL, 'bold'),
                anchor='w',
                wraplength=280
            )
            name_label.pack(fill=tk.X, pady=(0, 2))

            # Flow data - compact
            flow_cfs = data.get('flow_cfs')
            if flow_cfs:
                flow_text = f"💧 {flow_cfs:,.0f} CFS"
                flow_color = TEXT_COLOR

                if data.get('flow_24h_ago'):
                    change = flow_cfs - data['flow_24h_ago']
                    if change > 0:
                        flow_text += f" ↑{abs(change):,.0f}"
                        flow_color = RIVER_HIGH
                    elif change < 0:
                        flow_text += f" ↓{abs(change):,.0f}"
                        flow_color = RIVER_LOW

                tk.Label(
                    self.river_content_frame,
                    text=flow_text,
                    bg=CARD_BG,
                    fg=flow_color,
                    font=(FONT_FAMILY, FONT_SIZE_SMALL),
                    anchor='w'
                ).pack(fill=tk.X, pady=1)

            # Temperature data - compact
            temp_f = data.get('temp_f')
            if temp_f and temp_f > -100:
                temp_text = f"🌡️ {temp_f:.1f}°F"
                temp_color = TEXT_COLOR

                if data.get('temp_24h_ago') and data['temp_24h_ago'] > -100:
                    change = temp_f - data['temp_24h_ago']
                    if abs(change) > 0.5:
                        if change > 0:
                            temp_text += f" ↑{abs(change):.1f}°"
                            temp_color = WARNING_ORANGE
                        else:
                            temp_text += f" ↓{abs(change):.1f}°"
                            temp_color = ACCENT_COLOR

                tk.Label(
                    self.river_content_frame,
                    text=temp_text,
                    bg=CARD_BG,
                    fg=temp_color,
                    font=(FONT_FAMILY, FONT_SIZE_SMALL),
                    anchor='w'
                ).pack(fill=tk.X, pady=1)
        else:
            tk.Label(
                self.river_content_frame,
                text="⭐ No river pinned\nGo to River Conditions\nto pin a favorite",
                bg=CARD_BG,
                fg=TEXT_MUTED,
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                anchor='w',
                justify=tk.LEFT
            ).pack(fill=tk.X)

    def _update_weather(self):
        """Update weather section with default town."""
        for widget in self.weather_content_frame.winfo_children():
            widget.destroy()

        weather_data = self.app_data.get('weather_data', {})

        if weather_data:
            first_location = list(weather_data.keys())[0] if weather_data else None

            if first_location and first_location in weather_data:
                data = weather_data[first_location]
                current = data.get('current', {})
                periods = data.get('periods', [])

                # Location with emoji
                emoji = current.get('icon', '🌤️')
                temp = current.get('temperature', 'N/A')
                condition = current.get('conditions', 'N/A')

                tk.Label(
                    self.weather_content_frame,
                    text=f"{emoji} {first_location}",
                    bg=CARD_BG,
                    fg=TEXT_COLOR,
                    font=(FONT_FAMILY, FONT_SIZE_SMALL, 'bold'),
                    anchor='w'
                ).pack(fill=tk.X, pady=(0, 2))

                # Temperature - large
                tk.Label(
                    self.weather_content_frame,
                    text=f"{temp}°F",
                    bg=CARD_BG,
                    fg=ACCENT_COLOR,
                    font=(FONT_FAMILY, FONT_SIZE_LARGE, 'bold'),
                    anchor='w'
                ).pack(fill=tk.X, pady=1)

                # Condition
                tk.Label(
                    self.weather_content_frame,
                    text=condition,
                    bg=CARD_BG,
                    fg=TEXT_COLOR,
                    font=(FONT_FAMILY, FONT_SIZE_SMALL),
                    anchor='w',
                    wraplength=280
                ).pack(fill=tk.X, pady=1)

                # Next 24hrs high/low - compact
                if len(periods) >= 2:
                    high = periods[0].get('temperature', 'N/A')
                    low = periods[1].get('temperature', 'N/A')

                    tk.Label(
                        self.weather_content_frame,
                        text=f"Next 24hrs: ↑{high}°F  ↓{low}°F",
                        bg=CARD_BG,
                        fg=TEXT_MUTED,
                        font=(FONT_FAMILY, FONT_SIZE_SMALL),
                        anchor='w'
                    ).pack(fill=tk.X, pady=(2, 0))
            else:
                tk.Label(
                    self.weather_content_frame,
                    text="No weather data",
                    bg=CARD_BG,
                    fg=TEXT_MUTED,
                    font=(FONT_FAMILY, FONT_SIZE_SMALL)
                ).pack(fill=tk.X)
        else:
            tk.Label(
                self.weather_content_frame,
                text="Loading weather...",
                bg=CARD_BG,
                fg=TEXT_MUTED,
                font=(FONT_FAMILY, FONT_SIZE_SMALL)
            ).pack(fill=tk.X)

    def _update_indoor(self):
        """Update indoor section with sensor data."""
        for widget in self.indoor_content_frame.winfo_children():
            widget.destroy()

        sensor_data = self.app_data.get('sensor_data', {})

        if sensor_data:
            temp = sensor_data.get('temperature', 'N/A')
            humidity = sensor_data.get('humidity', 'N/A')
            pressure = sensor_data.get('pressure', 'N/A')
            pm25 = sensor_data.get('pm25', 'N/A')

            # Get air quality status
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

            # Temperature - large
            tk.Label(
                self.indoor_content_frame,
                text=f"🌡️ {temp}°F",
                bg=CARD_BG,
                fg=TEXT_COLOR,
                font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold'),
                anchor='w'
            ).pack(fill=tk.X, pady=(0, 4))

            # Humidity
            tk.Label(
                self.indoor_content_frame,
                text=f"💧 {humidity}%",
                bg=CARD_BG,
                fg=ACCENT_COLOR,
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                anchor='w'
            ).pack(fill=tk.X, pady=2)

            # Pressure
            if isinstance(pressure, (int, float)):
                tk.Label(
                    self.indoor_content_frame,
                    text=f"🎈 {pressure:.2f} inHg",
                    bg=CARD_BG,
                    fg=TEXT_MUTED,
                    font=(FONT_FAMILY, FONT_SIZE_SMALL),
                    anchor='w'
                ).pack(fill=tk.X, pady=2)

            # Air Quality - prominent
            tk.Label(
                self.indoor_content_frame,
                text=f"{emoji} Air: {status}",
                bg=CARD_BG,
                fg=status_color,
                font=(FONT_FAMILY, FONT_SIZE_SMALL, 'bold'),
                anchor='w'
            ).pack(fill=tk.X, pady=(4, 2))

            # PM2.5 detail
            if isinstance(pm25, (int, float)):
                tk.Label(
                    self.indoor_content_frame,
                    text=f"PM2.5: {pm25:.1f} µg/m³",
                    bg=CARD_BG,
                    fg=TEXT_MUTED,
                    font=(FONT_FAMILY, FONT_SIZE_SMALL),
                    anchor='w'
                ).pack(fill=tk.X, pady=1)
        else:
            tk.Label(
                self.indoor_content_frame,
                text="📊 Reading sensors...",
                bg=CARD_BG,
                fg=TEXT_MUTED,
                font=(FONT_FAMILY, FONT_SIZE_SMALL)
            ).pack(fill=tk.X)
