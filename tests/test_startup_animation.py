"""Unit tests for startup animation and banner in core.banner."""

from core.banner import VERSION, display_banner, display_startup_animation


def test_banner_version():
    """Verify banner version is updated to 0.0.6.3."""
    assert VERSION == "0.0.6.3"


def test_display_banner(capsys):
    """Verify display_banner prints expected version and organization info."""
    display_banner(animated=False)
    captured = capsys.readouterr()
    assert "Version: 0.0.6.3" in captured.out
    assert "Made by Workable Projects" in captured.out


def test_display_startup_animation(capsys):
    """Verify display_startup_animation runs without errors."""
    display_startup_animation()
    captured = capsys.readouterr()
    assert "Version: 0.0.6.3" in captured.out
