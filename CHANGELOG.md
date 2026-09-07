# Changelog

All notable changes to Workstation CLI will be documented in this file.

## [0.0.7] - March 3, 2025

### Added
- **UI Navigation Overhaul (v0.0.6.3)**:
  - Replaced nested submenus with a top-level horizontal tabbed layout (`[Chemistry]`, `[AI]`, `[Graphing]`, `[Settings]`, `[About]`).
  - Options for each category are rendered directly under the active tab without requiring nested enter steps.
  - Controls: `←`/`→` switch tabs, `↑`/`↓` navigate options, `Enter` executes options directly.
  - Startup ASCII/Unicode banner animation with slide-in effect and toggle support in Settings.
- **Graphing Overhauls & Calculus Tools (v0.0.6.4)**:
  - **Advanced Multi-Series Plotting**: Plot 2 to 5 functions simultaneously on shared axes with distinct Unicode symbols (`●`, `○`, `×`, `+`, `◆`) and formatted legends.
  - **Categorized Preset Library**: Expanded function presets to 13 categorized entries across Polynomials, Trigonometric, Exponential & Logarithmic, and Special Functions.
  - **Calculus Visualizations**: Added Numerical Derivative plotter ($f(x)$ & $f'(x)$) and Numerical Definite Integral calculator ($\int_a^b f(x) dx$ via Simpson's rule).
  - **Plot Export**: Save ASCII/Unicode rendered plots with metadata directly to `.txt` plain-text files.
- **AI Superprompt & Reasoning Levels (v0.0.6.2)**:
  - Consolidated Quiz Generator and Study Planner into a unified AI Chat superprompt with configurable reasoning levels (`Minimal`, `Low`, `Medium`, `Max`).
- **Expanded Settings & System Configuration (v0.0.6.5)**:
  - Categorized settings menu covering AI model configuration, UI preferences (theme selection & startup animation toggle), Graphing default parameters, and developer config tools.
  - Config storage in local user directory (`~/.workstation_cli/config.json`).
- **Expanded Test Suite**:
  - Added comprehensive test suites for horizontal tab menu navigation, multi-series plotting, numerical derivative/integral calculations, plot export, and AI superprompts.

### Changed
- Upgraded version string to `0.0.7` across `core/banner.py`, `services/ollama_prompts.py`, and `README.md`.
- Consolidated all v0.0.6.2 - v0.0.6.5 features into the official v0.0.7 overhaul release.

## [0.0.6] - March 3, 2025

### Added
- **Interactive Chemistry & Periodic Table**:
  - Transformed Periodic Table lookup into a 118-element interactive 2D grid component with arrow-key navigation, selected tile highlighting, and quick search.
  - Preserved traditional 18-group layout and detached Lanthanide (57-71) and Actinide (89-103) rows.
  - Comprehensive Element Detail View with expanded metadata: state, electronegativity, valence electrons, oxidation states, phase, block, period, and group.
  - Electron Configuration Engine: Noble-gas shorthand, formatted subshell notation (e.g. 1s² 2s² 2p⁶), orbital occupancy, shell electron count summary (n=1..7), and explicit ground-state exception handling.
- **Reusable Terminal UI Infrastructure**:
  - Reusable `GridSelector` and `DetailPanel` primitives in `core/ui.py` supporting 2D navigation, responsive compact mode for narrow terminals, and search/jump interaction.
- **Graphing Tool Enhancements**:
  - Explicit X-domain controls clarifying left → right visible bounds (`X-axis minimum (left edge)`, `X-axis maximum (right edge)`).
  - Explicit separation between X domain, Y range (auto scaling vs custom bounds), and plot size (width x height).
  - Submenu restructure: `Plot Custom Function`, `Preset Functions`, `Plot Settings`, `Graph Help / Controls`.
  - Plotter Engine: Multi-series plotting data model (`PlotSeries`), improved zero-axis intersection markers (`┼`, `│`, `─`), endpoint axis labels, and domain/range summary header/footer.
  - Robustness & Asymptote Handling: Outlier filtering for auto Y-scaling near asymptotes (e.g. `1/x`) and clean handling of undefined domain points (`nan`, `inf`).

### Changed
- Upgraded CLI version from 0.0.5.0 to 0.0.6.
- Refactored element lookup and detail formatting into canonical implementations in `chemistry/periodic_table.py`.
- Updated version strings in `core/banner.py`, `services/ollama_prompts.py`, and `README.md`.

## [0.0.5.0(b)] - September 6, 2026

### Added
- **Graphing Tool**: New top-tier main menu category alongside Chemistry and AI.
  - Interactive ASCII/Unicode terminal function plotter (`f(x)` evaluation).
  - Support for mathematical functions including polynomials, trigonometric functions, exponentials, logarithms, and roots.
  - Preset function library (Quadratic, Cubic, Sine, Cosine, Gaussian, Logarithmic, Reciprocal).
  - Customizable plot range/domain and plot scaling.
- **Context Help Support**: Added contextual help for Graphing Tool and Preset Functions menus.

### Changed
- Upgraded CLI version from 0.0.4.1 to 0.0.5.0.
- Updated main menu routing in `workstation.py` to include Graphing as Option 3.
- Refactored prompt templates and banner version strings across `core/banner.py` and `services/ollama_prompts.py`.
- Updated documentation in `README.md` and added link to `CHANGELOG.md`.
