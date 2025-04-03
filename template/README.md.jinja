# {{ project_name }}

{{ project_description }}

This project was generated from the [FastAPI HTMX Starter Kit]({{ repository_url }}) template, which provides a solid foundation for building web applications with Python, featuring built-in authentication, SQLite database integration, and interactive UI components.

## Features

- **FastAPI Backend**: High-performance, easy-to-use web framework
- **HTMX Integration**: Modern, browser-native interactivity without complex JavaScript
- **SQLite Database**: Simple, file-based database with SQLAlchemy ORM
- **User Authentication**: Built-in email/password authentication with JWT tokens
{% if include_admin_interface %}
- **Admin Interface**: Ready-to-use admin dashboard
{% endif %}
- **Theme Support**: Dark/light theme switching with customizable colors
{% if include_example_routes %}
- **Interactive UI Components**: Pre-built HTMX-powered components (todo list, infinite scroll, etc.)
{% endif %}

## Quick Start

0. Install UV:
```bash
# On macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows:
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

1. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
# Install all dependencies (including development tools):
uv pip install -e ".[dev]"

# Or for production dependencies only:
uv pip install -e "."
```

3. Copy the example environment file and configure it:
```bash
cp .env.example .env
```

4. Run the development server:
```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:{{ port }}` to see your application running.

## Environment Variables

Configure these variables in your `.env` file:

- `DATABASE_URL`: SQLite database URL (default: {{ database_url }})
- `JWT_SECRET_KEY`: Secret key for JWT token generation
- `ADMIN_EMAIL`: Default admin user email (default: {{ admin_email }})
- `ADMIN_PASSWORD`: Default admin user password (change in production!)
- `HOST`: Server host (default: {{ host }})
- `PORT`: Server port (default: {{ port }})
- `ENVIRONMENT`: Development or production mode

## Project Structure

```
.
├── app/                  # Application source code
│   ├── __init__.py
│   ├── main.py          # FastAPI application setup
│   ├── database.py      # Database configuration
│   ├── models.py        # SQLAlchemy models
│   ├── auth.py         # Authentication logic
│   ├── htmx.py        # HTMX utility functions
│   ├── static/
│   │   └── css/
│   │       └── theme.css # Theme styles
│   └── templates/
│       ├── base.html    # Base template
│       ├── index.html   # Home page
│       ├── login.html   # Login page
│       ├── register.html # Registration page
│       {% if include_admin_interface %}└── admin/
│           └── dashboard.html # Admin dashboard{% endif %}
│
└── agent/               # AI agent workspace
    ├── context/        # Core project context (immutable)
    │   ├── architecture.md
    │   ├── constraints.md
    │   ├── goals.md
    │   └── standards/
    ├── memory/         # Persistent knowledge (append-only)
    │   ├── decisions/
    │   ├── progress/
    │   └── learnings/
    └── workspace/      # Active development (mutable)
        ├── current/
        ├── planning/
        └── validation/
```

## Authentication

The application includes a complete authentication system:

- User registration with email/password
- JWT token-based authentication
- Remember me functionality
- Role-based authorization (user/admin)
- Automatic admin user creation

## HTMX Features

The application demonstrates various HTMX capabilities:

- Dynamic content loading
- Form submissions without page reloads
- Infinite scroll
- Active search
- Toast notifications
- Theme switching

## Development

### Adding New Routes

1. Create a new route file in the `app` directory
2. Define your routes using FastAPI's router
3. Include the router in `main.py`

Example:
```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/my-route")
def my_route():
    return {"message": "Hello"}
```

### Database Migrations

The project uses SQLAlchemy for database management. To make changes to the database schema:

1. Modify the models in `models.py`
2. The changes will be automatically applied on next startup

### Theme Customization

1. Add new themes in `app/themes.py`
2. Update theme CSS variables in `static/css/theme.css`
3. Use theme classes in your templates

## Production Deployment

Before deploying to production:

1. Set a secure `JWT_SECRET_KEY`
2. Change default admin credentials
3. Set `ENVIRONMENT=production`
4. Configure proper CORS settings
5. Enable HTTPS
6. Set appropriate cookie security flags

## License

This project is licensed under the MIT License - see the LICENSE file for details.
