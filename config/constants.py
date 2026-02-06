"""UI styling constants and configuration."""

# Nature-inspired color palette
# Deep, nature-inspired colors that work well with environmental data
BG_COLOR = "#0c0a09"              # Deep black (darker than stone)
TEXT_COLOR = "#fef3c7"            # Cream - easy on eyes
TEXT_MUTED = "rgba(254, 243, 199, 0.8)"  # Muted cream
TEXT_FAINT = "rgba(254, 243, 199, 0.6)"  # Faint cream

# Primary theme colors
ACCENT_COLOR = "#0369a1"          # Sky blue - for primary actions
ACCENT_LIGHT = "#0c4a6e"          # Deep sky - for hover/active
FOREST_COLOR = "#166534"          # Forest green - for success/good
FOREST_DARK = "#14532d"           # Deep forest - for emphasis

# UI Elements
BUTTON_BG = "#44403c"             # Stone - neutral buttons
BUTTON_HOVER = "#57534e"          # Light stone - hover state
CARD_BG = "#1c1917"               # Slightly lighter than background for cards
OVERLAY_BG = "rgba(0, 0, 0, 0.7)" # Dark overlay for modals

# Status colors
GOOD_GREEN = "#166534"            # Forest green
MODERATE_YELLOW = "#ca8a04"       # Warm yellow
WARNING_ORANGE = "#ea580c"        # Bright orange
ALERT_RED = "#dc2626"             # Strong red
UNHEALTHY_PURPLE = "#7e22ce"      # Purple for very unhealthy

# River flow colors (relative to normal)
RIVER_HIGH = "#0369a1"            # Sky blue for high flow
RIVER_NORMAL = "#166534"          # Forest for normal
RIVER_LOW = "#ea580c"             # Orange for low flow

# Weather condition colors
WEATHER_SUNNY = "#fbbf24"         # Warm yellow
WEATHER_CLOUDY = "#6b7280"        # Gray
WEATHER_RAIN = "#0369a1"          # Sky blue
WEATHER_SNOW = "#e0f2fe"          # Light blue
WEATHER_STORM = "#4c1d95"         # Deep purple

# Legacy compatibility (keeping old names for existing code)
ALERT_YELLOW = WARNING_ORANGE
ALERT_ORANGE = WARNING_ORANGE
GOOD_GREEN = FOREST_COLOR

# Fonts
FONT_FAMILY = "Helvetica"
FONT_SIZE_LARGE = 22
FONT_SIZE_MEDIUM = 18
FONT_SIZE_SMALL = 14
FONT_SIZE_XLARGE = 26

# Spacing
PADDING = 10
BUTTON_HEIGHT = 50
TAB_HEIGHT = 60
BUTTON_MIN_SIZE = 50

# Window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 480

# Update intervals (seconds)
API_UPDATE_INTERVAL = 3600      # 60 minutes for river/weather
SENSOR_DISPLAY_INTERVAL = 5     # 5 seconds for display update
SENSOR_LOG_INTERVAL = 60        # 60 seconds for database logging

# Alert settings
PM25_ALERT_THRESHOLD = 35.0     # Unhealthy for sensitive groups
ALERT_DISMISS_DURATION = 1200   # 20 minutes in seconds

# Air quality thresholds (PM2.5) with colors
AQI_THRESHOLDS = {
    'good': (0, 12, FOREST_COLOR),
    'moderate': (12, 35, MODERATE_YELLOW),
    'unhealthy_sensitive': (35, 55, WARNING_ORANGE),
    'unhealthy': (55, 150, ALERT_RED),
    'very_unhealthy': (150, float('inf'), UNHEALTHY_PURPLE)
}

# Pagination
RIVERS_PER_PAGE = 5

# Weather emoji mapping (enhanced)
WEATHER_EMOJIS = {
    'clear': '☀️',
    'sunny': '☀️',
    'mostly sunny': '🌤️',
    'partly sunny': '⛅',
    'partly cloudy': '⛅',
    'mostly cloudy': '☁️',
    'cloudy': '☁️',
    'overcast': '☁️',
    'rain': '🌧️',
    'showers': '🌧️',
    'light rain': '🌦️',
    'heavy rain': '⛈️',
    'thunderstorm': '⛈️',
    'storm': '⛈️',
    'snow': '❄️',
    'light snow': '🌨️',
    'heavy snow': '❄️',
    'sleet': '🌨️',
    'freezing': '🧊',
    'fog': '🌫️',
    'mist': '🌫️',
    'haze': '🌫️',
    'windy': '💨',
    'default': '🌤️'
}
