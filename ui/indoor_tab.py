"""Indoor Air Quality tab - Environmental sensors display."""
import tkinter as tk
from datetime import datetime
from config.constants import *
from ui.components import TouchButton
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class IndoorTab(tk.Frame):
    """Indoor air quality tab with current readings and graphs."""

    def __init__(self, parent, app_data, database):
        """Initialize indoor tab."""
        super().__init__(parent, bg=BG_COLOR)
        self.app_data = app_data
        self.database = database
        self.show_graphs = False
        self.selected_metric = 'temperature'
        self.selected_hours = 24

        # Main view (current readings)
        self.main_view = tk.Frame(self, bg=BG_COLOR)
        self.main_view.pack(fill=tk.BOTH, expand=True)

        self.create_main_view()

    def create_main_view(self):
        """Create main view with current readings."""
        for widget in self.main_view.winfo_children():
            widget.destroy()

        # Title
        title = tk.Label(
            self.main_view,
            text="INDOOR AIR QUALITY",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_LARGE, 'bold')
        )
        title.pack(pady=PADDING * 2)

        # Readings frame
        readings_frame = tk.Frame(self.main_view, bg=BG_COLOR)
        readings_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING * 4)

        sensor_data = self.app_data.get('sensor_data', {})

        # Temperature
        self.create_reading_display(
            readings_frame,
            "Temperature:",
            f"{sensor_data.get('temperature', 'N/A')}°F"
        )

        # Humidity
        self.create_reading_display(
            readings_frame,
            "Humidity:",
            f"{sensor_data.get('humidity', 'N/A')}%"
        )

        # Pressure
        pressure = sensor_data.get('pressure', 'N/A')
        self.create_reading_display(
            readings_frame,
            "Pressure:",
            f"{pressure} inHg" if pressure != 'N/A' else 'N/A'
        )

        # Air Quality
        pm25 = sensor_data.get('pm25', 0)
        if isinstance(pm25, (int, float)):
            if pm25 <= 12:
                status = "Good"
                color = GOOD_GREEN
            elif pm25 <= 35:
                status = "Moderate"
                color = ALERT_YELLOW
            elif pm25 <= 55:
                status = "Unhealthy for Sensitive"
                color = ALERT_ORANGE
            elif pm25 <= 150:
                status = "Unhealthy"
                color = ALERT_RED
            else:
                status = "Very Unhealthy"
                color = "#8b0000"
        else:
            status = "N/A"
            color = TEXT_COLOR

        quality_frame = tk.Frame(readings_frame, bg=BG_COLOR)
        quality_frame.pack(fill=tk.X, pady=PADDING)

        quality_label = tk.Label(
            quality_frame,
            text="Air Quality:",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold'),
            anchor='w'
        )
        quality_label.pack(side=tk.LEFT)

        quality_value = tk.Label(
            quality_frame,
            text=status,
            bg=BG_COLOR,
            fg=color,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            anchor='e'
        )
        quality_value.pack(side=tk.RIGHT)

        # PM2.5
        self.create_reading_display(
            readings_frame,
            "PM2.5:",
            f"{pm25} µg/m³ ({status})" if pm25 != 'N/A' else 'N/A',
            value_color=color
        )

        # View Graphs button
        graph_btn = TouchButton(
            self.main_view,
            text="View Graphs",
            command=self.show_graph_view,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold'),
            height=2
        )
        graph_btn.pack(pady=PADDING * 2)

        # Last updated
        last_updated = tk.Label(
            self.main_view,
            text=f"Last Updated: {datetime.now().strftime('%I:%M:%S %p')}",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_SMALL)
        )
        last_updated.pack(pady=PADDING)

    def create_reading_display(self, parent, label_text, value_text, value_color=None):
        """Create a reading display row."""
        frame = tk.Frame(parent, bg=BG_COLOR)
        frame.pack(fill=tk.X, pady=PADDING)

        label = tk.Label(
            frame,
            text=label_text,
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold'),
            anchor='w'
        )
        label.pack(side=tk.LEFT)

        value = tk.Label(
            frame,
            text=value_text,
            bg=BG_COLOR,
            fg=value_color or TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            anchor='e'
        )
        value.pack(side=tk.RIGHT)

    def show_graph_view(self):
        """Switch to graph view."""
        self.show_graphs = True
        self.main_view.pack_forget()

        # Create graph view
        self.graph_view = tk.Frame(self, bg=BG_COLOR)
        self.graph_view.pack(fill=tk.BOTH, expand=True)

        # Sidebar for metric selection
        sidebar = tk.Frame(self.graph_view, bg=BUTTON_BG, width=150)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        metrics = [
            ('temperature', 'Temperature'),
            ('humidity', 'Humidity'),
            ('pressure', 'Pressure'),
            ('gas_resistance', 'Air Quality'),
            ('pm25', 'PM2.5')
        ]

        for metric_key, metric_label in metrics:
            btn = TouchButton(
                sidebar,
                text=metric_label + (" ◄──" if metric_key == self.selected_metric else ""),
                command=lambda m=metric_key: self.select_metric(m),
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                anchor='w'
            )
            btn.pack(fill=tk.X, padx=5, pady=2)

        # Graph area
        graph_area = tk.Frame(self.graph_view, bg=BG_COLOR)
        graph_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Title
        self.graph_title = tk.Label(
            graph_area,
            text=f"{self.get_metric_label(self.selected_metric)} - Last {self.selected_hours} Hours",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_LARGE, 'bold')
        )
        self.graph_title.pack(pady=PADDING)

        # Graph canvas
        self.graph_canvas_frame = tk.Frame(graph_area, bg=BG_COLOR)
        self.graph_canvas_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING, pady=PADDING)

        # Time range buttons
        time_frame = tk.Frame(graph_area, bg=BG_COLOR)
        time_frame.pack(pady=PADDING)

        tk.Label(
            time_frame,
            text="Time Range:",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_SMALL)
        ).pack(side=tk.LEFT, padx=5)

        for hours in [24, 48, 72]:
            btn = TouchButton(
                time_frame,
                text=f"{hours}hr",
                command=lambda h=hours: self.select_time_range(h),
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                bg=ACCENT_COLOR if hours == self.selected_hours else BUTTON_BG
            )
            btn.pack(side=tk.LEFT, padx=2)

        # Back button
        back_btn = TouchButton(
            graph_area,
            text="Back to Current View",
            command=self.show_main_view,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM)
        )
        back_btn.pack(pady=PADDING)

        # Draw initial graph
        self.draw_graph()

    def show_main_view(self):
        """Switch back to main view."""
        self.show_graphs = False
        if hasattr(self, 'graph_view'):
            self.graph_view.destroy()
        self.main_view.pack(fill=tk.BOTH, expand=True)
        self.create_main_view()

    def select_metric(self, metric_key):
        """Select metric to display in graph."""
        self.selected_metric = metric_key
        if hasattr(self, 'graph_view'):
            self.show_graph_view()

    def select_time_range(self, hours):
        """Select time range for graph."""
        self.selected_hours = hours
        self.graph_title.config(text=f"{self.get_metric_label(self.selected_metric)} - Last {hours} Hours")
        self.draw_graph()

    def get_metric_label(self, metric_key):
        """Get display label for metric."""
        labels = {
            'temperature': 'Temperature',
            'humidity': 'Humidity',
            'pressure': 'Pressure',
            'gas_resistance': 'Air Quality',
            'pm25': 'PM2.5'
        }
        return labels.get(metric_key, metric_key)

    def draw_graph(self):
        """Draw graph for selected metric."""
        # Clear existing graph
        for widget in self.graph_canvas_frame.winfo_children():
            widget.destroy()

        # Get data from database
        readings = self.database.get_readings(hours=self.selected_hours)

        if not readings:
            no_data = tk.Label(
                self.graph_canvas_frame,
                text="No data available yet",
                bg=BG_COLOR,
                fg=TEXT_COLOR,
                font=(FONT_FAMILY, FONT_SIZE_LARGE)
            )
            no_data.pack(expand=True)
            return

        # Parse data
        timestamps = []
        values = []

        metric_index = {
            'temperature': 1,
            'humidity': 2,
            'pressure': 3,
            'gas_resistance': 4,
            'pm25': 6
        }

        idx = metric_index.get(self.selected_metric, 1)

        for reading in readings:
            try:
                timestamps.append(datetime.fromisoformat(reading[0]))
                values.append(reading[idx])
            except:
                continue

        if not values:
            no_data = tk.Label(
                self.graph_canvas_frame,
                text="No data available",
                bg=BG_COLOR,
                fg=TEXT_COLOR,
                font=(FONT_FAMILY, FONT_SIZE_LARGE)
            )
            no_data.pack(expand=True)
            return

        # Create matplotlib figure
        fig = Figure(figsize=(6, 4), facecolor='#1a1a1a')
        ax = fig.add_subplot(111)

        ax.plot(timestamps, values, color='#4a9eff', linewidth=2)
        ax.set_facecolor('#1a1a1a')
        ax.spines['bottom'].set_color('#ffffff')
        ax.spines['left'].set_color('#ffffff')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(colors='#ffffff')
        ax.xaxis.label.set_color('#ffffff')
        ax.yaxis.label.set_color('#ffffff')

        # Labels
        ax.set_xlabel('Time', color='#ffffff')

        unit_labels = {
            'temperature': '°F',
            'humidity': '%',
            'pressure': 'inHg',
            'gas_resistance': 'Ohms',
            'pm25': 'µg/m³'
        }
        ax.set_ylabel(f"{self.get_metric_label(self.selected_metric)} ({unit_labels.get(self.selected_metric, '')})",
                     color='#ffffff')

        fig.autofmt_xdate()
        fig.tight_layout()

        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, self.graph_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_display(self):
        """Update display with latest data."""
        if self.show_graphs:
            self.draw_graph()
        else:
            self.create_main_view()
