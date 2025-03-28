from fastapi import status
import json


def test_admin_dashboard_access(client, admin_headers):
    """Test admin can access dashboard."""
    response = client.get("/admin/dashboard", headers=admin_headers)
    # serialize response to json file

    assert response.status_code == status.HTTP_200_OK
    assert "Admin Dashboard" in response.text


def test_non_admin_dashboard_access(client, user_headers):
    """Test regular user cannot access dashboard."""
    response = client.get("/admin/dashboard", headers=user_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_moderator_dashboard_access(client, moderator_headers):
    """Test moderator can access dashboard."""
    response = client.get("/admin/dashboard", headers=moderator_headers)
    assert response.status_code == status.HTTP_200_OK


def test_list_users_admin(client, admin_headers, regular_user):
    """Test admin can list users."""
    response = client.get("/admin/users", headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK
    assert regular_user.email in response.text


def test_list_users_moderator(client, moderator_headers, regular_user):
    """Test moderator can list users."""
    response = client.get("/admin/users", headers=moderator_headers)
    assert response.status_code == status.HTTP_200_OK
    assert regular_user.email in response.text


def test_list_users_unauthorized(client, user_headers):
    """Test regular user cannot list users."""
    response = client.get("/admin/users", headers=user_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_user_admin(client, admin_headers, db):
    """Test admin can create new user."""
    headers = {**admin_headers, "Content-Type": "application/x-www-form-urlencoded"}
    response = client.post(
        "/admin/users",
        headers=headers,
        data={
            "email": "newuser@example.com",
            "password": "testpass123",
            "name": "New User",
            "role": "user",
            "is_active": "true",
        },
    )
    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert response.headers["location"] == "/admin/users"

    # Verify user was created
    response = client.get("/admin/users", headers=admin_headers)
    assert "newuser@example.com" in response.text


def test_create_user_moderator(client, moderator_headers, db):
    """Test moderator can create new user."""
    headers = {**moderator_headers, "Content-Type": "application/x-www-form-urlencoded"}
    response = client.post(
        "/admin/users",
        headers=headers,
        data={
            "email": "newuser@example.com",
            "password": "testpass123",
            "name": "New User",
            "role": "user",
            "is_active": "true",
        },
    )
    assert response.status_code == status.HTTP_303_SEE_OTHER


def test_create_user_unauthorized(client, user_headers):
    """Test regular user cannot create new user."""
    headers = {**user_headers, "Content-Type": "application/x-www-form-urlencoded"}
    response = client.post(
        "/admin/users",
        headers=headers,
        data={
            "email": "newuser@example.com",
            "password": "testpass123",
            "name": "New User",
            "role": "user",
            "is_active": "true",
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_user_admin(client, admin_headers, regular_user):
    """Test admin can update user."""
    headers = {**admin_headers, "Content-Type": "application/x-www-form-urlencoded"}
    response = client.put(
        f"/admin/users/{regular_user.id}",
        headers=headers,
        data={
            "email": "updated@example.com",
            "name": "Updated User",
            "role": "user",
            "is_active": "true",
        },
    )
    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert response.headers["location"] == "/admin/users"


def test_admin_cannot_modify_self(client, admin_headers, admin_user):
    """Test admin cannot modify their own account."""
    headers = {**admin_headers, "Content-Type": "application/x-www-form-urlencoded"}
    response = client.put(
        f"/admin/users/{admin_user.id}",
        headers=headers,
        data={
            "email": "updated@example.com",
            "name": "Updated Admin",
            "role": "user",  # Trying to downgrade own role
            "is_active": "true",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_reset_user_password(client, admin_headers, regular_user):
    """Test admin can reset user password."""
    response = client.post(
        f"/admin/users/{regular_user.id}/reset-password",
        headers=admin_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "password" in data
    assert data["success"] is True


def test_admin_cannot_reset_own_password(client, admin_headers, admin_user):
    """Test admin cannot reset their own password through admin interface."""
    response = client.post(
        f"/admin/users/{admin_user.id}/reset-password",
        headers=admin_headers,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_list_roles_admin(client, admin_headers):
    """Test admin can list roles."""
    response = client.get("/admin/roles", headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK
    assert "admin" in response.text
    assert "user" in response.text
    assert "moderator" in response.text


def test_list_roles_moderator(client, moderator_headers):
    """Test moderator can view roles but not manage them."""
    response = client.get("/admin/roles", headers=moderator_headers)
    assert response.status_code == status.HTTP_200_OK


def test_create_role_admin(client, admin_headers):
    """Test admin can create new role."""
    permissions = {
        "view_users": True,
        "manage_users": False,
        "view_roles": True,
        "manage_roles": False,
        "view_system": True,
        "manage_system": False,
    }
    headers = {**admin_headers, "Content-Type": "application/x-www-form-urlencoded"}
    response = client.post(
        "/admin/roles",
        headers=headers,
        data={
            "name": "viewer",
            "description": "Can only view",
            "permissions": json.dumps(permissions),
        },
    )
    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert response.headers["location"] == "/admin/roles"


def test_create_role_unauthorized(client, moderator_headers):
    """Test moderator cannot create new role."""
    permissions = {
        "view_users": True,
        "manage_users": False,
    }
    headers = {**moderator_headers, "Content-Type": "application/x-www-form-urlencoded"}
    response = client.post(
        "/admin/roles",
        headers=headers,
        data={
            "name": "viewer",
            "description": "Can only view",
            "permissions": json.dumps(permissions),
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_role_admin(client, admin_headers, db):
    """Test admin can update role."""
    # First create a role
    permissions = {"view_users": True}
    headers = {**admin_headers, "Content-Type": "application/x-www-form-urlencoded"}
    response = client.post(
        "/admin/roles",
        headers=headers,
        data={
            "name": "test_role",
            "description": "Test role",
            "permissions": json.dumps(permissions),
        },
    )

    # Get the role ID
    response = client.get("/admin/roles", headers=admin_headers)
    assert "test_role" in response.text

    # Update the role
    new_permissions = {"view_users": False}
    response = client.put(
        "/admin/roles/4",  # Assuming ID 4 for the new role after admin, user, moderator
        headers=headers,  # Reuse the headers with content type
        data={
            "name": "test_role_updated",
            "description": "Updated test role",
            "permissions": json.dumps(new_permissions),
        },
    )
    assert response.status_code == status.HTTP_303_SEE_OTHER


def test_delete_role_admin(client, admin_headers, db):
    """Test admin can delete unused role."""
    # First create a role
    permissions = {"view_users": True}
    headers = {**admin_headers, "Content-Type": "application/x-www-form-urlencoded"}
    response = client.post(
        "/admin/roles",
        headers=headers,
        data={
            "name": "test_role",
            "description": "Test role",
            "permissions": json.dumps(permissions),
        },
    )

    # Delete the role
    response = client.delete(
        "/admin/roles/4",  # Assuming ID 4 for the new role
        headers=admin_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True


def test_delete_role_in_use(client, admin_headers, regular_user):
    """Test cannot delete role that is assigned to users."""
    response = client.delete(
        "/admin/roles/2",  # ID for 'user' role
        headers=admin_headers,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
