import re
import secrets
import string


def generate_secret_key(length: int = 64) -> str:
    """Generate a secure secret key."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return "".join(secrets.choice(alphabet) for _ in range(length))


def normalize_package_name(name: str) -> str:
    """
    Normalize a string to be a valid Python package name.
    - Convert to lowercase
    - Replace spaces and hyphens with underscores
    - Remove any characters that aren't alphanumeric or underscore
    - Ensure it starts with a letter and ends with alphanumeric
    """
    # Convert to lowercase and replace spaces/hyphens with underscores
    name = name.lower().replace(" ", "_").replace("-", "_")

    # Remove any characters that aren't alphanumeric or underscore
    name = re.sub(r"[^\w]", "", name)

    # Ensure it starts with a letter
    name = re.sub(r"^[^a-zA-Z]+", "", name)

    # If empty after cleaning, use a default name
    if not name:
        name = "fastapi_project"

    return name


def validate_project_name(answers: dict) -> dict:
    """
    Validate and normalize the project name and slug.
    This function runs before the template is copied.
    """
    # Normalize the project slug for Python package naming
    answers["project_slug"] = normalize_package_name(answers["project_slug"])

    # Ensure the project name is a valid string
    if (
        not isinstance(answers["project_name"], str)
        or not answers["project_name"].strip()
    ):
        answers["project_name"] = "FastAPI Project"

    # Ensure description is a valid string
    if (
        not isinstance(answers["project_description"], str)
        or not answers["project_description"].strip()
    ):
        answers["project_description"] = (
            "A modern web application built with FastAPI and HTMX"
        )

    # Validate port number
    try:
        port = int(answers["port"])
        if port < 1 or port > 65535:
            answers["port"] = 8000
    except (ValueError, TypeError):
        answers["port"] = 8000

    # Validate environment
    if answers["environment"] not in ["development", "production"]:
        answers["environment"] = "development"

    # Ensure database URL is valid
    if not answers["database_url"].startswith("sqlite:///"):
        answers["database_url"] = "sqlite:///./data/app.db"

    # Validate admin email
    email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    if not email_pattern.match(answers["admin_email"]):
        answers["admin_email"] = "admin@example.com"

    # Ensure admin password meets minimum requirements
    if len(str(answers["admin_password"])) < 8:
        answers["admin_password"] = "admin123"  # Default password for development

    # Validate host
    if not answers["host"]:
        answers["host"] = "0.0.0.0"

    return answers


def pre_copy(answers: dict) -> dict:
    """
    Main entry point for pre-copy validation and normalization.
    """
    answers = validate_project_name(answers)

    # Generate a secure JWT secret key
    answers["jwt_secret_key"] = generate_secret_key(64)

    return answers
