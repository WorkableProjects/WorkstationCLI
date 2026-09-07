import sys
import time

VERSION = "1.0.0"
ORGANIZATION = "Workable Projects"
AUTHOR = "Dutchh"

BANNER_TEXT = r"""
██╗    ██╗  ██████╗  ██████╗  ██╗  ██╗ ███████╗ ████████╗  █████╗  ████████╗ ██╗  ██████╗  ███╗   ██╗
██║    ██║ ██╔═══██╗ ██╔══██╗ ██║ ██╔╝ ██╔════╝ ╚══██╔══╝ ██╔══██╗ ╚══██╔══╝ ██║ ██╔═══██╗ ████╗  ██║
██║ █╗ ██║ ██║   ██║ ██████╔╝ █████╔╝  ███████╗    ██║    ███████║    ██║    ██║ ██║   ██║ ██╔██╗ ██║
██║███╗██║ ██║   ██║ ██╔══██╗ ██╔═██╗  ╚════██║    ██║    ██╔══██║    ██║    ██║ ██║   ██║ ██║╚██╗██║
╚███╔███╔╝ ╚██████╔╝ ██║  ██╗ ██║  ██╗ ███████║    ██║    ██║  ██║    ██║    ██║ ╚██████╔╝ ██║ ╚████║
 ╚══╝╚══╝   ╚═════╝  ╚═╝  ╚═╝ ╚═╝  ╚═╝ ╚══════╝    ╚═╝    ╚═╝  ╚═╝    ╚═╝    ╚═╝  ╚═════╝  ╚═╝  ╚═══╝

 ██████╗██╗     ██╗
██╔════╝██║     ██║
██║     ██║     ██║
██║     ██║     ██║
╚██████╗███████╗██║
 ╚═════╝╚══════╝╚═╝
"""


def display_banner(animated: bool = False) -> None:
    """Display banner text and CLI information.

    If animated is True (and startup_animation setting is enabled), play a brief slide-in effect.
    """
    from services.config import load_config
    config = load_config()
    should_animate = animated and config.get("appearance", {}).get("startup_animation", True)

    lines = BANNER_TEXT.strip("\n").split("\n")
    if should_animate:
        for line in lines:
            print(line)
            sys.stdout.flush()
            time.sleep(0.02)
    else:
        print(BANNER_TEXT)

    print("Version: R1")
    print(f"Made by {ORGANIZATION}")
    print("-" * 50)


def display_startup_animation() -> None:
    """Play brief ASCII banner animation on startup."""
    display_banner(animated=True)
