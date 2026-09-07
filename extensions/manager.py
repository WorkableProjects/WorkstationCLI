"""
Extension management and discovery system for Workstation CLI.
"""

from typing import Dict, Any, List, Optional
import importlib
import logging

class Extension:
    """Base class for Workstation extensions."""

    id: str = ""
    name: str = ""
    version: str = "0.0.1"
    description: str = ""

    def __init__(self):
        self.enabled = False

    def initialize(self) -> None:
        """Initialize the extension (register commands, setup hooks)."""
        pass

    def start(self) -> None:
        """Start extension services (e.g. background HTTP server)."""
        pass

    def stop(self) -> None:
        """Stop extension services."""
        pass


class ExtensionManager:
    """Manages discovery, loading, and lifecycle of Workstation CLI extensions."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ExtensionManager, cls).__new__(cls)
            cls._instance.extensions: Dict[str, Extension] = {}
        return cls._instance

    def register_extension(self, extension: Extension) -> None:
        """Register an extension instance."""
        self.extensions[extension.id] = extension

    def get_extension(self, ext_id: str) -> Optional[Extension]:
        """Retrieve an extension by ID."""
        return self.extensions.get(ext_id)

    def load_built_in_extensions(self) -> None:
        """Discover and load standard built-in extensions (like WGI)."""
        try:
            from extensions.wgi.extension import WGIExtension
            wgi_ext = WGIExtension()
            self.register_extension(wgi_ext)
            wgi_ext.initialize()
        except ImportError as e:
            logging.warning(f"Could not load WGI extension: {e}")

    def start_enabled_extensions(self) -> None:
        """Start all extensions that are marked enabled in config."""
        from services.config import load_config
        config = load_config()
        wgi_cfg = config.get("wgi", {})

        for ext_id, ext in self.extensions.items():
            if ext_id == "wgi" and wgi_cfg.get("enabled", False):
                try:
                    ext.start()
                except Exception as e:
                    print(f"Failed to start extension {ext_id}: {e}")

    def stop_all_extensions(self) -> None:
        """Stop all running extensions gracefully."""
        for ext in self.extensions.values():
            try:
                ext.stop()
            except Exception as e:
                pass


extension_manager = ExtensionManager()
