from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from database import collection
from models import URL
from utils import generate_short_code

app = FastAPI()

BASE_URL = "http://localhost:8000"


@app.get("/")
def home():
    """Basic info endpoint for the URL shortener."""
    return {"message": "FastAPI URL Shortener"}


@app.post("/shorten")
def shorten_url(request: URL):
    """Create a short URL for the provided original URL.

    If the same original URL already exists in MongoDB, returns the existing
    `short_url` instead of creating a new record.
    """
    # Avoid creating duplicate short codes for the same original URL.
    original_url = request.url.strip()
    existing = collection.find_one({"original_url": original_url})
    if existing:
        short_url = f"{BASE_URL}/{existing['short_code']}"
        return {"short_url": short_url}

    short_code = generate_short_code()
    data = {
        "original_url": original_url,
        "short_code": short_code,
        "clicks": 0,
    }
    collection.insert_one(data)

    short_url = f"{BASE_URL}/{short_code}"
    return {"short_url": short_url}


@app.get("/{short_code}")
def redirect_url(short_code: str):
    """Redirect to the original URL for the given `short_code`.

    Increments `clicks` for analytics each time the short URL is used.
    """

    url = collection.find_one({"short_code": short_code})

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    collection.update_one(
        {"short_code": short_code},
        {"$inc": {"clicks": 1}}
    )

    return RedirectResponse(url["original_url"])