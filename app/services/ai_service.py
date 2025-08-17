import httpx
import json
import logging
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv

from ..models.prompt_templates import build_training_program_prompt

load_dotenv()

logger = logging.getLogger(__name__)

class AIService:
    """Service pour l'interaction avec les modèles d'IA Ollama / Service for interaction with Ollama AI models"""
    
    def __init__(self):
        self.base_url = "http://ollama:11434"  
        self.model = "llama2:7b"      
        self.timeout = 300.0          
        
        logger.info(f"Service IA initialisé - Base URL: {self.base_url}, Model: {self.model}, Timeout: {self.timeout}s")
    
    async def generate_program(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Génère un programme d'entraînement personnalisé avec le modèle Ollama.
        Generates a personalized training program with the Ollama model.
        
        Args:
            user_profile: Dictionnaire contenant le profil utilisateur / Dictionary containing user profile
            
        Returns:
            Dict[str, Any]: Programme d'entraînement généré / Generated training program
        """
        try:
            logger.info(f"Génération de programme pour utilisateur {user_profile.get('age', 'N/A')} ans")
            
            prompt = build_training_program_prompt(user_profile)
            
            url = f"{self.base_url}/api/generate"
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                
                ai_response = response.json()
                response_text = ai_response.get("response", "")
                
                if not response_text:
                    logger.error("Réponse vide du modèle IA")
                    raise ValueError("Réponse vide du modèle IA")
            
            program_data = self._parse_ai_response(response_text)
            
            logger.info("✅ RÉSULTAT FINAL / FINAL RESULT:")
            logger.info("-" * 50)
            logger.info(f"Nom du programme: {program_data.get('name', 'N/A')}")
            logger.info(f"Catégorie: {program_data.get('category', 'N/A')}")
            logger.info(f"Niveau: {program_data.get('difficulty_level', 'N/A')}")
            logger.info(f"Nombre d'exercices: {len(program_data.get('exercises', []))}")
            
            if program_data.get('exercises'):
                logger.info("📋 EXERCICES DÉTECTÉS / EXERCISES DETECTED:")
                for i, exercise in enumerate(program_data['exercises'], 1):
                    logger.info(f"  {i}. {exercise.get('name', 'N/A')} - {exercise.get('muscle_group', 'N/A')} - {exercise.get('sets_count', 'N/A')}x{exercise.get('reps_count', 'N/A')}")
            else:
                logger.warning("⚠️ AUCUN EXERCICE DÉTECTÉ / NO EXERCISES DETECTED!")
            
            logger.info("=" * 100)
            
            return program_data
                
        except httpx.TimeoutException:
            logger.error(f"⏰ TIMEOUT: L'IA n'a pas répondu dans les {self.timeout}s alloués")
            raise Exception(f"Timeout de l'IA après {self.timeout}s")
        except httpx.HTTPStatusError as e:
            logger.error(f"Erreur HTTP {e.response.status_code}: {e.response.text}")
            raise Exception(f"Erreur HTTP {e.response.status_code}")
        except Exception as e:
            logger.error(f"Erreur inattendue: {str(e)}")
            raise Exception(f"Erreur de communication avec l'IA: {str(e)}")
    
    async def test_connection(self, test_prompt: str) -> str:
        """
        Teste la connexion avec le service IA.
        Tests connection with AI service.
        
        Args:
            test_prompt: Prompt de test simple / Simple test prompt
            
        Returns:
            str: Réponse du service IA / AI service response
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": test_prompt,
                        "stream": False
                    }
                )
                
                if response.status_code != 200:
                    raise Exception(f"Erreur de connexion: HTTP {response.status_code}")
                
                ai_response = response.json()
                return ai_response.get("response", "Pas de réponse")
                
        except Exception as e:
            logger.error(f"Erreur de test de connexion: {str(e)}")
            raise Exception(f"Impossible de se connecter au service IA: {str(e)}")
    
    def _parse_ai_response(self, ai_response: str) -> Dict[str, Any]:
        """
        Parse la réponse de l'IA pour extraire le JSON du programme.
        Parses AI response to extract program JSON.
        
        Args:
            ai_response: Réponse brute de l'IA / Raw AI response
            
        Returns:
            Dict[str, Any]: Programme d'entraînement parsé / Parsed training program
        """
        try:
            logger.info("🔍 DÉBUT DU PARSING DE LA RÉPONSE IA / STARTING AI RESPONSE PARSING")
            cleaned_response = ai_response.strip()
            logger.info(f"📝 Réponse IA brute (200 premiers caractères): {cleaned_response[:200]}...")
            
            json_start = cleaned_response.find('{')
            json_end = cleaned_response.rfind('}') + 1
            
            logger.info(f"🔍 Recherche JSON: début à {json_start}, fin à {json_end}")
            
            if json_start == -1 or json_end == 0:
                logger.warning("❌ Aucun JSON trouvé, création d'un programme par défaut")
                return self._create_default_program(cleaned_response)
            
            json_str = cleaned_response[json_start:json_end]
            logger.info(f"📋 JSON extrait (100 premiers caractères): {json_str[:100]}...")
            
            try:
                program_data = json.loads(json_str)
            except json.JSONDecodeError:
                logger.warning("JSON malformé détecté, tentative de correction...")
                
                json_str = json_str.replace('\n', ' ').replace('\r', ' ')
                json_str = json_str.replace('},}', '}}').replace(',}', '}')
                json_str = json_str.replace('},]', '}]').replace(',]', ']')
                json_str = json_str.replace('",}', '"}').replace(',}', '}')
                
                try:
                    program_data = json.loads(json_str)
                except json.JSONDecodeError:
                    logger.error(f"JSON toujours malformé après correction: {json_str}")
                    return self._create_default_program(cleaned_response)
            
            program_data = self._validate_and_clean_program_data(program_data)
            
            logger.info(f"Programme parsé avec succès: {program_data.get('name', 'N/A')}")
            return program_data
            
        except Exception as e:
            logger.error(f"Erreur lors du parsing de la réponse IA: {str(e)}")
            return self._create_default_program(cleaned_response)
    
    def _create_default_program(self, ai_response: str) -> Dict[str, Any]:
        """Crée un programme par défaut basé sur la réponse IA / Creates default program based on AI response"""
        # Extraire les exercices de la réponse IA
        exercises = self._extract_exercises_from_text(ai_response)
        
        return {
            "name": "Programme d'entraînement personnalisé",
            "description": f"Programme généré par IA: {ai_response[:100]}...",
            "category": "musculation",
            "difficulty_level": "beginner",
            "target_audience": "tous niveaux",
            "duration_weeks": 8,
            "sessions_per_week": 3,
            "estimated_duration_minutes": 45,
            "equipment_required": "dumbbells",
            "exercises": exercises,  # Ajout des exercices extraits
            "tips": "Commencez progressivement et écoutez votre corps",
            "progression_plan": "Augmentez progressivement l'intensité"
        }
    
    def _extract_exercises_from_text(self, ai_response: str) -> list:
        """
        Extrait les exercices de la réponse textuelle de l'IA.
        Extracts exercises from AI text response.
        
        Args:
            ai_response: Réponse textuelle de l'IA / AI text response
            
        Returns:
            list: Liste des exercices extraits / List of extracted exercises
        """
        exercises = []
        lines = ai_response.split('\n')
        
        for line in lines:
            line = line.strip()
            # Chercher les lignes qui contiennent des exercices (numérotés ou avec des noms d'exercices)
            if (line and 
                (line[0].isdigit() or 
                 any(exercise in line.lower() for exercise in [
                     'push-ups', 'squats', 'deadlifts', 'bench press', 'pull-ups',
                     'lunges', 'planks', 'burpees', 'mountain climbers', 'jumping jacks',
                     'dumbbell', 'barbell', 'curl', 'press', 'row', 'fly', 'extension',
                     'flexion', 'élévation', 'rotation', 'abduction', 'adduction'
                 ]))):
                
                # Nettoyer et structurer l'exercice
                exercise_data = self._parse_exercise_line(line)
                if exercise_data:
                    exercises.append(exercise_data)
        
        # Si aucun exercice trouvé, créer des exercices par défaut
        if not exercises:
            exercises = [
                {
                    "name": "Push-ups",
                    "description": "Pompes pour la poitrine et les triceps",
                    "muscle_group": "CHEST",
                    "equipment": "BODYWEIGHT",
                    "sets_count": 3,
                    "reps_count": 10,
                    "duration_seconds": 0,
                    "weight_kg": None,
                    "notes": "Commencez par les genoux si nécessaire"
                },
                {
                    "name": "Squats",
                    "description": "Squats pour les jambes",
                    "muscle_group": "LEGS",
                    "equipment": "BODYWEIGHT",
                    "sets_count": 3,
                    "reps_count": 15,
                    "duration_seconds": 0,
                    "weight_kg": None,
                    "notes": "Gardez le dos droit"
                }
            ]
        
        return exercises
    
    def _parse_exercise_line(self, line: str) -> Optional[Dict[str, Any]]:
        """
        Parse une ligne d'exercice pour extraire les informations.
        Parses an exercise line to extract information.
        
        Args:
            line: Ligne contenant l'exercice / Line containing exercise
            
        Returns:
            Optional[Dict[str, Any]]: Données de l'exercice ou None / Exercise data or None
        """
        try:
            # Nettoyer la ligne
            line = line.strip()
            if not line or len(line) < 5:
                return None
            
            # Extraire le nom de l'exercice (première partie avant les deux-points ou parenthèses)
            exercise_name = line.split(':')[0].split('(')[0].strip()
            
            # Déterminer le groupe musculaire basé sur le nom
            muscle_group = self._determine_muscle_group(exercise_name)
            
            # Extraire les informations de séries et répétitions
            sets_count, reps_count = self._extract_sets_and_reps(line)
            
            return {
                "name": exercise_name,
                "description": line,
                "muscle_group": muscle_group,
                "equipment": "BODYWEIGHT",  # Par défaut
                "sets_count": sets_count,
                "reps_count": reps_count,
                "duration_seconds": 0,
                "weight_kg": None,
                "notes": "Exercice extrait de la réponse IA"
            }
        except Exception as e:
            logger.warning(f"Erreur lors du parsing de la ligne d'exercice '{line}': {str(e)}")
            return None
    
    def _determine_muscle_group(self, exercise_name: str) -> str:
        """Détermine le groupe musculaire basé sur le nom de l'exercice"""
        exercise_name_lower = exercise_name.lower()
        
        if any(word in exercise_name_lower for word in ['push', 'bench', 'chest', 'pectoral']):
            return "CHEST"
        elif any(word in exercise_name_lower for word in ['pull', 'row', 'back', 'dorsal']):
            return "BACK"
        elif any(word in exercise_name_lower for word in ['squat', 'leg', 'thigh', 'quad']):
            return "LEGS"
        elif any(word in exercise_name_lower for word in ['curl', 'bicep']):
            return "BICEPS"
        elif any(word in exercise_name_lower for word in ['extension', 'tricep']):
            return "TRICEPS"
        elif any(word in exercise_name_lower for word in ['shoulder', 'press', 'élévation']):
            return "SHOULDERS"
        elif any(word in exercise_name_lower for word in ['abs', 'crunch', 'plank']):
            return "ABS"
        else:
            return "CARDIO"
    
    def _extract_sets_and_reps(self, line: str) -> tuple:
        """Extrait le nombre de séries et répétitions d'une ligne d'exercice"""
        try:
            # Chercher des patterns comme "3 sets of 8-10 reps" ou "3x8-10"
            import re
            
            # Pattern 1: "3 sets of 8-10 reps"
            pattern1 = r'(\d+)\s*sets?\s*of\s*(\d+)-?(\d+)?\s*reps?'
            match1 = re.search(pattern1, line, re.IGNORECASE)
            if match1:
                sets = int(match1.group(1))
                reps = int(match1.group(2))
                return sets, reps
            
            # Pattern 2: "3x8-10" ou "3x8"
            pattern2 = r'(\d+)x(\d+)-?(\d+)?'
            match2 = re.search(pattern2, line, re.IGNORECASE)
            if match2:
                sets = int(match2.group(1))
                reps = int(match2.group(2))
                return sets, reps
            
            # Pattern 3: "3 sets, 8-10 reps"
            pattern3 = r'(\d+)\s*sets?[,\s]+(\d+)-?(\d+)?\s*reps?'
            match3 = re.search(pattern3, line, re.IGNORECASE)
            if match3:
                sets = int(match3.group(1))
                reps = int(match3.group(2))
                return sets, reps
            
            # Valeurs par défaut si aucun pattern trouvé
            return 3, 10
            
        except Exception:
            return 3, 10
    
    def _validate_and_clean_program_data(self, program_data: Dict[str, Any]) -> Dict[str, Any]:
        """Valide et nettoie les données du programme / Validates and cleans program data"""
        required_fields = {
            'name': "Programme d'entraînement",
            'description': "Programme personnalisé",
            'category': "musculation",
            'difficulty_level': "beginner",
            'target_audience': "tous niveaux",
            'duration_weeks': 8,
            'sessions_per_week': 3,
            'estimated_duration_minutes': 45,
            'equipment_required': "dumbbells"
        }
        
        for field, default_value in required_fields.items():
            if field not in program_data or not program_data[field]:
                program_data[field] = default_value
        
        # Validation et nettoyage des exercices
        logger.info("🔍 VALIDATION DES EXERCICES / EXERCISE VALIDATION:")
        
        if 'exercises' not in program_data or not program_data['exercises']:
            logger.warning("⚠️ Aucun exercice trouvé dans la réponse IA, création d'exercices par défaut")
            program_data['exercises'] = [
                {
                    "name": "Push-ups",
                    "description": "Pompes pour la poitrine et les triceps",
                    "muscle_group": "CHEST",
                    "equipment": "BODYWEIGHT",
                    "sets_count": 3,
                    "reps_count": 10,
                    "duration_seconds": 0,
                    "weight_kg": None,
                    "notes": "Commencez par les genoux si nécessaire"
                },
                {
                    "name": "Squats",
                    "description": "Squats pour les jambes",
                    "muscle_group": "LEGS",
                    "equipment": "BODYWEIGHT",
                    "sets_count": 3,
                    "reps_count": 15,
                    "duration_seconds": 0,
                    "weight_kg": None,
                    "notes": "Gardez le dos droit"
                }
            ]
            logger.info("Exercices par défaut créés")
        else:
            # Valider chaque exercice
            validated_exercises = []
            for exercise in program_data['exercises']:
                if isinstance(exercise, dict):
                    validated_exercise = self._validate_exercise(exercise)
                    if validated_exercise:
                        validated_exercises.append(validated_exercise)
            
            program_data['exercises'] = validated_exercises
        
        # Conversion des listes en chaînes si nécessaire
        if 'tips' in program_data and not isinstance(program_data['tips'], str):
            program_data['tips'] = str(program_data['tips'])
        
        if 'progression_plan' in program_data and not isinstance(program_data['progression_plan'], str):
            program_data['progression_plan'] = str(program_data['progression_plan'])
        
        if 'equipment_required' in program_data and isinstance(program_data['equipment_required'], list):
            program_data['equipment_required'] = ', '.join(program_data['equipment_required'])
        
        # Validation des champs numériques
        if 'estimated_duration_minutes' in program_data:
            duration = program_data['estimated_duration_minutes']
            if isinstance(duration, list) and len(duration) > 0:
                program_data['estimated_duration_minutes'] = int(duration[0])
            elif isinstance(duration, (int, float)):
                program_data['estimated_duration_minutes'] = int(duration)
        
        if 'duration_weeks' in program_data:
            weeks = program_data['duration_weeks']
            if isinstance(weeks, list) and len(weeks) > 0:
                program_data['duration_weeks'] = int(weeks[0])
            elif isinstance(weeks, (int, float)):
                program_data['duration_weeks'] = int(weeks)
        
        if 'sessions_per_week' in program_data:
            sessions = program_data['sessions_per_week']
            if isinstance(sessions, list) and len(sessions) > 0:
                program_data['sessions_per_week'] = int(sessions[0])
            elif isinstance(sessions, (int, float)):
                program_data['sessions_per_week'] = int(sessions)
        
        return program_data
    
    def _validate_exercise(self, exercise: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Valide et nettoie un exercice individuel.
        Validates and cleans an individual exercise.
        
        Args:
            exercise: Données de l'exercice / Exercise data
            
        Returns:
            Optional[Dict[str, Any]]: Exercice validé ou None / Validated exercise or None
        """
        try:
            # Vérifier que l'exercice a au moins un nom
            if not exercise.get("name"):
                return None
            
            # Créer une copie de l'exercice pour éviter de modifier l'original
            validated_exercise = exercise.copy()
            
            # Valeurs par défaut pour les champs manquants
            if "muscle_group" not in validated_exercise or not validated_exercise["muscle_group"]:
                validated_exercise["muscle_group"] = "CARDIO"
            
            if "equipment" not in validated_exercise or not validated_exercise["equipment"]:
                validated_exercise["equipment"] = "BODYWEIGHT"
            
            if "sets_count" not in validated_exercise or not validated_exercise["sets_count"]:
                validated_exercise["sets_count"] = 3
            
            if "reps_count" not in validated_exercise or not validated_exercise["reps_count"]:
                validated_exercise["reps_count"] = 10
            
            if "description" not in validated_exercise:
                validated_exercise["description"] = f"Exercice: {validated_exercise['name']}"
            
            if "duration_seconds" not in validated_exercise:
                validated_exercise["duration_seconds"] = 0
            
            if "weight_kg" not in validated_exercise:
                validated_exercise["weight_kg"] = None
            
            if "notes" not in validated_exercise:
                validated_exercise["notes"] = ""
            
            return validated_exercise
            
        except Exception as e:
            logger.warning(f"Erreur lors de la validation de l'exercice: {str(e)}")
            return None

ai_service = AIService() 