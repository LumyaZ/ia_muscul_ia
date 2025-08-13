import json
import random
from typing import Dict, Any

class MockAIService:
    """Service IA mock pour générer des programmes d'entraînement sans gros modèle."""
    
    def __init__(self):
        self.program_templates = {
            "muscle_gain": {
                "name": "Programme Prise de Masse",
                "description": "Programme spécialement conçu pour développer la masse musculaire",
                "category": "Musculation",
                "difficulty_level": "Débutant",
                "target_audience": "Hommes débutants",
                "duration_weeks": 8,
                "sessions_per_week": 3,
                "estimated_duration_minutes": 45,
                "equipment_required": "Haltères, tapis",
                "exercises": [
                    "Squats avec haltères",
                    "Développé couché",
                    "Tractions assistées",
                    "Fentes avec haltères",
                    "Curl biceps",
                    "Extensions triceps"
                ],
                "tips": "Mangez suffisamment de protéines et dormez 8h par nuit",
                "progression_plan": "Augmentez progressivement les poids chaque semaine"
            },
            "weight_loss": {
                "name": "Programme Perte de Poids",
                "description": "Programme cardio et musculation pour perdre du poids",
                "category": "Fitness",
                "difficulty_level": "Débutant",
                "target_audience": "Tous niveaux",
                "duration_weeks": 6,
                "sessions_per_week": 4,
                "estimated_duration_minutes": 30,
                "equipment_required": "Tapis, haltères légers",
                "exercises": [
                    "Burpees",
                    "Mountain climbers",
                    "Jumping jacks",
                    "Squats",
                    "Push-ups",
                    "Planks"
                ],
                "tips": "Combinez exercice et alimentation équilibrée",
                "progression_plan": "Augmentez l'intensité progressivement"
            },
            "strength": {
                "name": "Programme Force",
                "description": "Programme pour développer la force maximale",
                "category": "Force",
                "difficulty_level": "Intermédiaire",
                "target_audience": "Athlètes",
                "duration_weeks": 10,
                "sessions_per_week": 3,
                "estimated_duration_minutes": 60,
                "equipment_required": "Haltères, barre",
                "exercises": [
                    "Squats",
                    "Deadlifts",
                    "Bench press",
                    "Overhead press",
                    "Rows",
                    "Pull-ups"
                ],
                "tips": "Privilégiez les exercices composés",
                "progression_plan": "Augmentez les charges de 2.5kg par semaine"
            }
        }
    
    async def generate_program(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Génère un programme d'entraînement basé sur les données utilisateur."""
        
        # Déterminer le type de programme basé sur l'objectif
        goal = user_data.get('main_goal', 'muscle_gain')
        
        # Adapter le programme selon l'équipement
        equipment = user_data.get('equipment', 'dumbbells')
        
        # Obtenir le template de base
        template = self.program_templates.get(goal, self.program_templates['muscle_gain']).copy()
        
        # Adapter selon l'âge et l'expérience
        age = user_data.get('age', 25)
        experience = user_data.get('experience_level', 'beginner')
        
        if age > 40:
            template['tips'] += " Consultez un médecin avant de commencer."
        
        if experience == 'beginner':
            template['difficulty_level'] = 'Débutant'
            template['tips'] += " Commencez doucement et augmentez progressivement."
        elif experience == 'intermediate':
            template['difficulty_level'] = 'Intermédiaire'
        else:
            template['difficulty_level'] = 'Avancé'
        
        # Adapter la durée selon les préférences
        session_duration = user_data.get('session_duration', '45_minutes')
        if '30' in session_duration:
            template['estimated_duration_minutes'] = 30
        elif '60' in session_duration:
            template['estimated_duration_minutes'] = 60
        
        return template
    
    async def test_connection(self, prompt: str) -> str:
        """Teste la connexion du service IA."""
        return "Service IA Mock fonctionne correctement !" 