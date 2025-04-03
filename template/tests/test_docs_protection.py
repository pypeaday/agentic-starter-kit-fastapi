from fastapi import status


def test_docs_route_no_auth(client):
    """Test accessing /docs route without authentication."""
    response = client.get("/docs")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "Not authorized. Admin role required." in response.text


def test_redoc_route_no_auth(client):
    """Test accessing /redoc route without authentication."""
    response = client.get("/redoc")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "Not authorized. Admin role required." in response.text


def test_openapi_route_no_auth(client):
    """Test accessing /openapi.json route without authentication."""
    response = client.get("/openapi.json")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "Not authorized. Admin role required." in response.text


def test_docs_route_regular_user(client, user_headers):
    """Test accessing /docs route with regular user token."""
    # Set the cookie with the token
    client.cookies.set("access_token", user_headers["Authorization"].split(" ")[1])
    response = client.get("/docs")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "Not authorized. Admin role required." in response.text


def test_redoc_route_regular_user(client, user_headers):
    """Test accessing /redoc route with regular user token."""
    # Set the cookie with the token
    client.cookies.set("access_token", user_headers["Authorization"].split(" ")[1])
    response = client.get("/redoc")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "Not authorized. Admin role required." in response.text


def test_openapi_route_regular_user(client, user_headers):
    """Test accessing /openapi.json route with regular user token."""
    # Set the cookie with the token
    client.cookies.set("access_token", user_headers["Authorization"].split(" ")[1])
    response = client.get("/openapi.json")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "Not authorized. Admin role required." in response.text


def test_docs_route_admin_user(client, admin_headers):
    """Test accessing /docs route with admin token."""
    # Set the cookie with the token
    client.cookies.set("access_token", admin_headers["Authorization"].split(" ")[1])
    response = client.get("/docs")
    assert response.status_code == status.HTTP_200_OK


def test_redoc_route_admin_user(client, admin_headers):
    """Test accessing /redoc route with admin token."""
    # Set the cookie with the token
    client.cookies.set("access_token", admin_headers["Authorization"].split(" ")[1])
    response = client.get("/redoc")
    assert response.status_code == status.HTTP_200_OK


def test_openapi_route_admin_user(client, admin_headers):
    """Test accessing /openapi.json route with admin token."""
    # Set the cookie with the token
    client.cookies.set("access_token", admin_headers["Authorization"].split(" ")[1])
    response = client.get("/openapi.json")
    assert response.status_code == status.HTTP_200_OK
