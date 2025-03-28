# Agent Workspace

This directory serves as the primary workspace for AI agents collaborating on this project. It follows a clear three-part structure to optimize AI-human interaction and maintain clear context across development sessions.

## Directory Structure

```
agent/
├── context/                # Core project context (immutable)
│   ├── architecture.md    # System architecture and patterns
│   ├── constraints.md     # Project constraints and limitations
│   ├── goals.md          # Project objectives and success criteria
│   └── standards/        # Development standards and practices
│       ├── coding.md     # Coding standards and principles
│       └── docs.md       # Documentation guidelines
├── memory/                # Persistent knowledge (append-only)
│   ├── decisions/        # Key technical decisions and rationales
│   │   └── YYYY-MM-DD-title.md
│   ├── progress/         # Development progress and milestones
│   │   ├── checkpoints.md
│   │   └── YYYY-MM-DD-update.md
│   └── learnings/        # Insights and lessons learned
│       └── YYYY-MM-DD-topic.md
└── workspace/             # Active development (mutable)
    ├── current/          # Current task context and state
    │   ├── task.md       # Current task description and status
    │   └── notes.md      # Working notes and temporary content
    ├── planning/         # Task breakdown and implementation plans
    └── validation/       # Testing and verification criteria
```

## Core Principles

1. **Context First**
   - All agents must review relevant files in `/context` before starting work
   - Context files are immutable and define project boundaries
   - Standards in `/context/standards` guide all development

2. **Memory Management**
   - Decisions, progress, and learnings are tracked in `/memory`
   - All memory files are append-only
   - Use ISO date prefixes (YYYY-MM-DD) for all memory files
   - Checkpoints track major milestones

3. **Active Development**
   - All current work happens in `/workspace`
   - One task active at a time in `/workspace/current`
   - Plans and validation criteria stay with the task

## Documentation Rules

1. **Content Types**
   - Immutable: `<INSTRUCTION immutable>` sections cannot be modified
   - Append-only: `<LOG append>` sections for chronological updates
   - Task lists: Use `- [ ]` format for todos, `- [x]` for completed items

2. **File Management**
   - Keep files focused and single-purpose
   - Use clear, descriptive names
   - Follow consistent markdown formatting
   - Include creation date in memory files

## Usage Guidelines

1. Start each task by:
   - Reviewing relevant context
   - Creating or updating task.md in workspace/current
   - Breaking down implementation in planning/

2. During development:
   - Document decisions as they're made
   - Update progress regularly
   - Validate against requirements
   - Keep workspace clean

3. Complete each task by:
   - Documenting learnings
   - Creating a progress checkpoint
   - Cleaning the workspace