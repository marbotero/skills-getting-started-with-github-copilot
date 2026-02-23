"""
Tests for DELETE /activities/{activity_name}/participants endpoint.
Uses AAA pattern: Arrange → Act → Assert
"""

import pytest


def test_unregister_successful(client):
    """
    Test successful unregistration from an activity.
    
    AAA Pattern:
    - Arrange: Use fixture client with reset activities, pick existing participant
    - Act: Unregister student from activity
    - Assert: Verify status 200 and student removed from participants
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered in Chess Club
    
    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
    
    # Verify student was actually removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_activity_not_found(client):
    """
    Test unregister fails when activity doesn't exist.
    
    AAA Pattern:
    - Arrange: Use fixture client
    - Act: Try to unregister from non-existent activity
    - Assert: Verify 404 error response
    """
    # Arrange
    invalid_activity = "Non Existent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{invalid_activity}/participants", params={"email": email})
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_participant_not_found(client):
    """
    Test unregister fails when student is not registered.
    
    AAA Pattern:
    - Arrange: Use fixture client, pick non-registered student
    - Act: Try to unregister non-existent participant
    - Assert: Verify 404 error response
    """
    # Arrange
    activity_name = "Chess Club"
    not_registered_email = "notregistered@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": not_registered_email})
    
    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_unregister_then_cannot_unregister_again(client):
    """
    Test that unregistering twice fails (participant no longer exists).
    
    AAA Pattern:
    - Arrange: Use fixture client, pick existing participant
    - Act: Unregister once (success), unregister again (should fail)
    - Assert: First succeeds, second fails with 404
    """
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"
    
    # Act - First unregister (should succeed)
    response1 = client.delete(f"/activities/{activity_name}/participants", params={"email": email})
    assert response1.status_code == 200
    
    # Act - Second unregister (should fail)
    response2 = client.delete(f"/activities/{activity_name}/participants", params={"email": email})
    
    # Assert
    assert response2.status_code == 404
    assert "Participant not found" in response2.json()["detail"]


def test_unregister_multiple_participants(client):
    """
    Test unregistering multiple participants from the same activity.
    
    AAA Pattern:
    - Arrange: Identify multiple registered participants in an activity
    - Act: Unregister each one
    - Assert: Verify all were removed correctly
    """
    # Arrange
    activity_name = "Debate Team"
    participants_to_remove = ["lucas@mergington.edu", "ava@mergington.edu"]
    
    # Get initial count
    activities_response = client.get("/activities")
    initial_count = len(activities_response.json()[activity_name]["participants"])
    
    # Act & Assert - Remove each participant
    for email in participants_to_remove:
        response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})
        assert response.status_code == 200
    
    # Verify all were removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    final_count = len(activities[activity_name]["participants"])
    
    assert final_count == initial_count - len(participants_to_remove)
    for email in participants_to_remove:
        assert email not in activities[activity_name]["participants"]


def test_unregister_then_can_register_again(client):
    """
    Test that a student can re-register after unregistering.
    
    AAA Pattern:
    - Arrange: Pick registered student
    - Act: Unregister, then signup again
    - Assert: Both operations succeed, student back in participants
    """
    # Arrange
    activity_name = "Track and Field"
    email = "alex@mergington.edu"
    
    # Act - Unregister
    response1 = client.delete(f"/activities/{activity_name}/participants", params={"email": email})
    assert response1.status_code == 200
    
    # Act - Sign up again
    response2 = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response2.status_code == 200
    
    # Assert
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]
