URL Shortener
=============

A Flask-based URL shortener service with customizable shortcodes, expiration control, and built-in request/response logging middleware.

Features
--------
- Create short URLs with optional custom shortcodes
- Set expiry for each short URL (default: 24 hours)
- In-memory URL storage
- Request/response logging via custom Flask middleware
- RESTful API endpoints for short URL creation and resolution
- Error handling and user-friendly JSON responses

Getting Started
---------------
Requirements:
- Python 3.7+
- Flask

Install dependencies:
    pip install Flask

Run the Application:
    cd backend
    python app.py

The service runs on http://localhost:5000/ by default.

API Usage
---------

1. Create Short URL

Endpoint: POST /shorturls

Request Body (JSON):
    {
      "url": "https://example.com",
      "validity": 3600,        // (optional, seconds; default: 86400)
      "shortcode": "mycode"    // (optional, user-defined shortcode)
    }

Sample cURL:
    curl -X POST http://localhost:5000/shorturls \
      -H "Content-Type: application/json" \
      -d '{"url": "https://example.com"}'

Response:
    {
      "short_url": "http://localhost:5000/shorturls/XYZ789",
      "expiry": 1725563043.7924674
    }

2. Retrieve / Redirect Short URL

Endpoint: GET /shorturls/<shortcode>

- By default, redirects to the original URL if not expired.
- To get the underlying URL (for Postman/testing), append ?json=true.

Response:
    {
      "original_url": "https://example.com"
    }

Logging Middleware
------------------
Request and response logs are shown in the console for every incoming request:

- HTTP method and path
- JSON payload (for POST)
- Response status code

For advanced usage, the custom middleware functions in logging_middleware/middleware.py can be expanded or configured for file logging.

Error Handling
--------------
- 400: Bad request (missing fields, invalid JSON)
- 404: Shortcode not found
- 410: URL expired
- 500: Unhandled server errors

All errors return JSON with a relevant error description.
