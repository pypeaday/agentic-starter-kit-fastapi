import pytest
from fastapi.testclient import TestClient
from fastapi import Request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime

from fastapi.templating import Jinja2Templates
from app.main import app
from app.database import get_db
from app.models import Base, User  # Import Base from models and all models
from app.auth import create_access_token, get_password_hash
from app.roles import ensure_default_roles_exist
from app.jinja_filters import register_filters

# Create and configure test-specific templates
test_templates = Jinja2Templates(directory="app/templates")
register_filters(test_templates)

# Override the templates in the app for testing
app.state.templates = test_templates

# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    # Create default roles using the helper function
    ensure_default_roles_exist(db)

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def override_get_db():
    """Override the database dependency for testing."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


async def get_test_request():
    """Override the request dependency for testing."""
    return Request(
        scope={
            "type": "http",
            "method": "GET",
            "path": "/",
            "headers": [],
        }
    )


# Override the Request dependency
app.dependency_overrides[Request] = get_test_request


class CustomTestClient(TestClient):
    def request(self, method, url, **kwargs):
        # Disable following redirects
        kwargs["follow_redirects"] = False

        # Create a mock Request object
        mock_request = Request(
            scope={
                "type": "http",
                "method": method,
                "path": url.split("?")[0],
                "query_string": url.split("?")[1].encode() if "?" in url else b"",
                "headers": [],
            }
        )

        # Add the mock request and templates to app state
        app.state.request = mock_request
        app.state.templates = test_templates
        return super().request(method, url, **kwargs)


@pytest.fixture(scope="function")
def client():
    """Create a test client."""
    return CustomTestClient(app)


@pytest.fixture
def test_password():
    """Return a test password."""
    return "testpassword123"


@pytest.fixture
def admin_user(db, test_password):
    """Create an admin user."""
    user = User(
        email="admin@example.com",
        hashed_password=get_password_hash(test_password),
        role="admin",
        is_active=True,
        created_at=datetime.utcnow(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def regular_user(db, test_password):
    """Create a regular user."""
    user = User(
        email="user@example.com",
        hashed_password=get_password_hash(test_password),
        role="user",
        is_active=True,
        created_at=datetime.utcnow(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def moderator_user(db, test_password):
    """Create a moderator user."""
    user = User(
        email="moderator@example.com",
        hashed_password=get_password_hash(test_password),
        role="moderator",
        is_active=True,
        created_at=datetime.utcnow(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def inactive_user(db, test_password):
    """Create an inactive user."""
    user = User(
        email="inactive@example.com",
        hashed_password=get_password_hash(test_password),
        role="user",
        is_active=False,
        created_at=datetime.utcnow(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def admin_token(admin_user):
    """Create an access token for admin user."""
    return create_access_token(data={"sub": admin_user.email})


@pytest.fixture
def user_token(regular_user):
    """Create an access token for regular user."""
    return create_access_token(data={"sub": regular_user.email})


@pytest.fixture
def moderator_token(moderator_user):
    """Create an access token for moderator user."""
    return create_access_token(data={"sub": moderator_user.email})


@pytest.fixture
def inactive_token(inactive_user):
    """Create an access token for inactive user."""
    return create_access_token(data={"sub": inactive_user.email})


@pytest.fixture
def admin_headers(admin_token):
    """Headers with admin token."""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def user_headers(user_token):
    """Headers with user token."""
    return {"Authorization": f"Bearer {user_token}"}


@pytest.fixture
def moderator_headers(moderator_token):
    """Headers with moderator token."""
    return {"Authorization": f"Bearer {moderator_token}"}


@pytest.fixture
def inactive_headers(inactive_token):
    """Headers with inactive user token."""
    return {"Authorization": f"Bearer {inactive_token}"}
