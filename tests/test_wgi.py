"""
Unit tests for Workstation Graphical Interface (WGI) extension & HTTP backend.
"""

import json
import urllib.request
import urllib.parse
import pytest
from pathlib import Path

from core.banner import VERSION, WGI_VERSION
from core.registry import registry
from extensions.manager import extension_manager
from extensions.wgi.server import WGIServer


@pytest.fixture(scope="module")
def wgi_test_server():
    """Start a temporary WGIServer instance for testing API endpoints."""
    server = WGIServer(host="127.0.0.1", port=0)
    server.start(auto_open=False)
    yield server
    server.stop()


def test_command_registry():
    """Test registering, searching, and unregistering commands."""
    registry.register(
        command_id="test.calc",
        name="Test Calculator",
        category="Chemistry",
        description="A test calculator",
        keywords="test calc chemistry"
    )

    cmds = registry.search("Test Calculator")
    assert len(cmds) >= 1
    assert any(c["id"] == "test.calc" for c in cmds)

    registry.unregister("test.calc")
    cmds_after = registry.search("Test Calculator")
    assert not any(c["id"] == "test.calc" for c in cmds_after)


def test_extension_manager():
    """Test loading built-in extensions via ExtensionManager."""
    extension_manager.load_built_in_extensions()
    wgi_ext = extension_manager.get_extension("wgi")
    assert wgi_ext is not None
    assert wgi_ext.id == "wgi"
    assert wgi_ext.version == "0.0.1"


def test_wgi_api_status(wgi_test_server):
    """Test /api/status endpoint response."""
    url = f"http://{wgi_test_server.host}:{wgi_test_server.port}/api/status"
    req = urllib.request.urlopen(url)
    data = json.loads(req.read().decode("utf-8"))

    assert data["status"] == "ok"
    assert data["cli_version"] == VERSION
    assert data["wgi_version"] == WGI_VERSION


def test_wgi_api_files(wgi_test_server):
    """Test /api/files endpoint filtering."""
    url = f"http://{wgi_test_server.host}:{wgi_test_server.port}/api/files"
    req = urllib.request.urlopen(url)
    data = json.loads(req.read().decode("utf-8"))

    assert "files" in data
    assert isinstance(data["files"], list)
    # Ensure only .md and .py files are included
    for f in data["files"]:
        assert f["extension"] in (".md", ".py")


def test_wgi_api_file_content_markdown(wgi_test_server):
    """Test reading Markdown file content via /api/file-content."""
    url = f"http://{wgi_test_server.host}:{wgi_test_server.port}/api/file-content?path=README.md"
    req = urllib.request.urlopen(url)
    data = json.loads(req.read().decode("utf-8"))

    assert "content" in data
    assert "Workstation CLI" in data["content"]


def test_wgi_api_file_content_python_forbidden(wgi_test_server):
    """Test python source view protection returning HTTP 403."""
    url = f"http://{wgi_test_server.host}:{wgi_test_server.port}/api/file-content?path=workstation.py"
    try:
        urllib.request.urlopen(url)
        assert False, "Should have raised HTTPError 403"
    except urllib.error.HTTPError as e:
        assert e.code == 403


def test_wgi_api_terminal_lifecycle(wgi_test_server):
    """Test terminal session creation, input writing, and closing."""
    base_url = f"http://{wgi_test_server.host}:{wgi_test_server.port}"

    # 1. Create terminal session
    create_req = urllib.request.Request(
        f"{base_url}/api/terminal/create",
        data=json.dumps({"command": "echo Hello_WGI"}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    res = urllib.request.urlopen(create_req)
    data = json.loads(res.read().decode("utf-8"))
    term_id = data.get("id")
    assert term_id is not None

    # 2. Close terminal session
    close_req = urllib.request.Request(
        f"{base_url}/api/terminal/close",
        data=json.dumps({"id": term_id}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    close_res = urllib.request.urlopen(close_req)
    close_data = json.loads(close_res.read().decode("utf-8"))
    assert close_data.get("status") == "closed"
