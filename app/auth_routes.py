from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from . import database, models, schemas, auth, themes

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def get_current_theme(request: Request) -> tuple[themes.ThemeColors, str]:
    """Get the current theme colors based on cookie or default"""
    theme_name = request.cookies.get("theme", "gruvbox-dark")
    theme = themes.get_theme(theme_name)
    if not theme:
        theme = themes.get_theme("gruvbox-dark")
        theme_name = "gruvbox-dark"
    return theme, theme_name


def set_theme_cookie(response: HTMLResponse, theme_name: str) -> None:
    """Set theme cookie with standard parameters"""
    response.set_cookie(
        key="theme",
        value=theme_name,
        max_age=31536000,  # 1 year
        httponly=False,  # Allow JavaScript to read the cookie
        samesite="lax",
        secure=False,  # Allow non-HTTPS for local development
    )


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    """API endpoint for obtaining a token."""
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Display registration page."""
    theme, current_theme = get_current_theme(request)
    response = templates.TemplateResponse(
        "register.html",
        {"request": request, "theme": theme, "current_theme": current_theme},
    )
    set_theme_cookie(response, current_theme)
    return response


@router.post("/register", response_class=HTMLResponse)
async def register_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(database.get_db),
):
    """Register a new user."""
    theme, current_theme = get_current_theme(request)

    # Validate inputs
    if password != confirm_password:
        response = templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "theme": theme,
                "current_theme": current_theme,
                "error": "Passwords do not match",
            },
        )
        set_theme_cookie(response, current_theme)
        return response

    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        response = templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "theme": theme,
                "current_theme": current_theme,
                "error": "Email already registered",
            },
        )
        set_theme_cookie(response, current_theme)
        return response

    # Create new user
    hashed_password = auth.get_password_hash(password)
    new_user = models.User(
        email=email,
        hashed_password=hashed_password,
        created_at=datetime.utcnow(),
        is_active=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create success response with toast notification
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.headers["HX-Trigger"] = (
        '{"showToast": {"message": "Registration successful! Please log in.", "type": "success"}}'
    )
    set_theme_cookie(response, current_theme)
    return response


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Display login page."""
    theme, current_theme = get_current_theme(request)
    response = templates.TemplateResponse(
        "login.html",
        {"request": request, "theme": theme, "current_theme": current_theme},
    )
    set_theme_cookie(response, current_theme)
    return response


@router.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    remember_me: Optional[str] = Form(None),
    db: Session = Depends(database.get_db),
):
    """Log in a user."""
    theme, current_theme = get_current_theme(request)

    # Authenticate user
    user = auth.authenticate_user(db, email, password)
    if not user:
        response = templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "theme": theme,
                "current_theme": current_theme,
                "error": "Invalid email or password",
            },
        )
        set_theme_cookie(response, current_theme)
        return response

    # Create access token with longer expiration if remember_me is checked
    if remember_me:
        # 30 days if remember me is checked
        access_token_expires = timedelta(days=30)
    else:
        # Default 30 minutes
        access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    # Create success response with token cookie
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    # Set cookie max_age to match token expiration
    max_age = 30 * 24 * 60 * 60 if remember_me else 1800  # 30 days or 30 minutes

    response.set_cookie(
        key="access_token",
        value=access_token,  # Store just the token, middleware will add 'Bearer'
        httponly=True,
        max_age=max_age,
        samesite="lax",
        secure=False,  # Set to True in production with HTTPS
    )
    response.headers["HX-Trigger"] = (
        '{"showToast": {"message": "Login successful!", "type": "success"}}'
    )
    set_theme_cookie(response, current_theme)
    return response


@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    """Log out a user."""
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="access_token")
    response.headers["HX-Trigger"] = (
        '{"showToast": {"message": "Logged out successfully", "type": "success"}}'
    )
    return response


# Create a dependency that will check for authenticated user
def user_dependency(
    token: str = Depends(auth.oauth2_scheme), db: Session = Depends(database.get_db)
):
    return auth.get_current_user_sync(token, db)


@router.get("/profile", response_class=HTMLResponse)
async def profile(
    request: Request,
    current_user: models.User = Depends(user_dependency),
    db: Session = Depends(database.get_db),
):
    """Display user profile."""
    theme, current_theme = get_current_theme(request)

    response = templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "theme": theme,
            "current_theme": current_theme,
            "user": current_user,
        },
    )
    set_theme_cookie(response, current_theme)
    return response
