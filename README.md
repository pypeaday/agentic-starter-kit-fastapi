# FastAPI HTMX Starter Kit Template

A modern web application template that combines the power of FastAPI with the simplicity of HTMX. This template provides a solid foundation for building web applications with Python, featuring built-in authentication, SQLite database integration, and interactive UI components.

## Features

- **FastAPI Backend**: High-performance, easy-to-use web framework
- **HTMX Integration**: Modern, browser-native interactivity without complex JavaScript
- **SQLite Database**: Simple, file-based database with SQLAlchemy ORM
- **User Authentication**: Built-in email/password authentication with JWT tokens
- **Admin Interface** (Optional): Ready-to-use admin dashboard
- **Theme Support**: Dark/light theme switching with customizable colors
- **Interactive UI Components** (Optional): Pre-built HTMX-powered components (todo list, infinite scroll, etc.)
- **AI-Ready**: Includes agent context management for AI-assisted development

## Creating a New Project

### Prerequisites

- Python 3.12 or higher
- [Copier](https://copier.readthedocs.io/) 9.0 or higher

```bash
# Install Copier if you haven't already
pipx install copier
```

### Generate a New Project

```bash
# Create a new project
copier copy gh:pypeaday/agentic-starter-kit-python my-project
```

### Configuration Options

During project creation, you'll be prompted for various configuration options:

- **Project Name**: Your project's display name
- **Project Slug**: Python package name (auto-generated from project name)
- **Project Description**: Brief description of your project
- **Database URL**: SQLite database URL (default: sqlite:///./data/app.db)
- **Admin Email**: Default admin user email
- **Admin Password**: Default admin user password
- **Host**: Server host (default: 0.0.0.0)
- **Port**: Server port (default: 8000)
- **Environment**: Development or production mode
- **Optional Features**:
  - Admin Interface: Include admin dashboard and user management
  - Example Routes: Include todo list and other example components

## Development Workflow

After creating your project:

1. Install UV if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies (including development tools):
```bash
uv pip install -e ".[dev]"
```

4. Run the development server:
```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000` to see your application running.

## Project Structure

```
app/
├── __init__.py
├── main.py              # FastAPI application setup
├── database.py          # Database configuration
├── models.py            # SQLAlchemy models
├── auth.py             # Authentication logic
├── htmx.py            # HTMX utility functions
├── static/
│   └── css/
│       └── theme.css   # Theme styles
└── templates/
    ├── base.html       # Base template
    ├── index.html      # Home page
    ├── login.html      # Login page
    ├── register.html   # Registration page
    └── admin/          # (Optional) Admin interface
        └── dashboard.html

agent/                  # AI agent context management
├── context/           # Core project context (immutable)
│   ├── architecture.md    # System architecture and patterns
│   ├── constraints.md     # Project constraints and limitations
│   ├── goals.md          # Project objectives and success criteria
│   └── standards/        # Development standards and practices
├── memory/            # Persistent knowledge (append-only)
│   ├── decisions/        # Key technical decisions and rationales
│   ├── progress/         # Development progress and milestones
│   └── learnings/        # Insights and lessons learned
└── workspace/         # Active development (mutable)
    ├── current/          # Current task context and state
    ├── planning/         # Task breakdown and implementation plans
    └── validation/       # Testing and verification criteria
```

## Updating Your Project

To update your project with the latest template changes:

```bash
cd my-project
copier update
```

## Releases

This project uses semantic-release for automated versioning and releases. When changes are pushed to the main branch, the release workflow:

1. Runs all tests to ensure quality
2. Analyzes commit messages to determine the version bump
3. Creates a new GitHub release with automatically generated release notes

To trigger a release, simply push your changes to the main branch with conventional commit messages:

- `feat: new feature` - Minor version bump
- `fix: bug fix` - Patch version bump
- `BREAKING CHANGE: major change` - Major version bump

The release process is fully automated - no manual version updates or tag creation needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
