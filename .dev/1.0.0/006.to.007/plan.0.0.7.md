# v0.0.7 — The Overhaul (Full Release)

## Integration & Release

- **Consolidate v0.0.6.2 through v0.0.6.5** into a single v0.0.7 release.
- **Update Documentation**:
  - README: New tab-based navigation, superprompt, graphing features.
  - CHANGELOG: Summarize all improvements. (all files excluding this one in ~/.dev/006.to.007/
  - Help/About: Reflect new structure and capabilities.
  
- **Version Bump**: `0.0.6` → `0.0.7` in `core/banner.py`.

- **User Communication**:
  - Highlight removal of Quiz Generator/Study Planner and migration to AI Chat.
  - Show navigation examples (tab switching, keyboard controls).
  - Showcase graphing enhancements (multi-series, presets, export).

---

## Summary: Phased Rollout

| Version | Focus | Key Changes |
|---------|-------|------------|
| **v0.0.6.2** | AI Superprompt | Remove Quiz/Study Planner, unify into superprompt chat, enhance reasoning levels |
| **v0.0.6.3** | UI Navigation | Horizontal tabbed layout, startup animation, keyboard navigation |
| **v0.0.6.4** | Graphing | Multi-series plotting, more presets, export, derivative/integral viz, help expansion |
| **v0.0.6.5** | Quality | Test coverage, refactor menu infrastructure, settings expansion |
| **v0.0.7** | Final Release | Consolidated, tested, documented overhaul release |

---

## Open Questions & Future Considerations

1. **Accessibility**: Ensure tabbed navigation works with screen readers (ARIA labels, semantic HTML where applicable).
2. **Performance**: Verify multi-series graphing performance on slower terminals.
3. **Mobile/Narrow Terminals**: Define fallback behavior if terminal width < 80 chars.
4. **Platform Support**: Test animation and tab behavior on macOS, Linux, Windows (WSL).
5. **Extensibility**: Can the tab/menu system support plugins or user-defined tools?

---

## Acceptance Criteria — v0.0.7

- [x] AI Chat uses superprompt; Quiz Generator & Study Planner removed from menu.
- [x] Horizontal tab navigation fully functional with keyboard controls.
- [x] Startup animation plays on launch (can be disabled in settings).
- [x] Multi-series graphing works with 2+ functions.
- [x] Preset functions expanded to 10+ with categories.
- [x] Plot export to `.txt` implemented.
- [x] Graphing help/documentation comprehensive.
- [x] Test coverage > 80%.
- [x] All existing features (Chemistry calculators, etc.) remain functional.
- [x] Documentation and CHANGELOG updated.
