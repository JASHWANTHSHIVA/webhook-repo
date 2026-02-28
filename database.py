"""
database.py
MongoDB connection and helper functions for storing and retrieving webhook events.
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "techstax_webhooks")
COLLECTION_NAME = "events"

# Initialize MongoDB client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
events_collection = db[COLLECTION_NAME]


def insert_event(event: dict) -> bool:
    """
    Insert a new webhook event into MongoDB.
    Avoids duplicate entries based on request_id + action.

    :param event: dict with keys: request_id, author, action, from_branch, to_branch, timestamp
    :return: True if inserted, False if duplicate
    """
    # Prevent exact duplicates (same request_id and action)
    existing = events_collection.find_one({
        "request_id": event.get("request_id"),
        "action": event.get("action")
    })
    if existing:
        return False

    events_collection.insert_one(event)
    return True


def get_all_events() -> list:
    """
    Retrieve all events from MongoDB, sorted by insertion order (newest first).

    :return: List of event dicts (with _id removed for JSON serialization)
    """
    cursor = events_collection.find({}, {"_id": 0}).sort("_id", -1)
    return list(cursor)
