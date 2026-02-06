"""Platform detection utilities for cross-platform compatibility."""
import platform


def is_raspberry_pi():
    """
    Detect if running on Raspberry Pi.
    Returns True if on Pi, False otherwise (e.g., macOS).
    """
    machine = platform.machine().lower()
    # Raspberry Pi typically returns 'aarch64' or 'armv7l'
    return machine in ['aarch64', 'armv7l', 'armv6l']


def get_platform_name():
    """Return a human-readable platform name."""
    if is_raspberry_pi():
        return "Raspberry Pi"
    return f"{platform.system()} ({platform.machine()})"
