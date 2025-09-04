from flask import Flask, request, jsonify, redirect
import string, random, time
from datetime import datetime

app = Flask(__name__)

# In-memory storage for URL shortcodes
url_store = {}

# Default validity = 1 day (in seconds)
DEFAULT_VALIDITY_SECONDS = 24 * 60 * 60

# Logging Middleware
@app.before_request
def log_request():
    print(f"[{datetime.now()}] Incoming Request: {request.method} {request.path}")
    if request.method == "POST":
        print(f"Payload: {request.json}")

@app.after_request
def log_response(response):
    print(f"[{datetime.now()}] Response Status: {response.status}")
    return response

# Utility Functions
def generate_shortcode(length=6):
    """Generate a random shortcode (letters + digits)."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_expiry_time(validity_seconds):
    """Calculate expiry timestamp."""
    return time.time() + int(validity_seconds)

# Routes
@app.route("/shorturls", methods=["POST"])
def create_short_url():
    """Create a short URL."""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid JSON body"}), 400

        original_url = data.get("url")
        validity = data.get("validity", DEFAULT_VALIDITY_SECONDS)
        custom_shortcode = data.get("shortcode")

        if not original_url:
            return jsonify({"error": "URL is required"}), 400

        # Generate or validate shortcode
        shortcode = custom_shortcode if custom_shortcode else generate_shortcode()
        while not custom_shortcode and shortcode in url_store:
            shortcode = generate_shortcode()

        if shortcode in url_store and custom_shortcode:
            return jsonify({"error": "Shortcode already exists"}), 400

        # Save entry
        expiry_time = get_expiry_time(validity)
        url_store[shortcode] = {"url": original_url, "expiry": expiry_time}

        return jsonify({
            "short_url": f"{request.host_url}shorturls/{shortcode}",
            "expiry": expiry_time
        }), 201

    except Exception as e:
        print(f"[{datetime.now()}] Error in create_short_url: {str(e)}")
        return jsonify({"error": "Server error", "details": str(e)}), 500


@app.route("/shorturls/<shortcode>", methods=["GET"])
def retrieve_short_url(shortcode):
    """Retrieve original URL and redirect or return JSON."""
    try:
        entry = url_store.get(shortcode)
        if not entry:
            return jsonify({"error": "Short URL not found"}), 404

        if time.time() > entry["expiry"]:
            return jsonify({"error": "Short URL expired"}), 410

        # Postman-friendly: Return JSON instead of redirect
        if request.args.get("json") == "true":
            return jsonify({"original_url": entry["url"]}), 200

        # Default: redirect to original URL
        return redirect(entry["url"], code=302)

    except Exception as e:
        print(f"[{datetime.now()}] Error in retrieve_short_url: {str(e)}")
        return jsonify({"error": "Server error", "details": str(e)}), 500

# Global Exception Handler
@app.errorhandler(Exception)
def handle_unexpected_error(e):
    print(f"[{datetime.now()}] Unhandled Exception: {str(e)}")
    return jsonify({"error": "Server error", "details": str(e)}), 500

# Run the Flask App
if __name__ == "__main__":
    app.run(debug=True)
