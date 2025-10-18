---
title: "Use Extended Plan Mode"
sidebar_position: 5
---

# Use Extended Plan Mode

A structured multi-stage approach for implementing features with Claude Code:

**Stage 1: Context Priming**
- Provide Claude with proper context about the codebase
- Share requirements and implementation details
- Help Claude understand existing patterns and architecture

**Stage 2: Planning**
- Use Claude Code's **Plan Mode** to create an implementation plan
- Review the plan thoroughly before proceeding
- Ensure all edge cases and requirements are covered

**Stage 3: Implementation**
- Let Claude Code follow the plan autonomously
- Monitor progress and inspect changes as they happen
- Provide additional context or course-correct if needed

**Stage 4: Evaluation**
- Enable Claude Code to evaluate the task outcome
- Use unit tests and integration tests for validation
- For frontend changes, use Playwright or similar tools to verify visual results

**When to use:** Complex feature development requiring multiple steps and verification. Ideal for production code where quality and correctness are critical.

:::tip
Act as a supervisor during implementation - stay engaged but let Claude work through the plan independently.
:::

:::tip
The evaluation stage is very important - having automated tests or visual verification tools ready before starting saves time and ensures quality.
:::

```mermaid
flowchart TD
    subgraph Developer
        D1[Provide context:<br/>codebase, requirements,<br/>patterns]
        D2[Review plan<br/>thoroughly]
        D3[Monitor progress<br/>and inspect changes]
        D4{Course<br/>correction<br/>needed?}
        D5[Provide additional<br/>context/guidance]
        D6[Review results &<br/>approve feature]
    end

    subgraph Claude_Code[Claude Code]
        C1[Understand context<br/>and requirements]
        C2[Create implementation<br/>plan using Plan Mode]
        C3{Plan<br/>approved?}
        C4[Implement feature<br/>autonomously]
        C5[Run evaluation:<br/>Unit tests<br/>Integration tests<br/>E2E tests]
        C6{Tests<br/>pass?}
        C7[Analyze failures<br/>and suggest fixes]
    end

    Start([Start]) --> D1
    D1 --> |Context| C1
    C1 --> C2
    C2 --> D2
    D2 --> C3
    C3 --> |No| C2
    C3 --> |Yes| C4
    C4 --> D3
    D3 --> D4
    D4 --> |Yes| D5
    D5 --> |Additional context| C4
    D4 --> |No| C5
    C5 --> C6
    C6 --> |No| C7
    C7 --> |Fix| C4
    C6 --> |Yes| D6
    D6 --> End([Complete])

    style Developer fill:#e1f5ff
    style Claude_Code fill:#ffe1e1
```
