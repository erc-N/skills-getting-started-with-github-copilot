"""Test cases for the FastAPI application."""

import pytest


class TestGetActivities:
    """Tests for the GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """Test that /activities returns all activities."""
        response = client.get("/activities")
        assert response.status_code == 200
        
        activities = response.json()
        assert len(activities) == 9
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Gym Class" in activities

    def test_get_activities_has_correct_structure(self, client):
        """Test that activities have the correct structure."""
        response = client.get("/activities")
        activities = response.json()
        
        activity = activities["Chess Club"]
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity

    def test_get_activities_has_initial_participants(self, client):
        """Test that activities have initial participants."""
        response = client.get("/activities")
        activities = response.json()
        
        chess_club = activities["Chess Club"]
        assert len(chess_club["participants"]) == 2
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]


class TestSignup:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_new_student(self, client):
        """Test signing up a new student for an activity."""
        response = client.post(
            "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "Signed up newstudent@mergington.edu for Chess Club"

    def test_signup_adds_participant(self, client):
        """Test that signup adds participant to the activity."""
        # Sign up a new student
        client.post("/activities/Chess%20Club/signup?email=newstudent@mergington.edu")
        
        # Get activities and verify
        response = client.get("/activities")
        activities = response.json()
        
        assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]
        assert len(activities["Chess Club"]["participants"]) == 3

    def test_signup_duplicate_student_fails(self, client):
        """Test that signing up a duplicate student fails."""
        response = client.post(
            "/activities/Chess%20Club/signup?email=michael@mergington.edu"
        )
        assert response.status_code == 400
        
        data = response.json()
        assert data["detail"] == "Student already signed up for this activity"

    def test_signup_nonexistent_activity_fails(self, client):
        """Test that signing up for a nonexistent activity fails."""
        response = client.post(
            "/activities/Nonexistent%20Activity/signup?email=student@mergington.edu"
        )
        assert response.status_code == 404
        
        data = response.json()
        assert data["detail"] == "Activity not found"

    def test_signup_multiple_activities(self, client):
        """Test that a student can sign up for multiple activities."""
        # Sign up for Chess Club
        response1 = client.post(
            "/activities/Chess%20Club/signup?email=student@mergington.edu"
        )
        assert response1.status_code == 200
        
        # Sign up for Programming Class
        response2 = client.post(
            "/activities/Programming%20Class/signup?email=student@mergington.edu"
        )
        assert response2.status_code == 200
        
        # Verify both signups
        response = client.get("/activities")
        activities = response.json()
        
        assert "student@mergington.edu" in activities["Chess Club"]["participants"]
        assert "student@mergington.edu" in activities["Programming Class"]["participants"]


class TestUnregister:
    """Tests for the DELETE /activities/{activity_name}/unregister endpoint."""

    def test_unregister_existing_participant(self, client):
        """Test unregistering an existing participant."""
        response = client.delete(
            "/activities/Chess%20Club/unregister?email=michael@mergington.edu"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "Unregistered michael@mergington.edu from Chess Club"

    def test_unregister_removes_participant(self, client):
        """Test that unregister removes participant from activity."""
        # Unregister a participant
        client.delete("/activities/Chess%20Club/unregister?email=michael@mergington.edu")
        
        # Get activities and verify
        response = client.get("/activities")
        activities = response.json()
        
        assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
        assert len(activities["Chess Club"]["participants"]) == 1

    def test_unregister_nonexistent_participant_fails(self, client):
        """Test that unregistering a nonexistent participant fails."""
        response = client.delete(
            "/activities/Chess%20Club/unregister?email=nonexistent@mergington.edu"
        )
        assert response.status_code == 400
        
        data = response.json()
        assert data["detail"] == "Student is not registered for this activity"

    def test_unregister_from_nonexistent_activity_fails(self, client):
        """Test that unregistering from a nonexistent activity fails."""
        response = client.delete(
            "/activities/Nonexistent%20Activity/unregister?email=student@mergington.edu"
        )
        assert response.status_code == 404
        
        data = response.json()
        assert data["detail"] == "Activity not found"

    def test_unregister_then_signup_again(self, client):
        """Test that a student can unregister and sign up again."""
        # Unregister
        client.delete("/activities/Chess%20Club/unregister?email=michael@mergington.edu")
        
        # Sign up again
        response = client.post(
            "/activities/Chess%20Club/signup?email=michael@mergington.edu"
        )
        assert response.status_code == 200
        
        # Verify
        response = client.get("/activities")
        activities = response.json()
        assert "michael@mergington.edu" in activities["Chess Club"]["participants"]


class TestEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_email_with_special_characters_encoded(self, client):
        """Test signup with email containing special characters (URL encoded)."""
        response = client.post(
            "/activities/Chess%20Club/signup?email=student%2Btest@mergington.edu"
        )
        assert response.status_code == 200
        
        # Verify
        response = client.get("/activities")
        activities = response.json()
        assert "student+test@mergington.edu" in activities["Chess Club"]["participants"]

    def test_activity_with_spaces_in_name(self, client):
        """Test that activities with spaces in names work correctly."""
        response = client.post(
            "/activities/Programming%20Class/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200

    def test_case_sensitive_activity_names(self, client):
        """Test that activity names are case-sensitive."""
        response = client.post(
            "/activities/chess%20club/signup?email=student@mergington.edu"
        )
        assert response.status_code == 404
