from typing import Optional, Dict, Any, Union
from fastapi.responses import Response, HTMLResponse


def trigger_client_event(
    response: Union[Response, HTMLResponse],
    event_name: str,
    detail: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Trigger a client-side event using HX-Trigger.

    Args:
        response: FastAPI response object
        event_name: Name of the event to trigger
        detail: Optional event details/data

    Example:
        response = HTMLResponse("Success")
        trigger_client_event(response, "showToast", {"message": "Success!", "type": "success"})
    """
    if detail:
        trigger_value = {event_name: detail}
    else:
        trigger_value = event_name

    response.headers["HX-Trigger"] = str(trigger_value).replace("'", '"')


def set_client_redirect(response: Union[Response, HTMLResponse], url: str) -> None:
    """
    Redirect the client to a new URL using HX-Redirect.

    Args:
        response: FastAPI response object
        url: URL to redirect to

    Example:
        response = HTMLResponse("Success")
        set_client_redirect(response, "/dashboard")
    """
    response.headers["HX-Redirect"] = url


def set_client_refresh(response: Union[Response, HTMLResponse]) -> None:
    """
    Refresh the client page using HX-Refresh.

    Args:
        response: FastAPI response object

    Example:
        response = HTMLResponse("Success")
        set_client_refresh(response)
    """
    response.headers["HX-Refresh"] = "true"


def set_client_retarget(
    response: Union[Response, HTMLResponse], css_selector: str
) -> None:
    """
    Change the target of an HTMX request using HX-Retarget.

    Args:
        response: FastAPI response object
        css_selector: CSS selector for the new target

    Example:
        response = HTMLResponse("<div>New content</div>")
        set_client_retarget(response, "#main-content")
    """
    response.headers["HX-Retarget"] = css_selector


def set_client_reswap(response: Union[Response, HTMLResponse], swap_style: str) -> None:
    """
    Change how the response content is swapped in using HX-Reswap.

    Args:
        response: FastAPI response object
        swap_style: HTMX swap modifier (innerHTML, outerHTML, beforebegin, etc.)

    Example:
        response = HTMLResponse("<div>New content</div>")
        set_client_reswap(response, "outerHTML")
    """
    response.headers["HX-Reswap"] = swap_style
