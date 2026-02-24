"""
Tests for POST /activities/{activity_name}/signup endpoint.
Uses AAA pattern: Arrange → Act → Assert
"""

import pytest


def test_signup_successful(client):
    """
    Test successful signup for an activity.
    
    AAA Pattern:
    - Arrange: Use fixture client with reset activities
    - Act: Sign up a new student for an activity
    - Assert: Verify status 200 and student added to participants
    """
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    
    # Verify student was actually added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]


def test_signup_activity_not_found(client):
    """
    Test signup fails when activity doesn't exist.
    
    AAA Pattern:
    - Arrange: Use fixture client
    - Act: Try to sign up for non-existent activity
    - Assert: Verify 404 error response
    """
    # Arrange
    invalid_activity = "Non Existent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{invalid_activity}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_already_registered(client):
    """
    Test signup fails when student is already registered.
    
    AAA Pattern:
    - Arrange: Use fixture client, identify already registered student
    - Act: Try to sign up the same student again
    - Assert: Verify 400 error response
    """
    # Arrange
    activity_name = "Chess Club"
    already_registered_email = "michael@mergington.edu"  # Already in Chess Club
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": already_registered_email})
    
    # Assert
    assert response.status_code == 400
    assert "Student already signed up" in response.json()["detail"]


def test_signup_multiple_students_same_activity(client):
    """
    Test multiple students can sign up for the same activity.
    
    AAA Pattern:
    - Arrange: Prepare multiple student emails
    - Act: Sign up each student to the same activity
    - Assert: Verify all students are added
    """
    # Arrange
    activity_name = "Art Studio"
    students = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
    
    # Act & Assert
    for student_email in students:
        response = client.post(f"/activities/{activity_name}/signup", params={"email": student_email})
        assert response.status_code == 200
    
    # Verify all students were added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    
    for student_email in students:
        assert student_email in activities[activity_name]["participants"]


def test_signup_to_different_activities(client):
    """
    Test a student can sign up for multiple different activities.
    
    AAA Pattern:
    - Arrange: Prepare activities list
    - Act: Sign up same student to multiple activities
    - Assert: Verify student is in all activities
    """
    # Arrange
    student_email = "versatile@mergington.edu"
    activities_to_join = ["Chess Club", "Science Club", "Debate Team"]
    
    # Act & Assert - Sign up for each activity
    for activity_name in activities_to_join:
        response = client.post(f"/activities/{activity_name}/signup", params={"email": student_email})
        assert response.status_code == 200
    
    # Verify student is in all activities
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    
    for activity_name in activities_to_join:
        assert student_email in activities_data[activity_name]["participants"]
