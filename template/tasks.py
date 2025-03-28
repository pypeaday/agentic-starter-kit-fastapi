import secrets
import shutil
from pathlib import Path


def post_generation(answers):
    """
    Post-generation script to handle conditional features and cleanup.
    This script runs after the template is copied but before the virtual environment is created.
    """
    project_dir = Path.cwd()

    # Update the database URL in .env file
    env_file = project_dir / ".env"
    env_example = project_dir / ".env.example"

    if env_example.exists():
        shutil.copy(env_example, env_file)

    # Generate a random JWT secret key
    jwt_secret = secrets.token_urlsafe(32)

    # Update the .env file with the JWT secret and other settings
    env_content = []
    with open(env_file, "r") as f:
        for line in f:
            if line.startswith("JWT_SECRET_KEY="):
                line = f"JWT_SECRET_KEY={jwt_secret}\n"
            elif line.startswith("DATABASE_URL="):
                line = f"DATABASE_URL={answers['database_url']}\n"
            elif line.startswith("ADMIN_EMAIL="):
                line = f"ADMIN_EMAIL={answers['admin_email']}\n"
            elif line.startswith("ADMIN_PASSWORD="):
                line = f"ADMIN_PASSWORD={answers['admin_password']}\n"
            elif line.startswith("HOST="):
                line = f"HOST={answers['host']}\n"
            elif line.startswith("PORT="):
                line = f"PORT={answers['port']}\n"
            elif line.startswith("ENVIRONMENT="):
                line = f"ENVIRONMENT={answers['environment']}\n"
            env_content.append(line)

    with open(env_file, "w") as f:
        f.writelines(env_content)

    # Create data directory if it doesn't exist
    data_dir = project_dir / "data"
    data_dir.mkdir(exist_ok=True)

    # Create an empty .gitkeep file in the data directory
    (data_dir / ".gitkeep").touch()

    print("\nTemplate setup completed successfully!")
    print(f"\nProject '{answers['project_name']}' has been created.")
    print("\nNext steps:")
    print("1. Create and activate a virtual environment:")
    print("   python -m venv venv")
    print("   source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
    print("\n2. Install dependencies:")
    print("   pip install -r requirements.txt")
    print("\n3. Run the development server:")
    print("   uvicorn app.main:app --reload")
    print(
        f"\nVisit http://localhost:{answers['port']} to see your application running."
    )
