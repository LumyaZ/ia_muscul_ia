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
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "llama2:7b")
        self.timeout = int(os.getenv('AI_TIMEOUT', '300000')) / 1000
        
        logger.info(f"Service IA initialisé - Base URL: {self.base_url}, Model: {self.model}, Timeout: {self.timeout}s")
    
    async def generate_program(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Génère un programme d'entraînement personnalisé avec le vrai modèle Ollama.
        Generates a personalized training program with the real Ollama model.
        
        Args:
            user_profile: Dictionnaire contenant le profil utilisateur / Dictionary containing user profile
            
        Returns:
            Dict[str, Any]: Programme d'entraînement généré / Generated training program
        """
        try:
            logger.info(f"Génération de programme pour utilisateur {user_profile.get('age', 'N/A')} ans")
            
            prompt = build_training_program_prompt(user_profile)
            logger.info(f"Prompt généré: {prompt[:200]}...")
            
            url = f"{self.base_url}/api/generate"
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            
            logger.info(f"🚀 Appel à l'IA avec timeout: {self.timeout}s")
            logger.info(f"📡 URL: {url}")
            logger.info(f"🤖 Modèle: {self.model}")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                
                ai_response = response.json()
                response_text = ai_response.get("response", "")
                
                logger.info(f"✅ Réponse IA reçue en {len(response_text)} caractères")
                
                program_data = self._parse_ai_response(response_text)
                
                logger.info("=" * 80)
                logger.info("🔍 PROMPT COMPLET ENVOYÉ À L'IA / COMPLETE PROMPT SENT TO AI:")
                logger.info("=" * 80)
                logger.info(prompt)
                logger.info("=" * 80)
                logger.info(f"📊 RÉPONSE IA COMPLÈTE / COMPLETE AI RESPONSE:")
                logger.info("=" * 80)
                logger.info(response_text)
                logger.info("=" * 80)
                
                return program_data
                
        except httpx.TimeoutException:
            logger.error(f"⏰ TIMEOUT: L'IA n'a pas répondu dans les {self.timeout}s alloués")
            raise Exception(f"Timeout de l'IA après {self.timeout}s")
        except httpx.HTTPStatusError as e:
            logger.error(f"❌ Erreur HTTP {e.response.status_code}: {e.response.text}")
            raise Exception(f"Erreur HTTP {e.response.status_code}")
        except Exception as e:
            logger.error(f"❌ Erreur inattendue: {str(e)}")
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
            cleaned_response = ai_response.strip()
            logger.info(f"Réponse IA brute: {cleaned_response[:200]}...")
            
            json_start = cleaned_response.find('{')
            json_end = cleaned_response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                logger.warning("Aucun JSON trouvé, création d'un programme par défaut")
                return self._create_default_program(cleaned_response)
            
            json_str = cleaned_response[json_start:json_end]
            logger.info(f"JSON extrait: {json_str[:100]}...")
            
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
            "tips": "Commencez progressivement et écoutez votre corps",
            "progression_plan": "Augmentez progressivement l'intensité"
        }
    
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
        
        if 'tips' in program_data and not isinstance(program_data['tips'], str):
            program_data['tips'] = str(program_data['tips'])
        
        if 'progression_plan' in program_data and not isinstance(program_data['progression_plan'], str):
            program_data['progression_plan'] = str(program_data['progression_plan'])
        
        if 'equipment_required' in program_data and isinstance(program_data['equipment_required'], list):
            program_data['equipment_required'] = ', '.join(program_data['equipment_required'])
        
        return program_data

ai_service = AIService() 