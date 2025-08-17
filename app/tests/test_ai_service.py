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
    
    def test_extract_exercises_from_text(self, ai_service):
        """Test d'extraction d'exercices depuis du texte / Test exercise extraction from text"""
        ai_response = """
        1. Push-ups: 3 sets of 10-15 reps
        2. Squats: 3 sets of 15-20 reps
        3. Deadlifts: 3 sets of 8-10 reps
        """
        exercises = ai_service._extract_exercises_from_text(ai_response)
        
        assert len(exercises) >= 2
        assert any("Push-ups" in ex["name"] for ex in exercises)
        assert any("Squats" in ex["name"] for ex in exercises)
    
    def test_extract_exercises_from_text_no_exercises(self, ai_service):
        """Test d'extraction quand aucun exercice n'est trouvé / Test extraction when no exercises found"""
        ai_response = "Ceci est juste du texte sans exercices"
        exercises = ai_service._extract_exercises_from_text(ai_response)
        
        # Devrait créer des exercices par défaut
        assert len(exercises) == 2
        assert any("Push-ups" in ex["name"] for ex in exercises)
        assert any("Squats" in ex["name"] for ex in exercises)
    
    def test_parse_exercise_line(self, ai_service):
        """Test de parsing d'une ligne d'exercice / Test parsing exercise line"""
        exercise_line = "1. Push-ups: 3 sets of 10-15 reps"
        exercise = ai_service._parse_exercise_line(exercise_line)
        
        assert exercise is not None
        assert exercise["name"] == "1. Push-ups"
        assert exercise["muscle_group"] == "CHEST"
        assert exercise["sets_count"] == 3
        assert exercise["reps_count"] == 10
    
    def test_parse_exercise_line_invalid(self, ai_service):
        """Test de parsing d'une ligne invalide / Test parsing invalid line"""
        invalid_line = ""
        exercise = ai_service._parse_exercise_line(invalid_line)
        
        assert exercise is None
    
    def test_determine_muscle_group(self, ai_service):
        """Test de détermination du groupe musculaire / Test muscle group determination"""
        assert ai_service._determine_muscle_group("Push-ups") == "CHEST"
        assert ai_service._determine_muscle_group("Squats") == "LEGS"
        assert ai_service._determine_muscle_group("Bicep Curls") == "BICEPS"
        assert ai_service._determine_muscle_group("Tricep Extensions") == "TRICEPS"
        assert ai_service._determine_muscle_group("Shoulder Press") == "SHOULDERS"
        assert ai_service._determine_muscle_group("Plank") == "ABS"
        assert ai_service._determine_muscle_group("Running") == "CARDIO"
    
    def test_extract_sets_and_reps(self, ai_service):
        """Test d'extraction des séries et répétitions / Test sets and reps extraction"""
        # Pattern 1: "3 sets of 8-10 reps"
        sets, reps = ai_service._extract_sets_and_reps("3 sets of 8-10 reps")
        assert sets == 3
        assert reps == 8
        
        # Pattern 2: "3x8-10"
        sets, reps = ai_service._extract_sets_and_reps("3x8-10")
        assert sets == 3
        assert reps == 8
        
        # Pattern 3: "3 sets, 8-10 reps"
        sets, reps = ai_service._extract_sets_and_reps("3 sets, 8-10 reps")
        assert sets == 3
        assert reps == 8
        
        # Valeurs par défaut
        sets, reps = ai_service._extract_sets_and_reps("Exercice sans format")
        assert sets == 3
        assert reps == 10
    
    def test_validate_exercise(self, ai_service):
        """Test de validation d'un exercice / Test exercise validation"""
        valid_exercise = {
            "name": "Test Exercise",
            "description": "Test Description",
            "muscle_group": "CHEST",
            "equipment": "BODYWEIGHT",
            "sets_count": 3,
            "reps_count": 10,
            "duration_seconds": 0,
            "weight_kg": None,
            "notes": "Test notes"
        }
        
        result = ai_service._validate_exercise(valid_exercise)
        assert result is not None
        assert result["name"] == "Test Exercise"
        assert result["sets_count"] == 3
        assert result["reps_count"] == 10
    
    def test_validate_exercise_with_defaults(self, ai_service):
        """Test de validation d'un exercice avec valeurs par défaut / Test exercise validation with defaults"""
        incomplete_exercise = {"name": "Test"}
        
        result = ai_service._validate_exercise(incomplete_exercise)
        assert result is not None
        assert result["name"] == "Test"
        assert result["sets_count"] == 3
        assert result["reps_count"] == 10
        assert result["muscle_group"] == "CARDIO"
        assert result["equipment"] == "BODYWEIGHT"
    
    def test_validate_and_clean_program_data_with_exercises(self, ai_service):
        """Test de validation avec exercices / Test validation with exercises"""
        program_with_exercises = {
            "name": "Test Program",
            "exercises": [
                {
                    "name": "Test Exercise",
                    "sets_count": 3,
                    "reps_count": 10
                }
            ]
        }
        
        result = ai_service._validate_and_clean_program_data(program_with_exercises)
        assert "exercises" in result
        assert len(result["exercises"]) == 1
        assert result["exercises"][0]["name"] == "Test Exercise"
        assert result["exercises"][0]["sets_count"] == 3
        assert result["exercises"][0]["reps_count"] == 10
    
    def test_validate_and_clean_program_data_without_exercises(self, ai_service):
        """Test de validation sans exercices (devrait en créer) / Test validation without exercises (should create some)"""
        program_without_exercises = {"name": "Test Program"}
        
        result = ai_service._validate_and_clean_program_data(program_without_exercises)
        assert "exercises" in result
        assert len(result["exercises"]) == 2  # Exercices par défaut
        assert any("Push-ups" in ex["name"] for ex in result["exercises"])
        assert any("Squats" in ex["name"] for ex in result["exercises"])

if __name__ == "__main__":
    pytest.main([__file__]) 