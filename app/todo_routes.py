from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from datetime import datetime

from . import models, database
from .auth import get_current_active_user

router = APIRouter()


@router.get("/todos")
async def list_todos(
    request: Request,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(database.get_db),
):
    """Get all todos for the current user."""
    todos = db.query(models.Todo).filter(models.Todo.user_id == current_user.id).all()
    return {"todos": todos}


@router.post("/todos")
async def create_todo(
    request: Request,
    content: str = Form(...),
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(database.get_db),
):
    """Create a new todo."""
    todo = models.Todo(
        content=content, user_id=current_user.id, created_at=datetime.utcnow()
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)

    # Return the HTML for the new todo item
    return HTMLResponse(f"""
        <div id="todo-{todo.id}" class="flex items-center gap-2 p-2 bg-theme-bg rounded-md">
            <input type="checkbox" 
                   hx-post="/todos/{todo.id}/toggle"
                   hx-target="#todo-{todo.id}"
                   hx-swap="outerHTML"
                   class="form-checkbox">
            <span class="flex-1">{todo.content}</span>
            <button hx-delete="/todos/{todo.id}"
                    hx-target="#todo-{todo.id}"
                    hx-swap="outerHTML"
                    class="text-theme-error hover:opacity-80">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    """)


@router.post("/todos/{todo_id}/toggle")
async def toggle_todo(
    todo_id: int,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(database.get_db),
):
    """Toggle a todo's completed status."""
    todo = (
        db.query(models.Todo)
        .filter(models.Todo.id == todo_id, models.Todo.user_id == current_user.id)
        .first()
    )

    if todo:
        todo.completed = not todo.completed
        db.commit()
        db.refresh(todo)

        return HTMLResponse(f"""
            <div id="todo-{todo.id}" class="flex items-center gap-2 p-2 bg-theme-bg rounded-md">
                <input type="checkbox" 
                       {"checked" if todo.completed else ""}
                       hx-post="/todos/{todo.id}/toggle"
                       hx-target="#todo-{todo.id}"
                       hx-swap="outerHTML"
                       class="form-checkbox">
                <span class="flex-1 {"line-through text-theme-fg1" if todo.completed else ""}">{todo.content}</span>
                <button hx-delete="/todos/{todo.id}"
                        hx-target="#todo-{todo.id}"
                        hx-swap="outerHTML"
                        class="text-theme-error hover:opacity-80">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        """)


@router.delete("/todos/{todo_id}")
async def delete_todo(
    todo_id: int,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(database.get_db),
):
    """Delete a todo."""
    todo = (
        db.query(models.Todo)
        .filter(models.Todo.id == todo_id, models.Todo.user_id == current_user.id)
        .first()
    )

    if todo:
        db.delete(todo)
        db.commit()
        return HTMLResponse("")
