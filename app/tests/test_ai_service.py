import pytest
import asyncio
from unittest.mock import Mock, patch
from app.services.ai_service import AIService
from app.api.models import UserProfile

class TestAIService:
    """Tests unitaires pour le service IA / Unit tests for AI service"""
    
    @pytest.fixture
    def ai_service(self):
        """Fixture pour créer une instance du service IA / Fixture to create AI service instance"""
        return AIService()
    
    @pytest.fixture
    def sample_user_profile(self):
        """Fixture pour un profil utilisateur de test / Fixture for test user profile"""
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
    
    def test_ai_service_initialization(self, ai_service):
        """Test d'initialisation du service IA / Test AI service initialization"""
        assert ai_service.base_url is not None
        assert ai_service.model is not None
        assert ai_service.timeout > 0
    
    @patch('httpx.AsyncClient.post')
    @pytest.mark.asyncio
    async def test_generate_program_success(self, mock_post, ai_service, sample_user_profile):
        """Test de génération de programme réussie / Test successful program generation"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response": '{"name": "Test Program", "description": "Test", "category": "musculation", "difficulty_level": "beginner", "target_audience": "test", "duration_weeks": 6, "sessions_per_week": 3, "estimated_duration_minutes": 45, "equipment_required": "dumbbells"}'
        }
        mock_post.return_value = mock_response
        
        result = await ai_service.generate_program(sample_user_profile)
        
        assert result is not None
        assert "name" in result
        assert "description" in result
        assert result["name"] == "Test Program"
    
    @patch('httpx.AsyncClient.post')
    @pytest.mark.asyncio
    async def test_generate_program_timeout(self, mock_post, ai_service, sample_user_profile):
        """Test de timeout lors de la génération / Test timeout during generation"""
        mock_post.side_effect = Exception("Timeout")
        
        with pytest.raises(Exception):
            await ai_service.generate_program(sample_user_profile)
    
    def test_parse_ai_response_valid_json(self, ai_service):
        """Test de parsing d'une réponse JSON valide / Test parsing valid JSON response"""
        valid_response = '{"name": "Test", "description": "Test desc"}'
        result = ai_service._parse_ai_response(valid_response)
        
        assert result["name"] == "Test"
        assert result["description"] == "Test desc"
    
    def test_parse_ai_response_invalid_json(self, ai_service):
        """Test de parsing d'une réponse JSON invalide / Test parsing invalid JSON response"""
        invalid_response = "Invalid JSON response"
        result = ai_service._parse_ai_response(invalid_response)
        
        assert result["name"] == "Programme d'entraînement personnalisé"
    
    def test_validate_and_clean_program_data(self, ai_service):
        """Test de validation et nettoyage des données / Test data validation and cleaning"""
        incomplete_data = {"name": "Test"}
        result = ai_service._validate_and_clean_program_data(incomplete_data)
        
        assert "description" in result
        assert "category" in result
        assert "difficulty_level" in result
        assert "duration_weeks" in result
        assert "sessions_per_week" in result
        assert "estimated_duration_minutes" in result
        assert "equipment_required" in result

if __name__ == "__main__":
    pytest.main([__file__]) 