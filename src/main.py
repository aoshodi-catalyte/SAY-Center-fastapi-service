"""Minimal FastAPI hello-world application used during early project setup.

Run with::

    uvicorn main:app --reload --app-dir src
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello_world() -> dict[str, str]:
    """Return a static greeting message."""
    return {"message": "Hello, World!"}


@app.get("/hello/{name}")
def hello_name(name: str) -> dict[str, str]:
    """Return a personalized greeting for the given name.

    Args:
        name: Name to include in the greeting.

    Returns:
        A JSON object containing the greeting message.
    """
    return {"message": f"Hello, {name}!"}
