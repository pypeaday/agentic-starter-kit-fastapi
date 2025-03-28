from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import models, database

# JWT configuration
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use environment variable for SECRET_KEY or fallback to a default for development
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev_secret_key_change_in_production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Hash a password for storing."""
    return pwd_context.hash(password)


def authenticate_user(db: Session, email: str, password: str):
    """Authenticate a user by email and password."""
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    if not user.is_active:
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_token_from_cookie(request: Request):
    """Extract token from cookie."""
    token = request.cookies.get("access_token")
    if not token:
        return None
    # Remove 'Bearer ' prefix if present
    if token.startswith("Bearer "):
        token = token[7:]
    return token


def get_optional_current_user_sync(token: str, db: Session):
    """Synchronous version of get_optional_current_user."""
    if not token:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        user = db.query(models.User).filter(models.User.email == email).first()
        return user
    except JWTError:
        return None


async def get_optional_current_user(
    request: Request = None, db: Session = Depends(database.get_db)
):
    """Get the current user from a JWT token in cookie, or None if not authenticated."""
    if not request:
        return None

    token = await get_token_from_cookie(request)
    if not token:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        user = db.query(models.User).filter(models.User.email == email).first()
        return user
    except JWTError:
        return None


def get_current_user_sync(token: str, db: Session):
    """Synchronous version of get_current_user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = db.query(models.User).filter(models.User.email == email).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):
    """Get the current user from a JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
):
    """Get the current active user."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_admin_user(current_user: models.User = Depends(get_current_user)):
    """Get the current user and verify they have admin role."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized. Admin role required.",
        )
    return current_user


def check_user_role(required_role: str):
    """Dependency function factory to check if user has a specific role."""

    async def check_role(current_user: models.User = Depends(get_current_user)):
        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        if current_user.role != required_role and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not authorized. {required_role.capitalize()} role required.",
            )
        return current_user

    return check_role


# Note: The async get_optional_current_user function defined above replaces this one


def create_default_admin(db: Session):
    """
    Create the default administrator account.
    This should be called when setting up a new instance of the application.
    """
    # Get admin credentials from environment or use defaults
    admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")  # Change in production!

    # Check if admin already exists
    admin = db.query(models.User).filter(models.User.email == admin_email).first()
    if not admin:
        # Create admin user
        admin = models.User(
            email=admin_email,
            hashed_password=get_password_hash(admin_password),
            is_active=True,
            role="admin",
            created_at=datetime.utcnow(),
        )
        db.add(admin)
        try:
            db.commit()
            db.refresh(admin)
            print(f"Created default admin user: {admin_email}")
            print("IMPORTANT: Please change the default admin password in production!")
        except Exception as e:
            db.rollback()
            print(f"Error creating admin user: {e}")
            raise
    return admin


def ensure_admin_exists(db: Session):
    """
    Ensure that at least one admin user exists in the system.
    Creates a default admin if none exists.
    """
    # Check if any admin user exists
    admin = db.query(models.User).filter(models.User.role == "admin").first()
    if not admin:
        # Create default admin if no admin exists
        admin = create_default_admin(db)
    return admin
