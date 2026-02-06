"""River Conditions tab - Detailed river monitoring."""
import tkinter as tk
from datetime import datetime
from config.constants import *
from ui.components import TouchButton, PaginationControls
from config.rivers import RIVER_STATIONS
import math


class RiverTab(tk.Frame):
    """River conditions tab with paginated river cards."""

    def __init__(self, parent, app_data):
        """Initialize river tab."""
        super().__init__(parent, bg=BG_COLOR)
        self.app_data = app_data
        self.current_page = 0

        # Calculate total pages
        self.total_pages = math.ceil(len(RIVER_STATIONS) / RIVERS_PER_PAGE)

        # Main container
        self.main_frame = tk.Frame(self, bg=BG_COLOR)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Content area (scrollable)
        self.canvas = tk.Canvas(self.main_frame, bg=BG_COLOR, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
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

        # Pagination controls
        self.pagination = PaginationControls(
            self,
            total_pages=self.total_pages,
            on_page_change=self.change_page
        )
        self.pagination.pack(side=tk.BOTTOM, pady=PADDING)

        # Render first page
        self.render_page()

    def render_page(self):
        """Render current page of river cards."""
        # Clear existing cards
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Get rivers for current page
        start_idx = self.current_page * RIVERS_PER_PAGE
        end_idx = min(start_idx + RIVERS_PER_PAGE, len(RIVER_STATIONS))
        page_rivers = RIVER_STATIONS[start_idx:end_idx]

        # Create card for each river
        for river_info in page_rivers:
            self.create_river_card(river_info)

    def create_river_card(self, river_info):
        """Create a card for a single river."""
        name, site_id, has_temp = river_info
        river_data = self.app_data.get('river_data', {})

        # Check if this river is pinned
        pinned_river = self.app_data.get('pinned_river')
        is_pinned = (pinned_river == river_info)

        # Card frame
        card = tk.Frame(
            self.content_frame,
            bg=CARD_BG,
            relief=tk.FLAT,
            borderwidth=2
        )
        card.pack(fill=tk.X, padx=PADDING * 2, pady=PADDING)

        # Header with name and star button
        header_frame = tk.Frame(card, bg=CARD_BG)
        header_frame.pack(fill=tk.X, padx=PADDING, pady=PADDING)

        name_label = tk.Label(
            header_frame,
            text=name.upper(),
            bg=CARD_BG,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold'),
            anchor='w'
        )
        name_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        star_btn = TouchButton(
            header_frame,
            text="★" if is_pinned else "☆",
            command=lambda: self.toggle_pin(river_info),
            width=3,
            font=(FONT_FAMILY, FONT_SIZE_LARGE)
        )
        star_btn.pack(side=tk.RIGHT)

        # Data section
        data_frame = tk.Frame(card, bg=CARD_BG)
        data_frame.pack(fill=tk.BOTH, padx=PADDING, pady=PADDING)

        # Get site data
        site_data = river_data.get(river_info, {})

        if site_data and not site_data.get('error'):
            # Current conditions
            flow_cfs = site_data.get('flow_cfs', 'N/A')
            temp_f = site_data.get('temp_f', 'N/A')
            flow_text = f"{flow_cfs} CFS" if flow_cfs != 'N/A' else "N/A"
            temp_text = f"{temp_f}°F" if temp_f != 'N/A' else "N/A"

            current_label = tk.Label(
                data_frame,
                text=f"Current: {flow_text} • {temp_text}",
                bg=CARD_BG,
                fg=TEXT_COLOR,
                font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
                anchor='w'
            )
            current_label.pack(fill=tk.X)

            # 24hr change
            flow_change = ""
            if site_data.get('flow_cfs') and site_data.get('flow_24h_ago'):
                change = site_data['flow_cfs'] - site_data['flow_24h_ago']
                arrow = "↑" if change > 0 else "↓"
                flow_change = f"{arrow} {abs(change):.0f} CFS"

            temp_change = ""
            if site_data.get('temp_f') and site_data.get('temp_24h_ago'):
                change = site_data['temp_f'] - site_data['temp_24h_ago']
                arrow = "↑" if change > 0 else "↓"
                temp_change = f"{arrow} {abs(change):.1f}°F"

            if flow_change or temp_change:
                change_text = "24hr Change: "
                if flow_change:
                    change_text += flow_change
                if temp_change:
                    if flow_change:
                        change_text += " • "
                    change_text += temp_change

                change_label = tk.Label(
                    data_frame,
                    text=change_text,
                    bg=CARD_BG,
                    fg=TEXT_COLOR,
                    font=(FONT_FAMILY, FONT_SIZE_SMALL),
                    anchor='w'
                )
                change_label.pack(fill=tk.X)

            # Spacer
            tk.Label(data_frame, bg=CARD_BG, height=1).pack()

            # Average comparison (placeholder)
            avg_label = tk.Label(
                data_frame,
                text="Flow: Average data not available\nTemp: Average data not available",
                bg=CARD_BG,
                fg=TEXT_COLOR,
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                anchor='w',
                justify=tk.LEFT
            )
            avg_label.pack(fill=tk.X)

            # Timestamp
            timestamp = site_data.get('timestamp', 'Unknown')
            if timestamp != 'Unknown':
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    timestamp = dt.strftime('%I:%M %p %m/%d')
                except:
                    pass

            cached_text = " ⚠️ (cached)" if site_data.get('cached') else ""
            time_label = tk.Label(
                data_frame,
                text=f"Last Updated: {timestamp}{cached_text}",
                bg=CARD_BG,
                fg=TEXT_COLOR,
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                anchor='w'
            )
            time_label.pack(fill=tk.X, pady=(PADDING, 0))

        else:
            # Error or no data
            error_label = tk.Label(
                data_frame,
                text="⚠️ Data unavailable - check connection",
                bg=CARD_BG,
                fg=ALERT_YELLOW,
                font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
                anchor='w'
            )
            error_label.pack(fill=tk.X)

    def toggle_pin(self, river_info):
        """Toggle pin status for a river."""
        current_pin = self.app_data.get('pinned_river')

        if current_pin == river_info:
            # Unpin
            self.app_data['pinned_river'] = None
        else:
            # Pin this river
            self.app_data['pinned_river'] = river_info

        # Re-render page to update stars
        self.render_page()

    def change_page(self, new_page):
        """Handle page change."""
        self.current_page = new_page
        self.render_page()

    def update_display(self):
        """Update display with latest data."""
        self.render_page()
