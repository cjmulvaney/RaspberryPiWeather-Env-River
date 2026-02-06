"""Settings tab - Configuration and system controls."""
import tkinter as tk
from tkinter import ttk
from config.constants import *
from ui.components import TouchButton
import subprocess
import os


class SettingsTab(tk.Frame):
    """Settings tab for brightness and update intervals."""

    def __init__(self, parent, app_data, app_instance):
        """Initialize settings tab."""
        super().__init__(parent, bg=BG_COLOR)
        self.app_data = app_data
        self.app = app_instance

        # Settings values
        self.brightness = 100  # 0-100%
        self.sensor_display_interval = SENSOR_DISPLAY_INTERVAL
        self.sensor_log_interval = SENSOR_LOG_INTERVAL
        self.api_update_interval = API_UPDATE_INTERVAL
        self.scroll_sensitivity = SCROLL_SENSITIVITY  # 1-5

        # Create scrollable container
        self.canvas = tk.Canvas(self, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.content_frame = tk.Frame(self.canvas, bg=BG_COLOR)
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        # Enable touch scrolling with current sensitivity
        from ui.components import enable_touch_scroll
        enable_touch_scroll(self.canvas, sensitivity=SCROLL_SENSITIVITY)

        # Title
        title = tk.Label(
            self.content_frame,
            text="⚙️ SETTINGS",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_LARGE, 'bold')
        )
        title.pack(pady=PADDING * 2)

        # Create settings sections
        self._create_display_settings()
        self._create_scroll_settings()
        self._create_update_settings()
        self._create_system_info()

        # Configure canvas scrolling
        self.content_frame.bind('<Configure>',
                               lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

    def _create_display_settings(self):
        """Create display settings section."""
        # Section card
        card = tk.Frame(
            self.content_frame,
            bg=CARD_BG,
            relief=tk.FLAT,
            borderwidth=0
        )
        card.pack(fill=tk.X, padx=PADDING * 2, pady=PADDING)

        # Header
        header = tk.Label(
            card,
            text="🔆 Display Brightness",
            bg=CARD_BG,
            fg=ACCENT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold')
        )
        header.pack(fill=tk.X, padx=PADDING, pady=(PADDING, PADDING // 2))

        # Brightness control frame
        brightness_frame = tk.Frame(card, bg=CARD_BG)
        brightness_frame.pack(fill=tk.X, padx=PADDING * 2, pady=PADDING)

        # Current brightness label
        self.brightness_label = tk.Label(
            brightness_frame,
            text=f"{self.brightness}%",
            bg=CARD_BG,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_XLARGE, 'bold')
        )
        self.brightness_label.pack(pady=PADDING)

        # Brightness slider
        self.brightness_slider = tk.Scale(
            brightness_frame,
            from_=10,
            to=100,
            orient=tk.HORIZONTAL,
            command=self._on_brightness_change,
            bg=CARD_BG,
            fg=TEXT_COLOR,
            troughcolor=BUTTON_BG,
            activebackground=ACCENT_COLOR,
            highlightthickness=0,
            showvalue=False,
            length=300
        )
        self.brightness_slider.set(self.brightness)
        self.brightness_slider.pack(pady=PADDING)

        # Quick brightness buttons
        button_frame = tk.Frame(brightness_frame, bg=CARD_BG)
        button_frame.pack(pady=PADDING)

        for level in [25, 50, 75, 100]:
            btn = TouchButton(
                button_frame,
                text=f"{level}%",
                command=lambda l=level: self._set_brightness(l),
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                width=5
            )
            btn.pack(side=tk.LEFT, padx=2)

        # Note about brightness control
        note = tk.Label(
            brightness_frame,
            text="Note: Brightness control works on Raspberry Pi with official display",
            bg=CARD_BG,
            fg=TEXT_FAINT,
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            wraplength=400,
            justify=tk.CENTER
        )
        note.pack(pady=PADDING)

    def _create_scroll_settings(self):
        """Create scroll sensitivity settings section."""
        # Section card
        card = tk.Frame(
            self.content_frame,
            bg=CARD_BG,
            relief=tk.FLAT,
            borderwidth=0
        )
        card.pack(fill=tk.X, padx=PADDING * 2, pady=PADDING)

        # Header
        header = tk.Label(
            card,
            text="👆 Touch Scroll Sensitivity",
            bg=CARD_BG,
            fg=ACCENT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold')
        )
        header.pack(fill=tk.X, padx=PADDING, pady=(PADDING, PADDING // 2))

        content = tk.Frame(card, bg=CARD_BG)
        content.pack(fill=tk.X, padx=PADDING * 2, pady=PADDING)

        # Description
        description = tk.Label(
            content,
            text="Adjust how fast the screen scrolls when you drag:",
            bg=CARD_BG,
            fg=TEXT_MUTED,
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            anchor='w'
        )
        description.pack(fill=tk.X, pady=(0, PADDING))

        # Sensitivity buttons
        button_frame = tk.Frame(content, bg=CARD_BG)
        button_frame.pack(fill=tk.X, pady=PADDING)

        sensitivity_levels = [
            (1, "Very Slow"),
            (2, "Slow"),
            (3, "Normal"),
            (4, "Fast"),
            (5, "Very Fast")
        ]

        for level, label in sensitivity_levels:
            is_current = (level == self.scroll_sensitivity)

            btn = TouchButton(
                button_frame,
                text=label + (" ✓" if is_current else ""),
                command=lambda l=level: self._set_scroll_sensitivity(l),
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                bg=ACCENT_COLOR if is_current else BUTTON_BG
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2, expand=True, fill=tk.X)

        # Note about restart
        note = tk.Label(
            content,
            text="Note: Changes apply immediately to all scrollable areas",
            bg=CARD_BG,
            fg=TEXT_FAINT,
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            wraplength=400,
            justify=tk.CENTER
        )
        note.pack(pady=PADDING)

    def _create_update_settings(self):
        """Create update interval settings section."""
        # Section card
        card = tk.Frame(
            self.content_frame,
            bg=CARD_BG,
            relief=tk.FLAT,
            borderwidth=0
        )
        card.pack(fill=tk.X, padx=PADDING * 2, pady=PADDING)

        # Header
        header = tk.Label(
            card,
            text="🔄 Update Intervals",
            bg=CARD_BG,
            fg=ACCENT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold')
        )
        header.pack(fill=tk.X, padx=PADDING, pady=(PADDING, PADDING // 2))

        content = tk.Frame(card, bg=CARD_BG)
        content.pack(fill=tk.X, padx=PADDING * 2, pady=PADDING)

        # Sensor Display Interval
        self._create_interval_setting(
            content,
            "📊 Sensor Display Update",
            "sensor_display_interval",
            [1, 5, 10, 30],
            "seconds",
            self.sensor_display_interval
        )

        # Sensor Log Interval
        self._create_interval_setting(
            content,
            "💾 Sensor Database Logging",
            "sensor_log_interval",
            [30, 60, 120, 300],
            "seconds",
            self.sensor_log_interval
        )

        # API Update Interval
        self._create_interval_setting(
            content,
            "🌐 River/Weather API Update",
            "api_update_interval",
            [1800, 3600, 7200],
            "seconds",
            self.api_update_interval,
            custom_labels=["30 min", "60 min", "120 min"]
        )

    def _create_interval_setting(self, parent, label, key, options, unit, current_value, custom_labels=None):
        """Create an interval setting row."""
        setting_frame = tk.Frame(parent, bg=CARD_BG)
        setting_frame.pack(fill=tk.X, pady=PADDING)

        # Label
        tk.Label(
            setting_frame,
            text=label,
            bg=CARD_BG,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_SMALL, 'bold'),
            anchor='w'
        ).pack(fill=tk.X, pady=(0, 5))

        # Button frame
        button_frame = tk.Frame(setting_frame, bg=CARD_BG)
        button_frame.pack(fill=tk.X)

        for i, value in enumerate(options):
            display_label = custom_labels[i] if custom_labels else f"{value} {unit}"
            is_current = (value == current_value)

            btn = TouchButton(
                button_frame,
                text=display_label + (" ✓" if is_current else ""),
                command=lambda v=value, k=key: self._set_interval(k, v),
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                bg=ACCENT_COLOR if is_current else BUTTON_BG
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2)

    def _create_system_info(self):
        """Create system information section."""
        # Section card
        card = tk.Frame(
            self.content_frame,
            bg=CARD_BG,
            relief=tk.FLAT,
            borderwidth=0
        )
        card.pack(fill=tk.X, padx=PADDING * 2, pady=PADDING)

        # Header
        header = tk.Label(
            card,
            text="ℹ️ System Information",
            bg=CARD_BG,
            fg=ACCENT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold')
        )
        header.pack(fill=tk.X, padx=PADDING, pady=(PADDING, PADDING // 2))

        content = tk.Frame(card, bg=CARD_BG)
        content.pack(fill=tk.X, padx=PADDING * 2, pady=PADDING)

        # Get system info
        from utils.platform_detect import get_platform_name, is_raspberry_pi

        info_items = [
            ("Platform", get_platform_name()),
            ("Sensor Mode", "Real Sensors" if is_raspberry_pi() else "Mock Data"),
            ("Display Resolution", f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"),
            ("Database", "sensor_data.db")
        ]

        for label, value in info_items:
            row = tk.Frame(content, bg=CARD_BG)
            row.pack(fill=tk.X, pady=2)

            tk.Label(
                row,
                text=f"{label}:",
                bg=CARD_BG,
                fg=TEXT_MUTED,
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                anchor='w',
                width=20
            ).pack(side=tk.LEFT)

            tk.Label(
                row,
                text=value,
                bg=CARD_BG,
                fg=TEXT_COLOR,
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                anchor='e'
            ).pack(side=tk.RIGHT)

    def _on_brightness_change(self, value):
        """Handle brightness slider change."""
        brightness = int(float(value))
        self.brightness = brightness
        self.brightness_label.config(text=f"{brightness}%")
        self._apply_brightness(brightness)

    def _set_brightness(self, level):
        """Set brightness to specific level."""
        self.brightness = level
        self.brightness_slider.set(level)
        self.brightness_label.config(text=f"{level}%")
        self._apply_brightness(level)

    def _apply_brightness(self, level):
        """Apply brightness to display."""
        try:
            # Only works on Raspberry Pi with official display
            from utils.platform_detect import is_raspberry_pi

            if not is_raspberry_pi():
                return

            # Map 0-100 to 0-255
            value = int((level / 100.0) * 255)

            # Try to set brightness via system file
            brightness_file = "/sys/class/backlight/rpi_backlight/brightness"
            if os.path.exists(brightness_file):
                try:
                    # This requires sudo access or proper permissions
                    subprocess.run(
                        ["sudo", "bash", "-c", f"echo {value} > {brightness_file}"],
                        check=True,
                        capture_output=True
                    )
                except subprocess.CalledProcessError:
                    # Try without sudo (if permissions are set)
                    with open(brightness_file, 'w') as f:
                        f.write(str(value))
        except Exception as e:
            print(f"Could not set brightness: {e}")

    def _set_scroll_sensitivity(self, level):
        """Set scroll sensitivity and update globally."""
        self.scroll_sensitivity = level

        # Update the global constant
        import config.constants as constants
        constants.SCROLL_SENSITIVITY = level

        # Recreate settings to update button highlights
        self._refresh_settings()

    def _set_interval(self, key, value):
        """Set update interval."""
        if key == 'sensor_display_interval':
            self.sensor_display_interval = value
        elif key == 'sensor_log_interval':
            self.sensor_log_interval = value
        elif key == 'api_update_interval':
            self.api_update_interval = value

        # Recreate settings to update button highlights
        self._refresh_settings()

    def _refresh_settings(self):
        """Refresh the settings display."""
        # Recreate the settings to update button highlights
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Recreate title
        title = tk.Label(
            self.content_frame,
            text="⚙️ SETTINGS",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_LARGE, 'bold')
        )
        title.pack(pady=PADDING * 2)

        # Recreate sections
        self._create_display_settings()
        self._create_scroll_settings()
        self._create_update_settings()
        self._create_system_info()

    def update_display(self):
        """Update display (called when tab is shown)."""
        pass  # Settings are static, no need to update
