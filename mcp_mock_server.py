# ------------------------------------------------------------
# MCP Mock Server
# Simulates the MCP endpoints for local agent testing
# ------------------------------------------------------------

from flask import Flask, request, jsonify
from functools import wraps
import os

app = Flask(__name__)

# Get expected token from environment
EXPECTED_TOKEN = os.getenv('MCP_TOKEN', 'temporary-access-token')

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({
                "status": "error",
                "message": "Authentication required. Missing Authorization header."
            }), 401
        
        # Extract token from "Bearer <token>"
        try:
            token = auth_header.split(' ')[1] if ' ' in auth_header else auth_header
        except IndexError:
            return jsonify({
                "status": "error",
                "message": "Invalid Authorization header format. Expected 'Bearer <token>'"
            }), 401
        
        # Validate token
        if token != EXPECTED_TOKEN:
            return jsonify({
                "status": "error",
                "message": "Invalid authentication token."
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function

# ------------------------------------------------------------
# /tools/analyzeSEO endpoint
# ------------------------------------------------------------
@app.route("/tools/analyzeSEO", methods=["POST"])
@require_auth
def analyze_seo():
    data = request.json or {}
    url = data.get("url", "")
    
    # Simulated response payload
    return jsonify({
        "status": "ok",
        "data": {
            "url": url,
            "visibility_score": 72,
            "backlinks": 154,
            "referring_domains": 42,
            "recommendations": [
                "Add structured data for business info",
                "Improve mobile page speed",
                "Include AI-intent keywords in headings"
            ]
        }
    })

# ------------------------------------------------------------
# /tools/generatePost endpoint
# ------------------------------------------------------------
@app.route("/tools/generatePost", methods=["POST"])
@require_auth
def generate_post():
    data = request.json or {}
    topic = data.get("topic", "AI Visibility")
    
    return jsonify({
        "status": "ok",
        "data": {
            "title": f"Boost Your {topic.title()} with AI Visibility",
            "body": f"This is a mock AI-generated post about {topic}. "
                    "It was created by the MCP mock server for testing purposes."
        }
    })

# ------------------------------------------------------------
# Root route for sanity check
# ------------------------------------------------------------
@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "✅ MCP Mock Server is running locally"}), 200


# ------------------------------------------------------------
# Server runner
# ------------------------------------------------------------
if __name__ == "__main__":
    print("🚀 MCP Mock Server running on http://127.0.0.1:5000")
    app.run(port=5000)
