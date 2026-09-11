# Workstation CLI — 0.0.8 → 1.0.0 Jules Implementation Plan

## How to use this plan

Implement **one phase at a time**.

For every phase:

1. Read the existing code before changing it.
2. Implement only the scope of the current phase.
3. Run the relevant tests/checks.
4. Fix regressions caused by the phase.
5. Leave the repository in a working state.
6. Only move to the next phase after acceptance criteria pass.

Do not combine the entire roadmap into one large task.

---

# 0.0.8

## Goal

Turn the 0.0.7 overhaul into a cohesive application with shared infrastructure, consistent UX, fast navigation, reusable input/output systems, and lightweight session context.

## Phase 0 — Foundation

### Tasks

- Review the current 0.0.7 architecture.
- Identify duplicated:
  - menu code
  - input handling
  - output rendering
  - navigation
  - error handling
- Create shared infrastructure where practical.
- Preserve existing Chemistry, AI, Graphing, Settings, and About functionality.
- Standardize:
  - navigation
  - headers/screens
  - input
  - validation
  - errors
  - help
  - back/exit behavior
  - output actions
- Add/update tests for shared infrastructure.

### Acceptance Criteria

- Existing 0.0.7 functionality still works.
- Shared infrastructure is reusable.
- No major regressions.
- The codebase is ready for the remaining 0.0.8 phases.

---

## Phase 1 — Unified Tool Architecture

### Goal

Make every major section behave like part of the same application.

### Standard Tool Lifecycle

Every major tool should follow:

1. Enter tool.
2. Display header/context.
3. Display available actions.
4. Accept input.
5. Validate input.
6. Execute operation.
7. Render result.
8. Offer relevant output actions.
9. Allow back/navigation without restarting.

Apply this to:

- Chemistry
- Periodic Table
- Graphing
- AI
- Settings
- About

### Standardize

- Headers
- Menus
- Navigation footer/help
- Input prompts
- Validation messages
- Error messages
- Result formatting
- Back behavior
- Quit behavior

### Acceptance Criteria

- Major tools look and behave consistently.
- Users do not need a different interaction model for each tool.
- Shared behavior uses reusable code instead of duplication.

---

## Phase 2 — Command Palette

### Goal

Provide fast keyboard-first access to major functionality.

### Feature

Add a **Command Palette**, preferably using `Ctrl+K`.

### Requirements

The palette must:

- Search tools.
- Search major actions.
- Launch Chemistry tools.
- Open the Periodic Table.
- Open Graphing.
- Open AI Chat.
- Open Settings.
- Open Help/About where appropriate.
- Support keyboard navigation.
- Execute the selected command with Enter.
- Close with Escape without disrupting application state.

### Acceptance Criteria

- `Ctrl+K` opens the palette where supported.
- Commands can be searched and launched.
- Keyboard navigation works.
- Escape returns to the previous state cleanly.

---

## Phase 3 — Standardized Input System

### Goal

Create reusable input/form infrastructure.

### Supported Input Types

- Text
- Numeric
- Decimal
- Integer
- Selection lists
- Yes/No
- Range/domain
- Optional values
- Defaults
- Validation errors
- Cancel/back

### Requirements

Inputs must:

- Clearly show expected input.
- Give useful validation errors.
- Preserve valid values where practical.
- Support keyboard-first navigation.
- Allow cancellation without crashing or losing state.

### Acceptance Criteria

- Major tools use the shared input system.
- Validation is consistent.
- Normal invalid input never produces an unhandled traceback.

---

## Phase 4 — Universal Output Actions

### Goal

Give generated results a consistent set of actions.

### Standard Actions

Use these where applicable:

- `[Copy]`
- `[Save]`
- `[Export]`
- `[Send to AI]`
- `[Back]`

Not every result needs every action.

### Requirements

- Only show supported actions.
- Chemistry calculations produce reusable formatted output.
- Graph text/export follows the same conventions where practical.
- AI responses support appropriate copy/save behavior.
- Output remains readable in narrow terminals.

### Acceptance Criteria

- Output actions are consistent.
- Copy/save/export failures are handled cleanly.
- Users can return without restarting the tool.

---

## Phase 5 — Session Context

### Goal

Add temporary continuity during a running application session.

### Scope

This is **session context**, not persistent workspaces.

Possible session data:

- Recent calculations
- Current graph configuration
- Recently selected element
- AI conversation context
- Recent generated output

### Requirements

- Session data exists only while the application is running unless explicitly saved/exported.
- Users can clear session context.
- Unrelated tools must not become dependent on hidden session state.
- AI conversation context remains intact during the active conversation.
- Do not implement persistent workspaces.

### Acceptance Criteria

- Useful session information survives normal navigation.
- Clearing context works predictably.
- Exiting does not create persistent workspace data.

---

## Phase 6 — 0.0.8 Polish

### Tasks

- Run the complete test suite.
- Add integration tests for shared UI infrastructure.
- Test keyboard navigation.
- Test Command Palette.
- Test input validation.
- Test output actions.
- Test session context.
- Test narrow-terminal behavior.
- Verify Chemistry.
- Verify Graphing.
- Verify AI.
- Verify Settings.
- Update README.
- Update CHANGELOG.
- Update version information.

### 0.0.8 Acceptance Criteria

- Workstation CLI feels like one cohesive application.
- Shared navigation/input/output infrastructure is complete.
- Command Palette works.
- Session context works without becoming a workspace system.
- Existing features remain functional.
- Tests pass.
- Documentation matches 0.0.8.

---

# RC1 (codename 0.0.9)

## Goal

Harden Workstation CLI until it is release-candidate quality.

Focus on reliability, performance, testing, documentation, cleanup, and release readiness.

---

## Phase 7 — Reliability & Error Handling

### Audit For

- Unhandled exceptions
- Invalid user input
- Missing dependencies
- Missing configuration
- Invalid configuration
- Ollama unavailable
- Invalid AI model
- Graphing failures
- Invalid mathematical expressions
- File read/write failures
- Export failures
- Terminal-size edge cases

### Requirements

Normal user errors should provide:

- A clear explanation.
- A useful recovery action.
- No unnecessary traceback.

Developer/debug information may remain available through an appropriate debug mode.

### Acceptance Criteria

- Common user errors are handled gracefully.
- No obvious normal-use path unexpectedly crashes.
- Error behavior is consistent across tools.

---

## Phase 8 — Performance & Responsiveness

### Measure

- Startup time
- Menu navigation
- Periodic Table loading/rendering
- Chemistry calculations
- Graph generation
- Preset loading
- AI prompt preparation
- AI response handling
- File export

### Requirements

- Remove unnecessary repeated computation.
- Remove unnecessary rendering.
- Keep startup lightweight.
- Keep graphing responsive at reasonable resolutions.
- Avoid blocking unrelated UI work during AI processing where practical.

### Important Constraint

AI generation speed depends heavily on the local Ollama model and hardware.

Do not promise a specific LLM generation speed. Optimize Workstation CLI overhead instead.

### Acceptance Criteria

- No obvious performance regressions.
- Startup/navigation feel immediate.
- Expensive operations provide feedback when needed.

---

## Phase 9 — Testing Expansion

### Unit Tests

Cover:

- Chemistry calculations
- Element data
- Electron configurations
- Graphing calculations
- Presets
- Input validation
- Formatting
- Settings
- Configuration
- Shared UI infrastructure

### Integration Tests

Cover:

- Application navigation
- Chemistry flows
- Periodic Table flows
- Graphing flows
- AI flows
- Settings flows
- Command Palette
- Output actions
- Session context

### Regression Tests

Every previously fixed bug should receive a regression test where practical.

### Target

Maintain **80%+ meaningful test coverage**.

Prioritize important behavior over chasing a raw percentage.

### Acceptance Criteria

- Test suite is reliable.
- Core behavior is covered.
- Regressions are automatically caught.
- 80%+ meaningful coverage is reached, or uncovered code is intentionally documented.

---

## Phase 10 — Documentation

### Update

- `README.md`
- `CHANGELOG.md`
- Architecture documentation
- Chemistry documentation
- Graphing documentation
- AI documentation
- Configuration documentation
- Development documentation
- Installation/setup instructions

### Documentation Must Explain

- What Workstation CLI is.
- Requirements.
- How to install/run it.
- Python version requirement.
- How Ollama is used.
- Supported AI models/configuration.
- Major features.
- Keyboard controls.
- Configuration.
- Troubleshooting.
- Development/testing.

### Python Requirement

Clearly document:

**Workstation CLI requires Python 3.11+.**

### Explicit Scope Exclusion

Cross-platform hardening is **not part of 0.0.9**.

Beyond the Python 3.11+ requirement, broader platform-specific hardening/support is deferred to a later release.

### Acceptance Criteria

- A new user can install and run the application from the documentation.
- Developers can understand the architecture/workflow.
- Configuration and troubleshooting are documented.
- Python 3.11+ is clearly stated.

---

## Phase 11 — RC1 Polish

### Tasks

- Remove obsolete code.
- Remove dead code.
- Remove temporary debugging.
- Review dependencies.
- Review configuration defaults.
- Review terminal rendering.
- Review all user-facing wording.
- Review keyboard shortcuts.
- Review help screens.
- Review loading/progress states.
- Review version strings.
- Review startup behavior.
- Review README examples.
- Perform a clean installation test.
- Perform a fresh-user walkthrough.

### RC1 Acceptance Criteria

- No known high-severity bugs remain.
- User-facing behavior is polished.
- Documentation is complete.
- Clean installation works.
- Fresh-user walkthrough works.
- Feature set is ready for 1.0.0 feature freeze.

---

# R1 (codename 1.0.0)

## Goal

Freeze the feature set and ship a stable Workstation CLI release.

**1.0.0 is a stabilization/release milestone, not another feature dump.**

---

## Phase 12 — 1.0.0 Feature Freeze

### Rule

After this phase, do not add major features unless there is an explicit decision to postpone 1.0.0.

### Intended 1.0.0 Product Areas

### Chemistry

- Molar Mass
- Gas Laws
- Stoichiometry
- Limiting Reagent
- Percent Yield
- Dilution
- Concentration
- Interactive Periodic Table
- Element Properties
- Electron Configurations

### Mathematics / Graphing

- Custom Functions
- Multiple Functions
- Presets
- Domain/Range Controls
- Calculus Visualization
- Derivative Visualization
- Integral Visualization
- Graph Export
- Graph Help/Tutorial

### AI

- Local Ollama integration
- AI Chat
- Unified superprompt
- Reasoning levels
- Multi-turn context
- Chemistry assistance
- Math assistance
- Study assistance
- Educational/tutor behavior

### UX

- Horizontal tab navigation
- Command Palette
- Consistent menus
- Consistent forms/input
- Consistent output actions
- Keyboard-first interaction
- Responsive terminal layouts
- Themes
- Startup animation/settings

---

## Phase 13 — Final Stability Pass

### Tasks

Run:

- All automated tests.
- All integration tests.
- Manual testing of every major feature.
- Fresh installation testing.
- Missing/invalid configuration tests.
- Ollama-unavailable tests.
- Invalid AI model tests.
- Malformed graph-function tests.
- Invalid chemistry-input tests.
- File-export failure tests.
- Small-terminal tests.
- Application restart tests.
- Normal exit/back behavior tests.

### Acceptance Criteria

- No known release-blocking bugs remain.
- All core features work as documented.
- Normal error conditions are handled cleanly.

---

## Phase 14 — Release Documentation & Packaging

### Tasks

- Finalize README.
- Finalize CHANGELOG.
- Finalize installation instructions.
- Finalize requirements/dependencies.
- Finalize configuration documentation.
- Finalize troubleshooting documentation.
- Finalize architecture/development documentation.
- Update all version references to `1.0.0`.
- Verify package/application metadata.
- Verify startup/version display.
- Prepare release notes.

### Acceptance Criteria

- Documentation exactly matches the released software.
- Version numbers are consistent.
- A clean user can follow the installation process successfully.

---

## Phase 15 — 1.0.0 Final Verification

### Final Checklist

- [ ] Application starts successfully.
- [ ] Main navigation works.
- [ ] Chemistry tools work.
- [ ] Periodic Table works.
- [ ] Electron configuration tools work.
- [ ] Graphing works.
- [ ] Multiple graph series work.
- [ ] Graph presets work.
- [ ] Graph export works.
- [ ] Calculus visualization works.
- [ ] AI Chat works with Ollama.
- [ ] AI context works.
- [ ] AI reasoning levels work.
- [ ] Settings work.
- [ ] Command Palette works.
- [ ] Input validation works.
- [ ] Output actions work.
- [ ] Session context works.
- [ ] Error handling works.
- [ ] Tests pass.
- [ ] Documentation is current.
- [ ] Python 3.11+ requirement is documented.
- [ ] Version is `1.0.0`.
- [ ] No known release-blocking issues remain.

---

# Explicitly Deferred

These are intentionally outside the 0.0.8 → 1.0.0 roadmap:

- Cross-Tool Integration
- Persistent Workspaces
- Accessibility work
- Cross-Platform Hardening

### Python Requirement

Workstation CLI requires **Python 3.11+**.

More extensive cross-platform hardening/support can be handled after 1.0.0.

---

# Jules Execution Rules

Jules should treat each phase as an independent implementation task.

## Required Workflow

**Plan → Implement → Test → Review → Commit → Next Phase**

## Important Rules

1. Do not implement multiple phases at once unless explicitly requested.
2. Do not introduce deferred features.
3. Do not replace working architecture without a clear reason.
4. Preserve existing functionality while refactoring.
5. Prefer reusable infrastructure over duplicated implementations.
6. Add tests for new shared behavior.
7. Fix regressions before completing a phase.
8. Keep the repository working after every phase.
9. Read relevant existing code before modifying it.
10. Do not claim a phase is complete until its acceptance criteria are verified.

## Release Structure

```text
0.0.8
├── Phase 0 — Foundation
├── Phase 1 — Unified Tool Architecture
├── Phase 2 — Command Palette
├── Phase 3 — Standardized Input System
├── Phase 4 — Universal Output Actions
├── Phase 5 — Session Context
└── Phase 6 — Polish & Verification

RC1 (codename 0.0.9)
├── Phase 7 — Reliability & Error Handling
├── Phase 8 — Performance & Responsiveness
├── Phase 9 — Testing Expansion
├── Phase 10 — Documentation
└── Phase 11 — RC1 Polish

R1 (codename 1.0.0)
├── Phase 12 — Feature Freeze
├── Phase 13 — Final Stability Pass
├── Phase 14 — Release Documentation & Packaging
└── Phase 15 — Final Verification
```
