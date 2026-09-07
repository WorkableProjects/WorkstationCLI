"""
Central Command Registry for Workstation CLI and extensions (WGI).
"""

from typing import List, Dict, Any, Callable, Optional


class CommandRegistry:
    """
    Singleton / Shared command registry for managing commands across CLI and WGI.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CommandRegistry, cls).__new__(cls)
            cls._instance._commands = []
        return cls._instance

    def register(
        self,
        command_id: str,
        name: str,
        category: str,
        handler: Optional[Callable] = None,
        description: str = "",
        keywords: str = "",
        action_type: str = "python"
    ) -> Dict[str, Any]:
        """Register a new command into the shared registry."""
        # Remove existing command with same ID if re-registered
        self.unregister(command_id)

        cmd = {
            "id": command_id,
            "name": name,
            "category": category,
            "description": description or name,
            "keywords": keywords or f"{name} {category}".lower(),
            "handler": handler,
            "action_type": action_type
        }
        self._commands.append(cmd)
        return cmd

    def unregister(self, command_id: str) -> None:
        """Unregister command by ID."""
        self._commands = [c for c in self._commands if c["id"] != command_id]

    def clear(self) -> None:
        """Clear all registered commands."""
        self._commands.clear()

    def get_all(self) -> List[Dict[str, Any]]:
        """Return list of all registered commands."""
        return list(self._commands)

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search commands by query string against name, category, keywords, or description."""
        if not query or not query.strip():
            return self.get_all()

        q = query.strip().lower()
        results = []
        for cmd in self._commands:
            name = cmd["name"].lower()
            cat = cmd["category"].lower()
            kw = cmd.get("keywords", "").lower()
            desc = cmd.get("description", "").lower()
            if q in name or q in cat or q in kw or q in desc:
                results.append(cmd)
        return results


registry = CommandRegistry()
