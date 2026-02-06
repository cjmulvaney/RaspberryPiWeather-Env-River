"""Reusable UI components."""
import tkinter as tk
from tkinter import ttk
from config.constants import *


class TouchButton(tk.Button):
    """Button optimized for touch interaction with visual feedback."""

    def __init__(self, parent, text="", command=None, **kwargs):
        """Create touch-optimized button."""
        # Set default styling
        default_config = {
            'text': text,
            'command': command,
            'bg': BUTTON_BG,
            'fg': TEXT_COLOR,
            'font': (FONT_FAMILY, FONT_SIZE_MEDIUM),
            'relief': tk.FLAT,
            'borderwidth': 0,
            'cursor': 'hand2',
            'activebackground': BUTTON_HOVER,
            'activeforeground': TEXT_COLOR,
        }
        default_config.update(kwargs)

        super().__init__(parent, **default_config)

        # Bind touch feedback
        self.bind('<Button-1>', self._on_press)
        self.bind('<ButtonRelease-1>', self._on_release)

    def _on_press(self, event):
        """Visual feedback on press."""
        self.config(bg=ACCENT_COLOR)
        self.after(200, lambda: self.config(bg=BUTTON_BG))

    def _on_release(self, event):
        """Reset on release."""
        pass


class ScrollableFrame(tk.Frame):
    """Frame with vertical scrollbar for touch scrolling."""

    def __init__(self, parent, **kwargs):
        """Create scrollable frame."""
        super().__init__(parent, bg=BG_COLOR, **kwargs)

        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self, bg=BG_COLOR, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=BG_COLOR)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack elements
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Enable mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling."""
        if event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")


class Card(tk.Frame):
    """Card-style container for displaying data."""

    def __init__(self, parent, **kwargs):
        """Create card container."""
        super().__init__(
            parent,
            bg=BUTTON_BG,
            relief=tk.FLAT,
            borderwidth=1,
            **kwargs
        )
        self.pack(fill=tk.X, padx=PADDING, pady=PADDING)


class PaginationControls(tk.Frame):
    """Pagination controls for navigating pages."""

    def __init__(self, parent, total_pages, on_page_change, **kwargs):
        """Create pagination controls."""
        super().__init__(parent, bg=BG_COLOR, **kwargs)

        self.total_pages = total_pages
        self.current_page = 0
        self.on_page_change = on_page_change

        # Previous button
        self.prev_btn = TouchButton(
            self,
            text="< Prev",
            command=self.prev_page,
            width=10
        )
        self.prev_btn.pack(side=tk.LEFT, padx=5)

        # Page indicator
        self.page_label = tk.Label(
            self,
            text=self._get_page_text(),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM)
        )
        self.page_label.pack(side=tk.LEFT, padx=20)

        # Next button
        self.next_btn = TouchButton(
            self,
            text="Next >",
            command=self.next_page,
            width=10
        )
        self.next_btn.pack(side=tk.LEFT, padx=5)

        self.update_buttons()

    def _get_page_text(self):
        """Get page indicator text."""
        return f"Page {self.current_page + 1} of {self.total_pages}"

    def prev_page(self):
        """Go to previous page."""
        if self.current_page > 0:
            self.current_page -= 1
            self.update_buttons()
            self.on_page_change(self.current_page)

    def next_page(self):
        """Go to next page."""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.update_buttons()
            self.on_page_change(self.current_page)

    def update_buttons(self):
        """Update button states and page label."""
        self.page_label.config(text=self._get_page_text())
        self.prev_btn.config(state=tk.NORMAL if self.current_page > 0 else tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL if self.current_page < self.total_pages - 1 else tk.DISABLED)

    def set_page(self, page: int):
        """Set current page programmatically."""
        if 0 <= page < self.total_pages:
            self.current_page = page
            self.update_buttons()
