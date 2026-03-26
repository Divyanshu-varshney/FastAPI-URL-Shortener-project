# FastAPI URL Shortener

Simple URL shortener built with FastAPI.

## What it does

1. Generates a short code (random alphanumeric, 6 chars by default)
2. Stores the original URL in MongoDB with the short code
3. Redirects requests to `/{short_code}` back to the original URL
4. Tracks click counts (`clicks`) per short code

## Tech stack

- FastAPI (API)
- Uvicorn (dev server)
- MongoDB + PyMongo (storage)
- Pydantic (request model)

## Prerequisites

- Python 3.9+
- MongoDB running locally at `mongodb://localhost:27017/`

The app uses:
- Database: `url_shortener`
- Collection: `urls`

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Make sure MongoDB is running.
3. Start the API:
   ```bash
   uvicorn main:app --reload
   ```
   The app assumes `BASE_URL = "http://localhost:8000"`.

## API

### `GET /`

Health/info endpoint.

Response example:
```json
{ "message": "FastAPI URL Shortener" }
```

### `POST /shorten`

Create a short URL.

If the same `url` already exists in the database, the API will return the existing `short_url` (no duplicate entry is created).

Request body (JSON):
```json
{ "url": "https://example.com" }
```

Response:
```json
{
  "short_url": "http://localhost:8000/<short_code>"
}
```

### `GET /{short_code}`

Redirect to the stored original URL.

- If the short code does not exist, returns `404` with `{"detail":"URL not found"}`.
- On success, updates `clicks` using `$inc: { "clicks": 1 }` and returns an HTTP redirect.

## Example flow

1. Shorten a URL:
   ```bash
   curl -X POST http://localhost:8000/shorten \
     -H "Content-Type: application/json" \
     -d "{ \"url\": \"https://example.com\" }"
   ```
2. Open the returned `short_url` in your browser (or `curl` it) to trigger the redirect.
