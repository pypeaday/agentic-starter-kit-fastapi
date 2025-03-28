import json
from typing import Any, Dict
from fastapi.templating import Jinja2Templates


def fromjson(value: str) -> Dict[str, Any]:
    """Convert a JSON string to a Python dictionary."""
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return {}


def register_filters(templates: Jinja2Templates) -> None:
    """Register all custom filters with a Jinja2Templates instance."""
    templates.env.filters["fromjson"] = fromjson
