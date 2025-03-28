from fastapi import status
import json
from app.roles import has_permission


def test_default_roles_exist(db):
    """Test that default roles are created in the database."""
    from app.models import Role

    roles = db.query(Role).all()
    role_names = {role.name for role in roles}

    assert "admin" in role_names
    assert "user" in role_names
    assert "moderator" in role_names


def test_admin_permissions(admin_user):
    """Test that admin has all permissions."""
    permissions = [
        "view_users",
        "manage_users",
        "view_roles",
        "manage_roles",
        "view_system",
        "manage_system",
    ]

    for permission in permissions:
        assert has_permission(admin_user, permission) is True


def test_user_permissions(regular_user):
    """Test that regular user has no admin permissions."""
    permissions = [
        "view_users",
        "manage_users",
        "view_roles",
        "manage_roles",
        "view_system",
        "manage_system",
    ]

    for permission in permissions:
        assert has_permission(regular_user, permission) is False


def test_moderator_permissions(moderator_user):
    """Test that moderator has correct permissions."""
    # Should have these permissions
    assert has_permission(moderator_user, "view_users") is True
    assert has_permission(moderator_user, "manage_users") is True
    assert has_permission(moderator_user, "view_roles") is True
    assert has_permission(moderator_user, "view_system") is True

    # Should not have these permissions
    assert has_permission(moderator_user, "manage_roles") is False
    assert has_permission(moderator_user, "manage_system") is False


def test_inactive_user_permissions(inactive_user):
    """Test that inactive user has no permissions."""
    permissions = [
        "view_users",
        "manage_users",
        "view_roles",
        "manage_roles",
        "view_system",
        "manage_system",
    ]

    for permission in permissions:
        assert has_permission(inactive_user, permission) is False


def test_permission_decorator_admin(client, admin_headers):
    """Test permission decorator with admin user."""
    # Test various protected endpoints
    endpoints = [
        ("/admin/dashboard", status.HTTP_200_OK),  # requires view_system
        ("/admin/users", status.HTTP_200_OK),  # requires view_users
        ("/admin/roles", status.HTTP_200_OK),  # requires view_roles
    ]

    for endpoint, expected_status in endpoints:
        response = client.get(endpoint, headers=admin_headers)
        assert response.status_code == expected_status


def test_permission_decorator_moderator(client, moderator_headers):
    """Test permission decorator with moderator user."""
    # Test endpoints moderator should have access to
    allowed_endpoints = [
        "/admin/dashboard",  # view_system
        "/admin/users",  # view_users
    ]
    for endpoint in allowed_endpoints:
        response = client.get(endpoint, headers=moderator_headers)
        assert response.status_code == status.HTTP_200_OK

    # Test endpoint moderator should not have access to
    response = client.post(
        "/admin/roles",
        headers=moderator_headers,
        data={
            "name": "test_role",
            "description": "Test role",
            "permissions": "{}",
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_permission_decorator_user(client, user_headers):
    """Test permission decorator with regular user."""
    endpoints = [
        "/admin/dashboard",
        "/admin/users",
        "/admin/roles",
    ]

    for endpoint in endpoints:
        response = client.get(endpoint, headers=user_headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN


def test_custom_role_permissions(client, admin_headers, db):
    """Test creating and using custom role with specific permissions."""
    # Create a custom role with specific permissions
    permissions = {
        "view_users": True,
        "manage_users": False,
        "view_roles": True,
        "manage_roles": False,
        "view_system": True,
        "manage_system": False,
    }

    response = client.post(
        "/admin/roles",
        headers=admin_headers,
        data={
            "name": "custom_role",
            "description": "Custom role with specific permissions",
            "permissions": json.dumps(permissions),
        },
    )
    assert response.status_code == status.HTTP_303_SEE_OTHER

    # Create a user with the custom role
    response = client.post(
        "/admin/users",
        headers=admin_headers,
        data={
            "email": "custom@example.com",
            "password": "testpass123",
            "name": "Custom User",
            "role": "custom_role",
            "is_active": "true",
        },
    )
    assert response.status_code == status.HTTP_303_SEE_OTHER

    # Login as the custom role user
    response = client.post(
        "/token",
        data={
            "username": "custom@example.com",
            "password": "testpass123",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["access_token"]
    custom_headers = {"Authorization": f"Bearer {token}"}

    # Test permissions
    # Should have access to view endpoints
    response = client.get("/admin/users", headers=custom_headers)
    assert response.status_code == status.HTTP_200_OK

    # Should not have access to manage endpoints
    response = client.post(
        "/admin/users",
        headers=custom_headers,
        data={
            "email": "another@example.com",
            "password": "testpass123",
            "name": "Another User",
            "role": "user",
            "is_active": "true",
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_invalid_role_permissions(db):
    """Test handling of invalid role permissions JSON."""
    from app.models import Role, User
    from datetime import datetime

    # Create role with invalid JSON
    role = Role(
        name="invalid_role",
        description="Invalid role",
        permissions="invalid json",
        created_at=datetime.utcnow(),
    )
    db.add(role)
    db.commit()

    # Create user with invalid role
    user = User(
        email="invalid@example.com",
        hashed_password="dummy",
        role="invalid_role",
        is_active=True,
        created_at=datetime.utcnow(),
    )
    db.add(user)
    db.commit()

    # Test permissions (should all be False due to invalid JSON)
    assert has_permission(user, "view_users") is False
    assert has_permission(user, "manage_users") is False


def test_nonexistent_permission(admin_user):
    """Test checking for a permission that doesn't exist."""
    assert has_permission(admin_user, "nonexistent_permission") is False
