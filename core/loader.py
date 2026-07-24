from typing import Callable, Dict

class ModuleRegistry:
    def __init__(self):
        self._calculators: Dict[str, Callable[[], None]] = {}

    def register(self, key: str, handler: Callable[[], None]) -> None:
        self._calculators[key] = handler

    def execute(self, key: str) -> bool:
        if key in self._calculators:
            self._calculators[key]()
            return True
        return False

registry = ModuleRegistry()
