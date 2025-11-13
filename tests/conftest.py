"""Pytest configuration and fixtures."""

import sys
from pathlib import Path

# Add the src directory to the path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from fastapi.testclient import TestClient
from app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test."""
    from app import activities
    
    # Store the original activities
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Competitive soccer team training and matches",
            "schedule": "Mondays, Wednesdays, 4:00 PM - 6:00 PM",
            "max_participants": 18,
            "participants": ["liam@mergington.edu", "noah@mergington.edu"]
        },
        "Basketball Club": {
            "description": "Pickup games and skill development for basketball players",
            "schedule": "Tuesdays, Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 15,
            "participants": ["ava@mergington.edu", "isabella@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore drawing, painting, and mixed media projects",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["mia@mergington.edu", "charlotte@mergington.edu"]
        },
        "Drama Society": {
            "description": "Acting, stagecraft, and putting on school productions",
            "schedule": "Thursdays, 3:30 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["logan@mergington.edu", "lucas@mergington.edu"]
        },
        "Science Club": {
            "description": "Hands-on experiments, science fairs, and research projects",
            "schedule": "Fridays, 2:30 PM - 4:00 PM",
            "max_participants": 20,
            "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
        },
        "Debate Team": {
            "description": "Practice formal debating and compete in tournaments",
            "schedule": "Mondays, Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["jackson@mergington.edu", "elijah@mergington.edu"]
        }
    }
    
    # Clear current activities
    activities.clear()
    
    # Restore original activities
    for activity_name, activity_details in original_activities.items():
        activities[activity_name] = activity_details.copy()
        # Make a copy of participants list too
        activities[activity_name]["participants"] = activity_details["participants"].copy()
    
    yield
    
    # Reset after test
    activities.clear()
    for activity_name, activity_details in original_activities.items():
        activities[activity_name] = activity_details.copy()
        activities[activity_name]["participants"] = activity_details["participants"].copy()
