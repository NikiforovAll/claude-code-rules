# Structured Plan Mode

Structured planning methodology for complex feature implementations through systematic task decomposition.

## Features

- Phased approach: Setup → Research → Finalize → Tasks → Implement → Review
- Task breakdown with clear dependencies and success criteria
- User collaboration through iterative approach selection
- Track progress in `.plans/` directory with individual task files
- TodoWrite integration for phase tracking

## Installation

```bash
/plugin marketplace add nikiforovall/claude-code-rules
/plugin install handbook-structured-plan-mode
```

## Usage

The skill activates for complex feature implementations:

```
"Use structured-plan-mode to implement real-time collaboration"
"Plan the multi-tenant architecture feature"
"Create a structured plan for the payment integration"
```

**Example:**
```
You: "Use structured-plan-mode to add authentication system"
Claude: Creates .plans/authentication-system/ directory, researches approaches,
        proposes options, creates task files after user confirms approach
```
