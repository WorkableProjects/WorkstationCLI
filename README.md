# Workstation CLI

**Workstation CLI** is an offline, terminal-based chemistry calculator, graphing tool suite, and local Ollama-powered AI study tool designed for students and educators.

Made by **Workable Projects** (Created by **Dutchh**).

[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-1.1.0-green)]()
[![WGI Version](https://img.shields.io/badge/WGI-0.0.1-blue)]()
[![License](https://img.shields.io/badge/license-WCLI.L-blue)](https://github.com/WorkableProjects/WorkstationCLI/blob/main/LICENSE.md)

Workstation CLI v1.1.0 (Release 1.1) / Workstation Graphical Interface (WGI) v0.0.1

## Requirements

- **Python**: **3.11+** required.
- **AI Backend (Optional)**: [Ollama](https://ollama.ai) installed locally for AI Chat feature.

## Installation & Running

```bash
# Clone repository
git clone https://github.com/WorkableProjects/WorkstationCLI.git
cd WorkstationCLI

# Run Workstation CLI
python3 workstation.py
```

## Workstation Graphical Interface (WGI)

R1.1 introduces **WGI**, an optional browser-based graphical workspace extension for Workstation CLI.

- **Enabling WGI**: Go to `Settings` -> `Extensions` or edit `~/.workstation_cli/config.json` (`wgi.enabled: true`).
- **Accessing WGI**: When enabled, start Workstation to launch the local web server at `http://127.0.0.1:8080` (or run `workstation wgi`).
- **Features**: Browser desktop interface, project file tree, Markdown viewer, python script launcher windows, multi-terminal sessions, Command Palette integration, and persisted browser layout state.

## Key Features

- **Horizontal Tabbed Navigation**:
  - Seamless category tabs (`Chemistry`, `AI`, `Graphing`, `Settings`, `About`) with all options directly accessible via arrow keys (`←`/`→` switch tabs, `↑`/`↓` navigate options, `Enter` executes).
- **Command Palette (`Ctrl+K` or `/`)**:
  - Instant keyboard-first launcher to search and jump to any calculator, graphing function, AI chat, or setting across the application.
- **Interactive Chemistry Suite**:
  - 8 full calculators (Molar Mass, Gas Laws, Stoichiometry, Limiting Reagent, Percent Yield, Dilution, Concentration, Reference Lookups) and an interactive 118-element 2D Periodic Table with electron configuration and subshell details.
- **Advanced Graphing Engine**:
  - Custom function plotting with domain/range controls and outlier filtering for asymptotes.
  - **Multi-Series Comparison**: Plot 2 to 5 functions simultaneously with distinct Unicode symbols (`●`, `○`, `×`, `+`, `◆`) and formatted legends.
  - **Calculus Visualizations**: Numerical Derivative plotter ($f(x)$ & $f'(x)$) and Definite Integral calculator ($\int_a^b f(x) dx$ via Simpson's rule).
  - **Preset Library**: 13 categorized function presets (Polynomials, Trigonometric, Exponential & Logarithmic, Special Functions).
  - **Plot Export**: Save ASCII/Unicode plots with domain/range metadata directly to `.txt` files.
- **Local Ollama AI Integration**:
  - Multi-mode AI study assistant with superprompts and configurable reasoning levels (`Minimal`, `Low`, `Medium`, `Max`).
- **Comprehensive Settings & Session Management**:
  - Preferences for appearance themes, startup ASCII animation toggle, default graphing parameters, and developer config tools (`~/.workstation_cli/config.json`).

## Controls & Keyboard Shortcuts

- `←` / `→` (or `a` / `d`, `h` / `l`): Switch horizontal menu tabs.
- `↑` / `↓` (or `w` / `s`, `k` / `j`): Navigate options list or 2D grid items.
- `Enter`: Execute selected option or select element/item.
- `Ctrl+K` or `/`: Open Command Palette search from main menu.
- `q` or `Esc`: Return to previous menu or exit active tool.

## Documentation & Resources
- [Changelog](CHANGELOG.md)
- [License](LICENSE.md)
