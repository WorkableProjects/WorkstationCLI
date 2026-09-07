"""Tests for Session Context management."""

from core import history

def test_session_context():
    history.clear_session()

    assert history.get_session_data("last_element") is None

    history.set_session_data("last_element", "Au")
    assert history.get_session_data("last_element") == "Au"

    history.add({"type": "test", "result": "sample"})
    assert history.get_recent(1)["type"] == "test"

    history.clear_session()
    assert history.get_session_data("last_element") is None
    assert history.get_recent(1) is None
