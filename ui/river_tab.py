"""River conditions tab with regional filtering."""
import tkinter as tk
from config.constants import *
from config.rivers import RIVER_STATIONS, REGIONS, get_rivers_by_region
from ui.components import TouchButton


class RiverTab(tk.Frame):
    """River conditions tab with regional sidebar and compact display."""

    def __init__(self, parent, app_data):
        """Initialize river tab with regional filtering."""
        super().__init__(parent, bg=BG_COLOR)
        self.app_data = app_data
        self.selected_region = 'All'

        # Main layout: sidebar + content
        self.create_ui()

    def create_ui(self):
        """Create UI with sidebar and river list."""
        # SIDEBAR - Region selection (left side)
        sidebar = tk.Frame(self, bg=BUTTON_BG, width=140)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        # Sidebar title
        sidebar_title = tk.Label(
            sidebar,
            text="REGIONS",
            bg=BUTTON_BG,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_SMALL, 'bold')
        )
        sidebar_title.pack(pady=PADDING)

        # Region buttons
        self.region_buttons = {}
        regions_list = ['All', 'Flathead', 'Missoula', 'Northwest', 'Missouri']

        for region in regions_list:
            is_selected = (region == self.selected_region)
            btn = TouchButton(
                sidebar,
                text=region + (" ✓" if is_selected else ""),
                command=lambda r=region: self.select_region(r),
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                bg=ACCENT_COLOR if is_selected else BUTTON_BG,
                anchor='w'
            )
            btn.pack(fill=tk.X, padx=5, pady=2)
            self.region_buttons[region] = btn

        # CONTENT AREA - River list (right side)
        content_area = tk.Frame(self, bg=BG_COLOR)
        content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Title
        title_frame = tk.Frame(content_area, bg=BG_COLOR)
        title_frame.pack(fill=tk.X, pady=PADDING)

        self.title_label = tk.Label(
            title_frame,
            text="RIVER CONDITIONS - All Regions",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold')
        )
        self.title_label.pack(side=tk.LEFT, padx=PADDING)

        # Scrollable river list
        self.canvas = tk.Canvas(content_area, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.river_frame = tk.Frame(self.canvas, bg=BG_COLOR)
        self.canvas.create_window((0, 0), window=self.river_frame, anchor="nw")

        # Enable touch scrolling
        from ui.components import enable_touch_scroll
        enable_touch_scroll(self.canvas, sensitivity=SCROLL_SENSITIVITY)

        # Configure canvas scrolling
        self.river_frame.bind('<Configure>',
                             lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        # Initial display
        self.update_display()

    def select_region(self, region):
        """Select a region and filter rivers."""
        self.selected_region = region

        # Update button highlights
        for r, btn in self.region_buttons.items():
            is_selected = (r == region)
            btn.config(
                text=r + (" ✓" if is_selected else ""),
                bg=ACCENT_COLOR if is_selected else BUTTON_BG
            )

        # Update title
        self.title_label.config(text=f"RIVER CONDITIONS - {region}")

        # Refresh river list
        self.update_display()

    def update_display(self):
        """Update river list based on selected region."""
        # Clear existing river cards
        for widget in self.river_frame.winfo_children():
            widget.destroy()

        # Get rivers for selected region
        rivers = get_rivers_by_region(self.selected_region)
        river_data = self.app_data.get('river_data', {})

        if not rivers:
            no_data = tk.Label(
                self.river_frame,
                text=f"No rivers in {self.selected_region} region",
                bg=BG_COLOR,
                fg=TEXT_MUTED,
                font=(FONT_FAMILY, FONT_SIZE_MEDIUM)
            )
            no_data.pack(pady=PADDING * 4)
            return

        # Create compact river cards
        for river_info in rivers:
            self.create_river_card(river_info, river_data)

    def create_river_card(self, river_info, river_data):
        """Create a compact river card."""
        name, site_id, has_temp = river_info

        # Card container - more compact
        card = tk.Frame(
            self.river_frame,
            bg=CARD_BG,
            relief=tk.FLAT,
            borderwidth=0
        )
        card.pack(fill=tk.X, padx=PADDING, pady=PADDING // 2)

        # Get data
        data = river_data.get(river_info, {})

        # Check if this is the pinned river
        pinned_river = self.app_data.get('pinned_river')
        is_pinned = (pinned_river == river_info)

        # Top row: Name + Pin button
        top_row = tk.Frame(card, bg=CARD_BG)
        top_row.pack(fill=tk.X, padx=PADDING // 2, pady=PADDING // 2)

        # River name - SMALLER FONT
        name_label = tk.Label(
            top_row,
            text=f"{'★ ' if is_pinned else ''}{name}",
            bg=CARD_BG,
            fg=ACCENT_COLOR if is_pinned else TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_SMALL, 'bold'),
            anchor='w'
        )
        name_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Pin button - SMALLER
        pin_btn = TouchButton(
            top_row,
            text="★" if is_pinned else "☆",
            command=lambda: self.toggle_pin(river_info),
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            width=3,
            bg=ACCENT_COLOR if is_pinned else BUTTON_BG
        )
        pin_btn.pack(side=tk.RIGHT)

        # Data row - COMPACT horizontal layout
        if data:
            data_row = tk.Frame(card, bg=CARD_BG)
            data_row.pack(fill=tk.X, padx=PADDING // 2, pady=(0, PADDING // 2))

            # Flow
            flow_cfs = data.get('flow_cfs')
            if flow_cfs:
                flow_text = f"💧 {flow_cfs:,.0f} CFS"
                flow_color = TEXT_COLOR

                # Flow change
                if data.get('flow_24h_ago'):
                    change = flow_cfs - data['flow_24h_ago']
                    if change > 0:
                        flow_text += f" ↑{abs(change):,.0f}"
                        flow_color = RIVER_HIGH
                    elif change < 0:
                        flow_text += f" ↓{abs(change):,.0f}"
                        flow_color = RIVER_LOW

                tk.Label(
                    data_row,
                    text=flow_text,
                    bg=CARD_BG,
                    fg=flow_color,
                    font=(FONT_FAMILY, FONT_SIZE_SMALL),
                    anchor='w'
                ).pack(side=tk.LEFT, padx=(0, PADDING))

            # Temperature
            temp_f = data.get('temp_f')
            if temp_f and temp_f > -100:
                temp_text = f"🌡️ {temp_f:.1f}°F"
                temp_color = TEXT_COLOR

                # Temp change
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
                    data_row,
                    text=temp_text,
                    bg=CARD_BG,
                    fg=temp_color,
                    font=(FONT_FAMILY, FONT_SIZE_SMALL),
                    anchor='w'
                ).pack(side=tk.LEFT)
        else:
            # No data available
            tk.Label(
                card,
                text="No data available",
                bg=CARD_BG,
                fg=TEXT_MUTED,
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                anchor='w'
            ).pack(padx=PADDING // 2, pady=PADDING // 2)

    def toggle_pin(self, river_info):
        """Toggle pin status for a river."""
        current_pin = self.app_data.get('pinned_river')

        if current_pin == river_info:
            # Unpin
            self.app_data['pinned_river'] = None
        else:
            # Pin this river
            self.app_data['pinned_river'] = river_info

        # Refresh display
        self.update_display()
