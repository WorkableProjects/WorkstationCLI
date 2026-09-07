"""
WGI Extension Implementation.
"""

from extensions.manager import Extension
from extensions.wgi.server import WGIServer
from services.config import load_config

class WGIExtension(Extension):
    id = "wgi"
    name = "Workstation Graphical Interface"
    version = "0.0.1"
    description = "Local browser-based graphical extension for Workstation CLI."

    def __init__(self):
        super().__init__()
        self.server = None

    def initialize(self) -> None:
        """Register WGI commands with the registry."""
        from core.registry import registry

        registry.register(
            command_id="wgi.open",
            name="Open Workstation Graphical Interface",
            category="WGI",
            handler=self.start,
            description="Start and open local WGI browser desktop session.",
            keywords="wgi interface browser gui desktop"
        )

    def start(self) -> None:
        cfg = load_config().get("wgi", {})
        host = cfg.get("host", "127.0.0.1")
        port = cfg.get("port", 8080)
        auto_open = cfg.get("auto_open", True)

        if self.server is None:
            self.server = WGIServer(host=host, port=port)
            self.server.start(auto_open=auto_open)
            self.enabled = True

    def stop(self) -> None:
        if self.server:
            self.server.stop()
            self.server = None
            self.enabled = False
