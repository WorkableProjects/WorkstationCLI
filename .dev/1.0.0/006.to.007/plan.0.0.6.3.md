# v0.0.6.3 — UI Navigation Overhaul (Horizontal Tabbed Layout)

## UI/UX Improvements

### 0.0.6.3.a Horizontal Tabbed Navigation

Convert the nested vertical menu system to a **horizontal tab-based layout**.

**Current Flow** (nested menus):
```
Main Menu → Chemistry → Calculator Select → Run
         → AI → Chat/Settings
         → Graphing → Function Select
```

**New Flow** (horizontal tabs):
```
[Chemistry] [AI] [Graphing] [Settings] [About]
    ↓ (Up/Down navigate options within Chemistry)
[Molar Mass] [Gas Laws] [Stoichiometry] [...] [Return]
```

- **Key Navigation**:
  - **Left/Right arrows**: Switch between tabs (Chemistry, AI, Graphing, Settings, About).
  - **Up/Down arrows**: Navigate options within the active tab.
  - **Enter**: Execute selected option.
  - **Escape/q**: Return to main tab view.

- **Architecture Changes**:
  - Extend `core/ui.py` with a `HorizontalTabMenu` class (complementing existing `GridSelector`).
  - Refactor `display_menu()` to support tab mode or maintain two separate entry points.
  - Preserve keyboard accessibility; ensure screen-reader compatibility.

### 0.0.6.3.b Startup Animation

Add a brief **ASCII/Unicode animation** when launching the CLI.

- Display the Workstation CLI banner with a **slide-in**, **fade**, or **type-out** effect.
- Keep animation **< 2 seconds** to avoid annoying long startup times.
- Make animation **toggleable** in settings (enable by default, disable for accessibility/automation).

**Implementation**:
```python
def display_startup_animation():
    """Play ASCII banner animation on startup."""
    # Option 1: Type-out effect (char by char with small delays)
    # Option 2: Slide-in effect (reveal from top)
    # Option 3: Color-pulse effect (gradually colorize banner)
```
