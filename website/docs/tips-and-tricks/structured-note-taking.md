---
title: "Structured Note-Taking"
sidebar_position: 14
---

Structured note-taking is a powerful technique where Claude regularly writes notes that persist outside the context window. These notes can be retrieved later when needed, providing persistent memory and building institutional knowledge over time.

## Why Structured Notes Matter

- **Persistent Memory**: Unlike context that gets lost when the window fills up, notes persist across sessions and compactions
- **Minimal Overhead**: Notes are only loaded when relevant, keeping the active context clean
- **Progressive Building**: Information accumulates over time, building a knowledge base specific to your project
- **Context Recovery**: After context resets, Claude can read its own notes and continue seamlessly
- **Knowledge Transfer**: Team members can understand project history and decisions through well-maintained notes

## Effective Note-Taking Patterns

### Context Preservation
Use temporary files to preserve current context when transitioning between sessions or topics:
- **Working Memory**: Create a `CURRENT_SESSION.md` file that gets updated throughout a session and can be referenced later
- **Context Bridging**: Create summary files that capture the essential context from one session to inform the next

**💡 Examples:**

```
🗣️"Please create a CURRENT_SESSION.md file summarizing our conversation so far, 
focusing on the key decisions about the API design and the remaining tasks"

🗣️"Save the current context about the database migration to MIGRATION_CONTEXT.md 
so we can reference it later"

🗣️"Create a SESSION_SUMMARY.md capturing what we've learned about the performance 
issues and the solutions we've tried"
```

This allows you to:
- Start fresh sessions while maintaining continuity
- Reference previous work without cluttering current context
- Build a timeline of project evolution
- Recover from context window limitations seamlessly

### Decision Logs
Maintain `DECISIONS.md` to record:
- What was decided and when
- Rationale behind each decision
- Alternative approaches considered
- Impact on other parts of the system
- Who was involved in the decision

#### Architectural Decision Records (ADRs)
Use ADR format for important architectural decisions that both humans and AI agents can easily understand and reference:

**ADR Template:**
```markdown
# ADR-001: Use PostgreSQL for Primary Database

## Status
Accepted

## Context
We need to choose a database for our new microservice that will handle user data,
transactions, and reporting. The service expects high read/write throughput and
needs ACID compliance.

## Decision
We will use PostgreSQL as our primary database.

## Consequences
### Positive
- Strong ACID compliance and reliability
- Excellent performance for complex queries
- Rich ecosystem and tooling
- Team familiarity

### Negative
- Higher operational complexity than NoSQL alternatives
- Scaling limitations compared to distributed databases
- Additional infrastructure requirements

## Alternatives Considered
- MongoDB: Rejected due to consistency concerns
- MySQL: Rejected due to JSON handling limitations
- DynamoDB: Rejected due to query flexibility needs
```

**💡 Example:**

```
🗣️"Create an ADR for our decision to use Redis for caching, 
following the standard ADR template with status, context, decision, and consequences"

🗣️"Update ADR-003 status from 'Proposed' to 'Accepted' and add the implementation 
timeline we discussed"

🗣️"Generate ADR-005 documenting our choice of microservices architecture,
including the alternatives we considered and why we rejected them"
```

**Benefits for AI agents:**
- **Structured Context**: ADRs provide consistent, scannable decision context
- **Historical Reasoning**: Agents can understand why past decisions were made
- **Impact Assessment**: Clear consequences help agents evaluate related changes
- **Consistency**: Standardized format makes information easily parseable

### Learning Notes
Keep `LEARNINGS.md` for:
- Patterns that work well in this codebase
- Common pitfalls discovered
- Performance considerations
- Best practices specific to this project
- External resources and references

### Troubleshooting Guides
Document `TROUBLESHOOTING.md` with:
- Common issues and their solutions
- Debugging steps that proved effective
- Environment-specific gotchas
- Configuration pitfalls and fixes

## Implementation Tips

- **Be Specific**: Include concrete details, file paths, and specific methods rather than vague descriptions
- **Regular Updates**: Update notes after completing significant tasks or making important discoveries
- **Structured Format**: Use consistent headings, bullet points, and organization for easy scanning
- **Cross-References**: Link between different note files and reference specific code locations
- **Date Stamps**: Include timestamps for time-sensitive information
- **Examples**: Provide concrete code examples and command snippets where relevant

## Benefits in Practice

This approach transforms how Claude handles complex, multi-session projects by:
- **Maintaining Continuity**: Sessions can pick up exactly where they left off
- **Building Expertise**: Knowledge accumulates rather than being lost
- **Improving Efficiency**: Less time spent re-explaining context
- **Creating Documentation**: Notes serve as living documentation for the team
- **Supporting Debugging**: Historical context helps identify root causes

## Additional References

- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) - Anthropic's guide covering structured note-taking and agentic memory
- [Memory and Context Management Cookbook](https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/memory_cookbook.ipynb) - Practical examples of implementing memory patterns