"""
app.py
Flask application for the TechStaX Webhook Receiver.

Endpoints:
  POST /webhook  - Receives GitHub Actions webhook events and stores in MongoDB
  GET  /events   - Returns all stored events as JSON (polled by UI every 15s)
  GET  /         - Serves the main UI page
"""

from flask import Flask, request, jsonify, render_template
from database import insert_event, get_all_events

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook_receiver():
    """
    Receives webhook POST requests from GitHub Actions (action-repo).
    Validates payload and stores in MongoDB.
    Expected JSON fields: request_id, author, action, from_branch, to_branch, timestamp
    """
    data = request.get_json(silent=True)

    # Validate that all required fields are present
    required_fields = ["request_id", "author", "action", "from_branch", "to_branch", "timestamp"]
    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Validate action type
    allowed_actions = ["PUSH", "PULL_REQUEST", "MERGE"]
    if data["action"] not in allowed_actions:
        return jsonify({"error": f"Invalid action. Must be one of {allowed_actions}"}), 400

    # Build the event document
    event = {
        "request_id": str(data["request_id"]),
        "author":     str(data["author"]),
        "action":     str(data["action"]),
        "from_branch": str(data["from_branch"]),
        "to_branch":   str(data["to_branch"]),
        "timestamp":   str(data["timestamp"])
    }

    inserted = insert_event(event)
    if inserted:
        return jsonify({"status": "success", "message": "Event stored successfully"}), 201
    else:
        return jsonify({"status": "duplicate", "message": "Event already exists, skipped"}), 200


@app.route("/events", methods=["GET"])
def get_events():
    """
    Returns all stored webhook events as a JSON array.
    The UI polls this endpoint every 15 seconds.
    """
    events = get_all_events()
    return jsonify(events), 200


@app.route("/", methods=["GET"])
def index():
    """
    Serves the main UI page.
    """
    return render_template("index.html")


if __name__ == "__main__":
    # Run the Flask app on port 5000 with debug mode
    app.run(debug=True, port=5000)
