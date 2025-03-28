# User Instructions

Welcome to the Agentic Starter Kit.

The idea behind this repo is to give developers working with tools like
Windsurf or Cline a way to manage context and keep models/agents on the right
track.

## Project Structure

The agent workspace is organized into three main areas:

1. `agent/context/` - Core project context (immutable)
   - architecture.md - System architecture and patterns
   - constraints.md - Project constraints and limitations
   - goals.md - Project objectives and success criteria
   - standards/ - Development standards and practices

2. `agent/memory/` - Persistent knowledge (append-only)
   - decisions/ - Key technical decisions and rationales
   - progress/ - Development progress and milestones
   - learnings/ - Insights and lessons learned

3. `agent/workspace/` - Active development (mutable)
   - current/ - Current task context and state
   - planning/ - Task breakdown and implementation plans
   - validation/ - Testing and verification criteria

## Setup

1. Start with ChatGPT (or yourself) to flesh out your project's goals and constraints.
   Document these in `agent/context/goals.md` and `agent/context/constraints.md`

2. Review and customize the architecture patterns in `agent/context/architecture.md`

3. Familiarize yourself with the coding and documentation standards in
   `agent/context/standards/`

## Development

1. I like to manage python and environments myself with `uv` - so make a new repo,
   then `uv init` and either make a `requirements.txt` file or start using `uv add`
   to add requirements.

2. I also typically manage docker myself without letting the Agent run docker
   commands - this repo comes with a dockerfile, compose file, and entrypoint
   script to serve as fodder for the docker setup

## Working with Agents

1. Agents should always start by reviewing relevant files in `/context`
2. Development decisions and progress are tracked in `/memory`
3. Active work happens in `/workspace`
4. Each directory contains an index.md file explaining its specific purpose
