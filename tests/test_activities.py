"""
Tests for GET /activities endpoint.
Uses AAA pattern: Arrange → Act → Assert
"""

import pytest


def test_get_activities_returns_all_activities(client):
    """
    Test that GET /activities returns all activities.
    
    AAA Pattern:
    - Arrange: Use fixture client (already set up by conftest.py)
    - Act: Make GET request to /activities
    - Assert: Verify response status and content
    """
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    
    # Verify all expected activities are present
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Track and Field",
        "Art Studio",
        "Stage Production",
        "Science Club",
        "Debate Team"
    ]
    
    for activity in expected_activities:
        assert activity in activities


def test_get_activities_structure(client):
    """
    Test that each activity has the correct structure.
    
    AAA Pattern:
    - Arrange: Use fixture client
    - Act: Make GET request to /activities
    - Assert: Verify each activity has required fields
    """
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    for activity_name, activity_data in activities.items():
        for field in required_fields:
            assert field in activity_data, f"Activity '{activity_name}' missing field '{field}'"
        
        # Verify field types
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)


def test_get_activities_initial_participants(client):
    """
    Test that activities have the correct initial participants.
    
    AAA Pattern:
    - Arrange: Use fixture client
    - Act: Make GET request to /activities
    - Assert: Verify initial participant lists are correct
    """
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert - verify specific initial participants
    assert "michael@mergington.edu" in activities["Chess Club"]["participants"]
    assert "emma@mergington.edu" in activities["Programming Class"]["participants"]
    assert "john@mergington.edu" in activities["Gym Class"]["participants"]
