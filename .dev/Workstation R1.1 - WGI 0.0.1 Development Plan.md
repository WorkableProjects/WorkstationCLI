# Workstation R1.1 — WGI 0.0.1
## Release 1.1.0 / Workstation Graphical Interface 0.0.1

**Project:** Workstation CLI  
**Repository:** WorkableProjects/WorkstationCLI  
**CLI Release:** R1.1 / v1.1.0  
**Extension:** Workstation Graphical Interface (WGI) v0.0.1  
**Codename:** WGI / Local Desktop  
**Status:** Development Plan

---

# 0. Overview

R1.1 introduces the first graphical extension for Workstation CLI.

The core product remains **Workstation CLI**. The graphical interface is an **optional extension** that can be enabled through Workstation settings.

When enabled, Workstation can start a small local web server. The user can then access WGI through a browser using a localhost address.

The goal is **not** to recreate a complete IDE, operating system, or online development platform.

The goal is to create a **small, usable browser-based workstation interface** for interacting with a Workstation project.

### Core Concept

```text
                    WORKSTATION
                         │
             ┌───────────┴───────────┐
             │                       │
       Workstation CLI              WGI
          v1.1.0                    v0.0.1
             │                       │
       Terminal Interface       Local Web Interface
                                     │
                              Browser / localhost
```

WGI should reuse Workstation's existing functionality wherever possible rather than creating duplicate implementations.

---

# 1. R1.1 Goals

R1.1 has two related goals:

### Workstation CLI v1.1.0

Improve the CLI architecture to support extensions and provide the infrastructure required by WGI.

### WGI v0.0.1

Create the first usable graphical interface capable of:

- Browsing a Workstation project.
- Viewing supported documentation.
- Launching Python scripts.
- Running multiple terminals.
- Accessing Workstation functionality.
- Using the existing Command Palette.
- Managing WGI configuration.
- Running entirely locally.

---

# 2. Extension Architecture

WGI must be treated as an **extension/plugin**, not as a replacement for the CLI.

The CLI must remain usable without WGI.

### Required behavior

```text
Workstation
│
├── CLI
│   ├── Chemistry
│   ├── AI
│   ├── Graphing
│   ├── Settings
│   └── Command Palette
│
└── Extensions
    └── WGI
        ├── Local Web Server
        ├── Browser UI
        ├── File Explorer
        ├── Documentation Viewer
        ├── Terminal Windows
        └── Command Palette Integration
```

WGI should only load when enabled.

If WGI is disabled:

- Workstation behaves normally.
- No web server is started.
- No browser interface is required.
- No WGI-specific dependencies should interfere with normal CLI operation.

---

# 3. WGI Enable/Disable Setting

Add a setting for enabling WGI.

Example:

```text
Settings
│
├── AI & Models
├── UI & Display
├── Graphing
├── Extensions
│   └── Workstation Graphical Interface
│       ├── Enabled: Yes/No
│       ├── Host: 127.0.0.1
│       ├── Port: Auto
│       └── Open browser automatically: Yes/No
└── Developer
```

### Important

WGI should be disabled by default unless the existing Workstation extension architecture makes enabling it by default appropriate.

The setting must persist through Workstation's existing configuration system.

Do not introduce a separate unrelated configuration system.

---

# 4. Local Web Server

When WGI is enabled, Workstation should be capable of starting a local HTTP server.

Example:

```text
http://127.0.0.1:<port>
```

or:

```text
http://localhost:<port>
```

### Requirements

- Localhost only by default.
- Do not expose WGI to the public network by default.
- Automatically select an available port when the configured port is unavailable.
- Clearly display the active address.
- Provide a clean shutdown mechanism.
- Avoid blocking the normal CLI process unnecessarily.
- WGI must not require an internet connection.

Example CLI output:

```text
WGI enabled
Workstation Graphical Interface started.

Local address:
http://127.0.0.1:PORT

Press Ctrl+C to stop Workstation.
```

---

# 5. WGI User Interface

WGI should resemble a lightweight desktop environment inside the browser.

It should **not** attempt to reproduce Windows, macOS, GNOME, or another operating system exactly.

The design should instead use familiar desktop concepts:

- Sidebar
- Windows
- Applications
- Search
- Terminal
- File browser

---

# 6. Main Layout

The primary WGI layout should consist of:

```text
┌──────────────────────────────────────────────────────────────┐
│ [Workstation Logo]                         [Search / Palette] │
├───────────────┬──────────────────────────────────────────────┤
│               │                                              │
│ PROJECT       │                                              │
│               │                 Desktop                      │
│ ▼ project     │                                              │
│   ▼ docs      │                                              │
│     README.md │                                              │
│   ▼ src       │                                              │
│     tool.py   │                                              │
│     app.py    │                                              │
│               │                                              │
│               │                                              │
│               │                                              │
└───────────────┴──────────────────────────────────────────────┘
```

The interface should feel like a **local workstation**, rather than a conventional website.

---

# 7. Workstation Logo

The Workstation logo remains visible in the upper-left corner.

Requirements:

- No surrounding background panel.
- Logo should remain visually clean.
- Scale responsively.
- Preserve aspect ratio.
- Do not distort the logo.
- Styling and sizing should be easy to refine later.

The logo should act as WGI's primary visual identity.

Do not redesign the logo as part of R1.1 unless required for technical rendering.

---

# 8. Project File Explorer

The left sidebar contains a project file tree.

Example:

```text
PROJECT

▼ WorkstationCLI
  ▼ .dev
    README.md
    plan.1.1.md
  ▼ core
    ui.py
    config.py
  ▼ services
    ollama.py
  ▼ docs
    architecture.md
  README.md
  workstation.py
```

### File visibility

WGI should only expose selected file types.

Initially display:

- Markdown files
- Documentation files
- Python scripts

Examples:

```text
.md
.py
```

Other files should remain hidden from the WGI file explorer unless explicitly supported later.

Do not attempt to render arbitrary binary files.

---

# 9. Markdown / Documentation Viewer

Markdown files should be rendered as Markdown rather than displayed as raw source.

Example:

```text
README.md
```

opens as:

```text
# Workstation CLI

Workstation is an offline chemistry...

## Features

...
```

The viewer should support the Markdown features already expected by Workstation documentation.

At minimum:

- Headings
- Paragraphs
- Lists
- Links
- Code blocks
- Inline code
- Tables
- Emphasis
- Basic Markdown formatting

The rendered view should be readable and visually consistent with WGI.

---

# 10. Python File Handling

Python scripts are intentionally different from Markdown files.

For WGI 0.0.1:

**Do not display Python source code in the graphical file viewer.**

Python files should instead behave as launchable applications/scripts.

### Interaction

Single click:

```text
Select file
```

Double click:

```text
Launch Python script
```

The script opens in a new WGI window.

Example:

```text
┌─────────────────────────────────────────┐
│ tool.py                         ─ □ ×   │
├─────────────────────────────────────────┤
│                                         │
│             TERMINAL                    │
│                                         │
│ $ python tool.py                        │
│                                         │
│ > Running...                            │
│                                         │
└─────────────────────────────────────────┘
```

This prevents WGI from becoming a code editor in v0.0.1.

A code editor can be considered for a future WGI release.

---

# 11. Window System

WGI should implement a basic browser-based window manager.

Windows represent applications/tools.

Supported controls:

```text
[—] [□] [×]
```

### Minimize

Removes the window from the visible desktop while keeping its state alive.

### Maximize

Expands the window to fill the available WGI workspace.

### Close

Terminates/closes the associated application or terminal session.

### Window movement

Windows should be movable around the desktop.

### Window focus

Clicking a window brings it to the front.

The active window should have the highest z-index.

---

# 12. No macOS-Style Window Behavior

WGI should use conventional desktop window controls.

Do not design the window manager around macOS conventions.

Use:

```text
Minimize | Maximize | Close
```

rather than:

```text
Close | Minimize | Maximize
```

or macOS-specific traffic-light behavior.

The interface should feel platform-neutral and desktop-oriented.

---

# 13. Multiple Terminals

One of the major purposes of WGI is allowing multiple terminal sessions to exist simultaneously.

Example:

```text
Desktop

┌───────────────┐     ┌─────────────────────┐
│ Terminal 1    │     │ Terminal 2          │
│               │     │                     │
│ $ workstation │     │ $ python script.py  │
│               │     │                     │
└───────────────┘     └─────────────────────┘
```

Each terminal should have its own:

- Process/session
- Input
- Output
- Window state
- Minimize/maximize state
- Working directory

Closing one terminal must not close the others.

---

# 14. Terminal Safety

Because WGI provides terminal functionality, command execution must remain local and explicit.

Do not create a remote shell.

Do not expose arbitrary terminal functionality to external network users.

The WGI server should remain localhost-only by default.

Terminal processes should be associated with the Workstation process and cleaned up when Workstation shuts down.

---

# 15. Command Palette Integration

The existing Workstation Command Palette is a major part of WGI.

The Command Palette introduced in the previous release should become the central application launcher.

Example:

```text
┌──────────────────────────────────────────┐
│ Search Workstation...                    │
├──────────────────────────────────────────┤
│ Open README.md                           │
│ Open Documentation                       │
│ Launch workstation.py                    │
│ New Terminal                             │
│ Chemistry → Molar Mass                   │
│ Chemistry → Periodic Table               │
│ Graphing → Function Plotter              │
│ Settings                                 │
│ WGI Settings                             │
└──────────────────────────────────────────┘
```

### Critical architectural requirement

The Command Palette must use a shared command registry.

New Workstation features should automatically become discoverable by the Command Palette when they register themselves.

WGI should consume this same command system.

Do **not** create a second independent WGI command registry unless absolutely necessary.

---

# 16. Command Palette as Application Launcher

WGI should allow users to launch functionality through search rather than requiring every application to have a permanent icon.

For example:

```text
Search:
"terminal"

→ New Terminal

Search:
"molar"

→ Chemistry: Molar Mass

Search:
"periodic"

→ Chemistry: Periodic Table

Search:
"README"

→ Open README.md
```

This creates a consistent relationship between the CLI and graphical interface.

---

# 17. WGI Applications

WGI should treat Workstation functionality as applications.

Initial application types:

```text
Applications
├── Terminal
├── Documentation Viewer
├── Markdown Viewer
├── Python Launcher
└── Workstation Tools
```

Future releases can expose:

```text
Chemistry
Graphing
AI Chat
Settings
File Utilities
```

without requiring a complete rewrite of the window system.

---

# 18. Configuration

WGI configuration must integrate with Workstation's existing configuration architecture.

The project already uses a Workstation configuration file located at:

```text
~/.workstation_cli/config.json
```

WGI should not invent an unrelated configuration location.



### Browser Storage

Browser storage may be used for **WGI-specific UI state**, such as:

- Window positions
- Window sizes
- Last opened application
- Sidebar state
- UI preferences
- Session layout

However:

**Browser storage must not replace Workstation's authoritative configuration file.**

Think of it as:

```text
Workstation config
        │
        ├── CLI settings
        └── WGI settings
                 │
                 ▼
          Browser storage
          (UI/session state)
```

---

# 19. Configuration Synchronization

WGI should load configuration from Workstation when the interface starts.

Changes to Workstation settings should be reflected in WGI where appropriate.

Avoid storing duplicate configuration values in multiple locations.

For example:

```text
Theme
Port
WGI Enabled
Terminal preferences
```

should have a clear authoritative source.

Browser storage should primarily handle ephemeral graphical state.

---

# 20. Project Root

WGI must have a clearly defined project root.

The file explorer should not arbitrarily expose the entire filesystem.

The initial implementation should operate on the Workstation project/current working directory.

Example:

```text
WGI
└── Project Root
    ├── .dev
    ├── core
    ├── services
    ├── tests
    ├── README.md
    └── workstation.py
```

Future versions can introduce configurable workspace/project roots.

---

# 21. Security Boundaries

WGI is a local development interface, so security should be intentionally simple but not ignored.

### Default rules

- Bind to localhost.
- Do not require authentication for localhost use.
- Do not expose WGI publicly.
- Do not provide remote access in v0.0.1.
- Validate file paths.
- Prevent path traversal outside the project root.
- Restrict exposed file types.
- Avoid executing arbitrary browser-supplied commands without server-side validation.
- Clean up child processes.

The goal is a safe local utility, not a remotely accessible administration panel.

---

# 22. Dependency Strategy

Keep WGI lightweight.

The core Workstation CLI should not become dependent on a large frontend ecosystem simply to remain usable.

Prefer:

- Small local HTTP server
- Lightweight frontend
- Existing Workstation Python architecture
- Minimal JavaScript
- Existing project styling conventions where applicable

Avoid unnecessarily introducing:

- Large frontend frameworks
- External cloud services
- Authentication systems
- Databases
- Remote APIs

WGI must remain offline-first.

---

# 23. CLI Integration

Add WGI-related commands to Workstation.

Potential commands:

```text
workstation wgi
```

or equivalent existing command architecture.

Possible operations:

```text
WGI
├── Start
├── Stop
├── Open
└── Status
```

The exact CLI syntax should follow Workstation's existing command/menu architecture rather than creating a completely separate CLI convention.

---

# 24. Settings Integration

WGI should appear naturally inside Workstation Settings.

Example:

```text
Settings
  Extensions
    Workstation Graphical Interface
      Enabled
      Host
      Port
      Auto-open browser
```

When WGI is disabled, the CLI should continue working exactly as before.

---

# 25. UI State Persistence

Persist lightweight graphical state where useful.

Possible state:

```json
{
  "sidebar": {
    "width": 280,
    "collapsed": false
  },
  "windows": {
    "terminal-1": {
      "x": 100,
      "y": 80,
      "width": 800,
      "height": 500
    }
  }
}
```

This state belongs to the graphical experience rather than the CLI configuration itself.

---

# 26. WGI 0.0.1 Scope

WGI 0.0.1 should intentionally remain small.

### MUST HAVE

- Local web server
- Enable/disable setting
- Browser interface
- Workstation logo
- Project file tree
- Markdown rendering
- Documentation viewing
- Python script launching
- Basic terminal window
- Multiple terminal windows
- Minimize
- Maximize
- Close
- Window focus/z-order
- Command Palette integration
- Browser-side UI state
- Local-only security boundaries

### SHOULD HAVE

- Draggable windows
- Resizable windows
- Automatic port selection
- Auto-open browser option
- Clean loading/error states
- Empty-state UI
- Loading indicators
- Basic responsive behavior

### NOT IN WGI 0.0.1

- Full code editor
- Git GUI
- Remote development
- Cloud services
- User accounts
- Authentication
- Database
- Online file storage
- Collaboration
- Full IDE functionality
- Complete operating-system emulation
- Mobile-first interface
- Remote terminal access

---

# 27. Future WGI Direction

WGI 0.0.1 establishes the foundation.

Potential future versions:

```text
WGI 0.0.1
│
├── Project Explorer
├── Documentation
├── Python Launcher
└── Multi-Terminal
       │
       ▼
WGI 0.0.2
├── Better application management
├── Improved terminal UX
└── More Workstation tools
       │
       ▼
WGI 0.1.0
├── Chemistry applications
├── Graphing applications
├── AI Chat
└── Richer desktop environment
       │
       ▼
WGI 1.0.0
└── Mature graphical Workstation environment
```

Do not prematurely implement future functionality in 0.0.1.

---

# 28. CLI R1.1 Development Priorities

R1.1 should prioritize infrastructure required to make WGI possible.

### Phase 1 — Extension Infrastructure

- Define WGI as an optional Workstation extension.
- Establish extension loading/discovery.
- Ensure extensions cannot break the core CLI.
- Create shared interfaces for extension registration.
- Integrate extensions with Settings.

### Phase 2 — Command Registry

- Refine the existing Command Palette architecture.
- Create a shared command registry.
- Allow commands to expose:
  - Name
  - Description
  - Category
  - Action
  - Search keywords
- Allow WGI to consume the same registry.

### Phase 3 — WGI Backend

- Local HTTP server.
- API endpoints required by WGI.
- Project file discovery.
- Markdown retrieval.
- Python launcher.
- Terminal process management.
- Configuration access.
- Security/path validation.

### Phase 4 — WGI Frontend

Implement the desktop shell:

```text
Shell
├── Header
├── Logo
├── Command Palette
├── Sidebar
├── Desktop
└── Window Manager
```

### Phase 5 — Applications

Implement:

```text
Markdown Viewer
Documentation Viewer
Terminal
Python Launcher
```

### Phase 6 — Persistence

Implement browser-side UI state.

### Phase 7 — Integration

Connect WGI to:

- Settings
- Command Palette
- Workstation configuration
- Existing Workstation functionality

### Phase 8 — Testing & Polish

Test:

- Server startup/shutdown
- File access
- Markdown rendering
- Python launching
- Multiple terminals
- Window controls
- Window focus
- Command Palette
- Configuration
- Browser refresh behavior
- Invalid files
- Invalid paths
- Port conflicts
- Process cleanup

---

# 29. Testing Requirements

### Backend

Test:

- WGI server starts.
- WGI server stops.
- Server binds to localhost.
- Port conflicts are handled.
- Project root is enforced.
- Unsupported files are rejected.
- Markdown files are returned correctly.
- Python scripts launch correctly.
- Terminal processes are isolated.
- Child processes are cleaned up.

### Frontend

Test:

- Sidebar renders.
- File tree renders.
- Markdown opens.
- Python double-click launches a window.
- Terminal windows can coexist.
- Windows can be minimized.
- Windows can be maximized.
- Windows can be closed.
- Windows maintain correct focus.
- Command Palette opens.
- Commands launch correctly.
- Browser state persists.

### Regression

All existing Workstation CLI functionality must remain functional without WGI.

---

# 30. Documentation

Update:

### README

Document:

- R1.1
- WGI
- How to enable WGI
- How to start WGI
- Local URL behavior
- Requirements

### CHANGELOG

Add:

```text
R1.1 / v1.1.0

Workstation Graphical Interface v0.0.1
```

Clearly distinguish:

```text
Workstation CLI v1.1.0
```

from:

```text
WGI v0.0.1
```

### Developer Documentation

Document:

- Extension architecture
- WGI backend
- WGI frontend
- Command registry
- Configuration
- Security boundaries
- Process management

---

# 31. Versioning

The releases intentionally use separate version numbers.

## Workstation

```text
R1.1
v1.1.0
```

This is the primary Workstation CLI release.

## WGI

```text
WGI v0.0.1
```

This is the first version of the graphical extension.

These numbers should **not** be merged.

Example:

```text
Workstation R1.1 (v1.1.0)
└── WGI extension v0.0.1
```

---

# 32. Acceptance Criteria

R1.1 / WGI 0.0.1 is complete when:

- [ ] Workstation remains fully functional as a CLI without WGI.
- [ ] WGI can be enabled/disabled from Workstation Settings.
- [ ] WGI runs entirely locally.
- [ ] WGI binds to localhost by default.
- [ ] A browser can access the WGI interface.
- [ ] Workstation logo appears in the upper-left corner.
- [ ] Project structure appears in a sidebar.
- [ ] Only supported documentation/Markdown/Python files are exposed.
- [ ] Markdown files render as formatted documents.
- [ ] Python source code is not displayed.
- [ ] Double-clicking a Python script launches it.
- [ ] Python scripts open in their own window.
- [ ] Multiple terminals can run simultaneously.
- [ ] Windows support minimize.
- [ ] Windows support maximize.
- [ ] Windows support close.
- [ ] Windows can be moved and focused.
- [ ] Existing Command Palette functionality is available through WGI.
- [ ] Newly registered Workstation commands can appear in the Command Palette without creating a separate WGI implementation.
- [ ] Workstation configuration remains authoritative.
- [ ] Browser storage is used only for appropriate WGI UI/session state.
- [ ] Project-root boundaries are enforced.
- [ ] Child processes are cleaned up.
- [ ] WGI can be shut down cleanly.
- [ ] Existing Workstation tests continue to pass.
- [ ] New WGI functionality has appropriate automated tests.
- [ ] README and CHANGELOG document R1.1 and WGI 0.0.1.

---

# 33. Design Principle

The central design principle for R1.1 is:

> **WGI should make Workstation feel graphical without turning Workstation into a web application.**

Workstation remains the engine.

WGI is the interface.

The CLI and GUI should share the same underlying functionality, command system, configuration, and project context wherever practical.

```text
                 ┌───────────────────────┐
                 │      WORKSTATION      │
                 │   Core Functionality  │
                 └───────────┬───────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
       ┌──────▼──────┐               ┌──────▼──────┐
       │     CLI     │               │     WGI     │
       │   v1.1.0    │               │   v0.0.1    │
       └─────────────┘               └─────────────┘
              │                             │
          Terminal                       Browser
```

R1.1 should establish this architecture without overbuilding it.

The first WGI release should be **small, fast, local, useful, and extensible**.