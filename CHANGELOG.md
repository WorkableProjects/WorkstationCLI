# Changelog

All notable changes to Workstation CLI will be documented in this file.

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
