---
title: "Fresh Eyes Pattern"
sidebar_position: 16
---

# Fresh Eyes Pattern

After AI-assisted development, use a separate agent with its own context window and system prompt to review your work. This "fresh eyes" approach helps catch hallucinations, improves quality, and provides focused analysis from an unbiased perspective.

## The Core Pattern

When building with AI assistance, use a two-stage approach:

1. **Creation Stage**: Primary agent focuses on implementation
2. **Review Stage**: Separate agent with fresh context reviews the output

This separation creates a **double-check mechanism** where a new perspective can identify issues that might be missed during creation.

## Why This Pattern Works

**Separate Context Window**: The review agent starts with a clean slate, without the assumptions and decisions from the creation phase.

**Dedicated System Prompt**: A specialized prompt focuses the agent on specific quality dimensions (security, standards, architecture) rather than building solutions.

**Reduces Hallucinations**: A fresh agent with separate context is less likely to inherit or reinforce errors from the creation phase.

**Unbiased Analysis**: The review agent isn't anchored by implementation decisions made during creation.

## Examples

### Security Review
Review security-sensitive code with focused attention.

**Example:**
```
Review the authentication implementation for security vulnerabilities,
including injection flaws, token handling issues, and authorization gaps.
```

### Architecture Review
Validate alignment with design principles and patterns.

**Example:**
```
Analyze the new microservice architecture for proper separation of concerns,
scalability considerations, and adherence to our architectural guidelines.
```

### Breaking Change Detection
Identify changes that could break existing integrations.

**Example:**
```
Examine the API changes to find breaking changes that could affect existing
clients, including signature modifications and removed endpoints.
```

### Code Quality Review
Assess maintainability, best practices, and technical debt.

**Example:**
```
Review the payment processing module for code smells, maintainability issues,
and adherence to clean code principles.
```

### Standards Compliance
Validate against project-specific conventions.

**Example:**
```
Check the TypeScript code against our coding standards, including naming
conventions, type usage, and project structure guidelines.
```

