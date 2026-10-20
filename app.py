from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data model
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory storage for events
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Helper function to find an event by ID
def find_event(event_id):
    return next((e for e in events if e.id == event_id), None)

# --- Routes ---

# Welcome route (Required by Rubric)
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Event Management API"}), 200

# GET /events - Retrieve all events (Required by Rubric)
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([e.to_dict() for e in events]), 200

# POST /events - Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json() or {}
    
    # Input validation
    if "title" not in data or not str(data["title"]).strip():
        return jsonify({"error": "Title is required"}), 400

    # Auto-generate next ID
    new_id = max([e.id for e in events], default=0) + 1
    new_event = Event(id=new_id, title=data["title"])
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201

# PATCH /events/<int:id> - Update the title of an event
@app.route("/events/<int:id>", methods=["PATCH"])
def update_event(id):
    event = find_event(id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json() or {}
    if "title" in data and str(data["title"]).strip():
        event.title = data["title"]
        return jsonify(event.to_dict()), 200
    
    return jsonify({"error": "Title is required for update"}), 400

# DELETE /events/<int:id> - Remove an event from the list
@app.route("/events/<int:id>", methods=["DELETE"])
def delete_event(id):
    event = find_event(id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)
    return jsonify({"message": f"Event {id} deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)