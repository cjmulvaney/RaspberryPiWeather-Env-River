"""UI styling constants and configuration."""

# Colors
BG_COLOR = "#1a1a1a"          # Dark background
TEXT_COLOR = "#ffffff"         # White text
ACCENT_COLOR = "#4a9eff"       # Blue accent
BUTTON_BG = "#2d2d2d"          # Button background
BUTTON_HOVER = "#3d3d3d"       # Button hover
ALERT_YELLOW = "#ffa500"       # Warning
ALERT_RED = "#ff4444"          # Danger
GOOD_GREEN = "#44ff44"         # Good status
ALERT_ORANGE = "#ff8c00"       # Unhealthy for sensitive

# Fonts
FONT_FAMILY = "Helvetica"
FONT_SIZE_LARGE = 22
FONT_SIZE_MEDIUM = 18
FONT_SIZE_SMALL = 14

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

# Air quality thresholds (PM2.5)
AQI_THRESHOLDS = {
    'good': (0, 12),
    'moderate': (12, 35),
    'unhealthy_sensitive': (35, 55),
    'unhealthy': (55, 150),
    'very_unhealthy': (150, float('inf'))
}

# Pagination
RIVERS_PER_PAGE = 5
