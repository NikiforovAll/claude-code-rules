---
description: Magazine-quality slide deck as a self-contained HTML page
argument-hint: "[topic] [--style <name>] [--theme light|dark]"
disable-model-invocation: true
---
Load the visual-explainer skill, then generate a slide deck about the topic below. Any `--flags` in it belong to the skill's Arguments table, not to the topic.

Topic: $ARGUMENTS

Follow **Slide Deck Mode** in the skill — it owns the reading list, the narrative arc, and the composition rules.

**Slide output is always opt-in.** Only generate slides when this command is invoked or the user explicitly asks for a slide deck.

**Aesthetic:** pick one of the four slide presets in `slide-patterns.md` (Midnight Editorial, Warm Signal, Terminal Mono, Swiss Clean), or any `--style` value from the skill's table adapted for slides. Vary from previous decks and carry the choice through every slide.
