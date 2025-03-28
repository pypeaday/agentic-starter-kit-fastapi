from fastapi import APIRouter, Depends, HTTPException, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime
import json

from . import models, auth
from .roles import requires_permission
from .auth import get_password_hash
from .database import get_db


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
)


def get_templates(request: Request):
    """Get templates from app state."""
    return request.app.state.templates


@router.get("/dashboard", response_class=HTMLResponse)
@requires_permission("view_system")
async def admin_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    """Admin dashboard showing system statistics and management options."""
    # Get user count
    user_count = db.query(models.User).count()

    # Get recent users
    recent_users = (
        db.query(models.User).order_by(models.User.created_at.desc()).limit(5).all()
    )

    templates = get_templates(request)
    return templates.TemplateResponse(
        "admin/dashboard.html",
        {
            "request": request,
            "current_user": current_user,
            "user": current_user,  # Add this for the base template
            "user_count": user_count,
            "recent_users": recent_users,
        },
    )


@router.get("/users", response_class=HTMLResponse)
@requires_permission("view_users")
async def list_users(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    """List all users in the system."""
    users = db.query(models.User).all()
    templates = get_templates(request)
    return templates.TemplateResponse(
        "admin/users.html",
        {
            "request": request,
            "current_user": current_user,
            "user": current_user,  # Add this for the base template
            "users": users,
        },
    )


@router.get("/users/new", response_class=HTMLResponse)
@requires_permission("manage_users")
async def new_user_form(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    """Show form to create a new user."""
    roles = db.query(models.Role).all()
    templates = get_templates(request)
    return templates.TemplateResponse(
        "admin/user_form.html",
        {
            "request": request,
            "current_user": current_user,
            "user": None,
            "roles": roles,
            "is_new": True,
        },
    )


@router.get("/users/{user_id}/edit", response_class=HTMLResponse)
@requires_permission("manage_users")
async def edit_user_form(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    """Show form to edit a user."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    roles = db.query(models.Role).all()
    templates = get_templates(request)
    return templates.TemplateResponse(
        "admin/user_form.html",
        {
            "request": request,
            "current_user": current_user,
            "user": user,
            "roles": roles,
            "is_new": False,
        },
    )


@router.post("/users")
@requires_permission("manage_users")
async def create_user(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
    email: str = Form(...),
    password: str = Form(...),
    name: str = Form(None),
    role: str = Form("user"),
    is_active: bool = Form(True),
):
    """Create a new user."""
    # Check if email already exists
    if db.query(models.User).filter(models.User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Validate role exists
    if not db.query(models.Role).filter(models.Role.name == role).first():
        raise HTTPException(status_code=400, detail="Invalid role")

    # Create user
    user = models.User(
        email=email,
        name=name,
        hashed_password=get_password_hash(password),
        role=role,
        is_active=is_active,
        created_at=datetime.utcnow(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return RedirectResponse(
        url="/admin/users",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.put("/users/{user_id}")
@requires_permission("manage_users")
async def update_user(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
    email: str = Form(...),
    name: str = Form(None),
    role: str = Form("user"),
    is_active: bool = Form(True),
):
    """Update a user's information."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Don't allow admins to modify themselves
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot modify your own account")

    # Check if email is taken by another user
    existing_user = (
        db.query(models.User)
        .filter(models.User.email == email, models.User.id != user_id)
        .first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already taken")

    # Validate role exists
    if not db.query(models.Role).filter(models.Role.name == role).first():
        raise HTTPException(status_code=400, detail="Invalid role")

    # Update user
    user.email = email
    user.name = name
    user.role = role
    user.is_active = is_active
    db.commit()

    return RedirectResponse(
        url="/admin/users",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.post("/users/{user_id}/reset-password")
@requires_permission("manage_users")
async def reset_user_password(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    """Reset a user's password to a random string."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Don't allow admins to reset their own password
    if user.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Cannot reset your own password. Use the profile page instead.",
        )

    # Generate random password
    import secrets
    import string

    alphabet = string.ascii_letters + string.digits
    password = "".join(secrets.choice(alphabet) for _ in range(12))

    # Update password
    user.hashed_password = get_password_hash(password)
    db.commit()

    return {"success": True, "password": password}


@router.get("/roles", response_class=HTMLResponse)
@requires_permission("view_roles")
async def list_roles(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    """List all roles."""
    roles = db.query(models.Role).all()
    templates = get_templates(request)
    return templates.TemplateResponse(
        "admin/roles.html",
        {
            "request": request,
            "current_user": current_user,
            "user": current_user,
            "roles": roles,
        },
    )


@router.post("/roles")
@requires_permission("manage_roles")
async def create_role(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
    name: str = Form(...),
    description: str = Form(None),
    permissions: str = Form("{}"),  # JSON string of permissions
):
    """Create a new role."""
    # Validate name is unique
    if db.query(models.Role).filter(models.Role.name == name).first():
        raise HTTPException(status_code=400, detail="Role name already exists")

    # Validate permissions JSON
    try:
        json.loads(permissions)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid permissions format")

    role = models.Role(
        name=name,
        description=description,
        permissions=permissions,
        created_at=datetime.utcnow(),
    )
    db.add(role)
    db.commit()

    return RedirectResponse(
        url="/admin/roles",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.put("/roles/{role_id}")
@requires_permission("manage_roles")
async def update_role(
    request: Request,
    role_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
    name: str = Form(...),
    description: str = Form(None),
    permissions: str = Form("{}"),
):
    """Update a role."""
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # Check if new name is taken by another role
    existing_role = (
        db.query(models.Role)
        .filter(models.Role.name == name, models.Role.id != role_id)
        .first()
    )
    if existing_role:
        raise HTTPException(status_code=400, detail="Role name already taken")

    # Validate permissions JSON
    try:
        json.loads(permissions)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid permissions format")

    role.name = name
    role.description = description
    role.permissions = permissions
    db.commit()

    return RedirectResponse(
        url="/admin/roles",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.delete("/roles/{role_id}")
@requires_permission("manage_roles")
async def delete_role(
    request: Request,
    role_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    """Delete a role."""
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # Don't allow deleting roles that are in use
    if db.query(models.User).filter(models.User.role == role.name).first():
        raise HTTPException(
            status_code=400, detail="Cannot delete role that is assigned to users"
        )

    db.delete(role)
    db.commit()

    return {"success": True}
