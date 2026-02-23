"""
Shared test fixtures and configuration for FastAPI tests.
Uses AAA pattern: Arrange (fixtures setup), Act (test execution), Assert (test validation).
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Arrange: Create a TestClient connected to the FastAPI app.
    This provides a test-compatible client for making HTTP requests.
    """
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Arrange: Reset activities to a clean state before each test.
    This ensures test isolation - each test starts with predictable data.
    Auto-used for all tests.
    """
    # Store original state
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
        "Basketball Team": {
            "description": "Competitive basketball team for school tournaments",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Track and Field": {
            "description": "Running, jumping, and throwing events for athletic competitions",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["alex@mergington.edu", "grace@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and sculpture techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu"]
        },
        "Stage Production": {
            "description": "Drama club for theater performances and acting",
            "schedule": "Thursdays, 3:30 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["noah@mergington.edu", "lucas@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific concepts",
            "schedule": "Fridays, 3:00 PM - 4:30 PM",
            "max_participants": 16,
            "participants": ["mia@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and argumentation skills",
            "schedule": "Mondays and Fridays, 4:00 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["lucas@mergington.edu", "ava@mergington.edu"]
        }
    }
    
    # Clear and reset activities
    activities.clear()
    activities.update(original_activities)
    
    # Yield control to test
    yield
    
    # No cleanup needed - reset_activities will run again before next test
