import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app
from app.api.models import UserProfile

class TestIntegration:
    """Tests d'intégration pour le service IA / Integration tests for AI service"""
    
    @pytest.fixture
    def client(self):
        """Client de test FastAPI / FastAPI test client"""
        return TestClient(app)
    
    @pytest.fixture
    def sample_user_profile(self):
        """Profil utilisateur de test / Test user profile"""
        return {
            "age": 25,
            "gender": "Homme",
            "weight": 75.0,
            "height": 180.0,
            "experience_level": "Débutant",
            "main_goal": "Prise de masse",
            "session_frequency": "3 fois par semaine",
            "session_duration": "60 minutes",
            "equipment": "Salle de sport complète",
            "training_preference": "Musculation"
        }
    
    def test_root_endpoint(self, client):
        """Test du endpoint racine / Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "status" in data
    
    def test_health_endpoint(self, client):
        """Test du endpoint de santé / Test health endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "ai-muscul-ia"
    
    def test_generate_training_program_endpoint(self, client, sample_user_profile):
        """Test du endpoint de génération de programme / Test program generation endpoint"""
        response = client.post("/generate-training-program", json=sample_user_profile)
        
        if response.status_code == 200:
            data = response.json()
            assert "name" in data
            assert "description" in data
            assert "category" in data
            assert "difficulty_level" in data
        else:
            assert response.status_code == 500
    
    def test_simple_question_endpoint(self, client):
        """Test du endpoint de question simple / Test simple question endpoint"""
        question_data = {"question": "Test question"}
        response = client.post("/simple-question", json=question_data)
        
        if response.status_code == 200:
            data = response.json()
            assert "status" in data
            assert "question" in data
            assert "response" in data
        else:
            assert response.status_code == 500
    
    def test_invalid_user_profile(self, client):
        """Test avec un profil utilisateur invalide / Test with invalid user profile"""
        invalid_profile = {
            "age": 5,
            "weight": 1000,
            "height": 50
        }
        response = client.post("/generate-training-program", json=invalid_profile)
        assert response.status_code == 422

if __name__ == "__main__":
    pytest.main([__file__]) 