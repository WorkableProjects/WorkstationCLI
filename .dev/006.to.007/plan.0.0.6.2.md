# v0.0.6.2 — AI Superprompt & Foundation Overhaul

## AI Overhauls

### 0.0.6.2.a Remove Quiz Generator & Study Planner

- **Deprecate** the `run_quiz_generator()` and `run_study_planner()` from the AI menu.
- **Consolidate** their intended functionality into an improved **AI Chat** that uses a superprompt system.
- **Rationale**: Users can request quizzes and study plans directly through the chat interface with full conversational context—no need for separate, rigid workflows.

### 0.0.6.2.b Superprompt Architecture

Build a **versatile superprompt** that transforms the base AI Chat into a capable tutor, quiz engine, and study planner without switching modes.

- **Base Superprompt**: Establish a unified system prompt that covers:
  - Tutor mode (explain topics, answer questions)
  - Quiz generation (create problems, verify solutions)
  - Study planning (recommend resources, create schedules)
  - Code/chemistry problem-solving
  
- **Context Awareness**: Preserve multi-turn conversation state so follow-ups maintain coherence.
- **Reasoning Levels**: Enhance existing `ReasoningLevel` enum prompts to progressively encourage deeper thinking:
  - `MINIMAL`: "Answer directly and concisely."
  - `LOW`: "Brief planning, verify key facts."
  - `MEDIUM`: "Plan your approach, explain decisions, self-check conclusions."
  - `MAX`: "Extensive planning, explore alternatives, verify reasoning, provide comprehensive answer."

### 0.0.6.2.c Improved AI Chat Prompt

- Refactor `ai_chat_prompt()` in `services/ollama_prompts.py` to use the superprompt.
- **Add educational context**:
  - Clarify that responses should be educational, not just correct.
  - Encourage Socratic questioning when appropriate.
  - Define behavior for unsafe/out-of-scope requests.
- **Optimize token efficiency**: Remove redundant guidance, use structured formatting for clarity.

### 0.0.6.2.d Reasoning Level Enhancement

Adjust reasoning prompts to increasingly encourage model depth:

```python
REASONING_INSTRUCTIONS: dict[ReasoningLevel, str] = {
    ReasoningLevel.MINIMAL: "Answer directly. Avoid unnecessary explanation.",
    ReasoningLevel.LOW: "Use light planning. Verify important facts. Stay concise.",
    ReasoningLevel.MEDIUM: "Plan before answering. Explain key decisions. Self-check conclusions.",
    ReasoningLevel.MAX: "Use extensive planning. Consider alternatives. Self-verify. Provide complete answer with reasoning.",
}
```
