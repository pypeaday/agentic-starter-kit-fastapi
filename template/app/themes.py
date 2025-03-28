"""Theme management for the book tracking app."""
from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class ThemeColors:
    """Represents the colors used in a theme."""
    bg: str  # Main background
    bg1: str  # Secondary background
    bg2: str  # Tertiary background
    fg: str  # Main text
    fg1: str  # Secondary text
    accent: str  # Primary accent color
    accent_hover: str  # Hover state for accent
    success: str  # Success/positive color
    error: str  # Error/negative color

# Built-in themes
THEMES: Dict[str, ThemeColors] = {
    "gruvbox-dark": ThemeColors(
        bg="#282828",  # Background
        bg1="#3c3836",  # Secondary Background
        bg2="#504945",  # Tertiary Background
        fg="#ebdbb2",  # Text
        fg1="#d5c4a1",  # Secondary Text
        accent="#83a598",  # Blue for links/buttons
        accent_hover="#8ec07c",  # Aqua for hover states
        success="#b8bb26",  # Green
        error="#fb4934"  # Red
    ),
    "light": ThemeColors(
        bg="#ffffff",
        bg1="#f3f4f6",
        bg2="#e5e7eb",
        fg="#111827",
        fg1="#4b5563",
        accent="#3b82f6",
        accent_hover="#2563eb",
        success="#10b981",
        error="#ef4444"
    ),
    "nord": ThemeColors(
        bg="#2e3440",  # Polar Night
        bg1="#3b4252",
        bg2="#434c5e",
        fg="#eceff4",  # Snow Storm
        fg1="#d8dee9",
        accent="#88c0d0",  # Frost
        accent_hover="#81a1c1",
        success="#a3be8c",  # Aurora
        error="#bf616a"
    ),
    "dracula": ThemeColors(
        bg="#282a36",  # Background
        bg1="#44475a",  # Current Line
        bg2="#6272a4",  # Selection
        fg="#f8f8f2",  # Foreground
        fg1="#bfbfbf",
        accent="#bd93f9",  # Purple
        accent_hover="#ff79c6",  # Pink
        success="#50fa7b",  # Green
        error="#ff5555"  # Red
    ),
    "solarized-dark": ThemeColors(
        bg="#002b36",  # Base03
        bg1="#073642",  # Base02
        bg2="#586e75",  # Base01
        fg="#fdf6e3",  # Base3
        fg1="#eee8d5",  # Base2
        accent="#268bd2",  # Blue
        accent_hover="#2aa198",  # Cyan
        success="#859900",  # Green
        error="#dc322f"  # Red
    ),
    "solarized-light": ThemeColors(
        bg="#fdf6e3",  # Base3
        bg1="#eee8d5",  # Base2
        bg2="#93a1a1",  # Base1
        fg="#002b36",  # Base03
        fg1="#073642",  # Base02
        accent="#268bd2",  # Blue
        accent_hover="#2aa198",  # Cyan
        success="#859900",  # Green
        error="#dc322f"  # Red
    )
}

def get_theme(name: str) -> Optional[ThemeColors]:
    """Get a theme by name."""
    return THEMES.get(name)
