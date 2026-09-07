# v0.0.6.5 — Architecture & Quality (Optional Polish)

## Code Quality & Testing

### 0.0.6.5.a Expand Test Coverage

Focus on areas added or refactored in v0.0.6–v0.0.6.4:

- `tests/test_ai_superprompt.py`: Test superprompt generation and reasoning level logic.
- `tests/test_ui_horizontal_tabs.py`: Test tab navigation state and keyboard handling.
- `tests/test_graphing_multi_series.py`: Multi-series plotting correctness and edge cases.
- `tests/test_graphing_export.py`: Export functionality (if implemented).

### 0.0.6.5.b Refactor Core Menu Infrastructure

Extract common menu patterns into reusable building blocks:

- **MenuConfig**: Data structure for tab/option definitions.
- **MenuHandler**: Base class for routable menus (Chemistry, AI, Graphing, etc.).
- **KeyboardEventDispatcher**: Centralized keyboard input handling (arrows, Enter, Escape).

### 0.0.6.5.c Settings Expansion

Add user-facing controls for new v0.0.7 features:

```
Settings Menu:
  1. AI & Models
     - Model selection
     - Reasoning level default
     - Timeout configuration
  2. UI & Display
     - Theme selection (existing)
     - Tabbed navigation (new)
     - Enable/disable startup animation (new)
     - Terminal width override (for narrow displays)
  3. Graphing Defaults
     - Default X domain (-10 to 10)
     - Default plot width/height
     - Default Y-axis behavior (auto vs manual)
  4. Developer
     - Debug logging
     - Export logs
```

While moving the configuration file within the code somewhere, not in a random location on the OS.
