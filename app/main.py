from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import logging
import httpx

from .api.models import UserProfile, TrainingProgramResponse
from .services.ai_service import ai_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Muscul IA - Service IA",
    description="Service IA pour la génération de programmes d'entraînement personnalisés / AI Service for personalized training program generation",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware pour logger toutes les requêtes / Middleware to log all requests"""
    logger.info(f"Request: {request.method} {request.url}")
    logger.info(f"Headers: {dict(request.headers)}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response

@app.get("/")
async def root():
    """Point d'entrée principal du service IA / Main entry point of the AI service"""
    logger.info("Root endpoint called")
    return {
        "message": "Service IA Muscul IA / Muscul IA AI Service",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Vérification de l'état du service / Service health check"""
    return {"status": "healthy", "service": "ai-muscul-ia"}

@app.post("/generate-training-program", response_model=TrainingProgramResponse)
async def generate_training_program(user_profile: UserProfile):
    """
    Génère un programme d'entraînement personnalisé basé sur le profil utilisateur.
    Generates a personalized training program based on user profile.
    
    Args:
        user_profile: Profil utilisateur avec toutes les informations nécessaires / User profile with all necessary information
        
    Returns:
        TrainingProgramResponse: Programme d'entraînement généré / Generated training program
    """
    try:
        logger.info(f"Génération de programme pour utilisateur: {user_profile.age} ans, {user_profile.experience_level}")
        
        logger.info("=" * 80)
        logger.info("👤 PROFIL UTILISATEUR RECU / USER PROFILE RECEIVED:")
        logger.info("=" * 80)
        logger.info(f"Age: {user_profile.age}")
        logger.info(f"Gender: {user_profile.gender}")
        logger.info(f"Height: {user_profile.height} cm")
        logger.info(f"Weight: {user_profile.weight} kg")
        logger.info(f"Body Fat: {user_profile.body_fat_percentage}%")
        logger.info(f"Experience Level: {user_profile.experience_level}")
        logger.info(f"Main Goal: {user_profile.main_goal}")
        logger.info(f"Equipment: {user_profile.equipment}")
        logger.info(f"Session Duration: {user_profile.session_duration}")
        logger.info(f"Session Frequency: {user_profile.session_frequency}")
        logger.info(f"Training Preference: {user_profile.training_preference}")
        logger.info("=" * 80)
        
        program = await ai_service.generate_program(user_profile.dict())
        
        logger.info(f"Programme généré avec succès: {program.get('name', 'N/A')}")
        return TrainingProgramResponse(**program)
        
    except Exception as e:
        logger.error(f"Erreur lors de la génération du programme: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur lors de la génération du programme: {str(e)}"
        )

@app.post("/test-ai-connection")
async def test_ai_connection():
    """Teste la connexion avec le service IA (Ollama) / Tests connection with AI service (Ollama)"""
    try:
        test_prompt = "Réponds simplement 'OK' si tu reçois ce message."
        response = await ai_service.test_connection(test_prompt)
        return {"status": "success", "ai_response": response}
    except Exception as e:
        logger.error(f"Erreur de connexion IA: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur de connexion avec le service IA: {str(e)}"
        )

class SimpleQuestionRequest(BaseModel):
    question: str

@app.post("/simple-question")
async def simple_question(request: SimpleQuestionRequest):
    """
    Endpoint simple pour poser une question à l'IA.
    Simple endpoint to ask a question to the AI.
    
    Args:
        question: Question simple à poser à l'IA / Simple question to ask the AI
        
    Returns:
        dict: Réponse de l'IA / AI response
    """
    try:
        logger.info(f"Question simple reçue: {request.question}")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{ai_service.base_url}/api/generate",
                json={
                    "model": ai_service.model,
                    "prompt": request.question,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "max_tokens": 500
                    }
                }
            )
            
            if response.status_code != 200:
                raise Exception(f"Erreur Ollama (HTTP {response.status_code}): {response.text}")
            
            ai_response = response.json()
            
            if "response" not in ai_response:
                raise Exception("Réponse invalide d'Ollama")
            
            response_text = ai_response["response"]
            logger.info(f"Réponse IA reçue: {response_text[:100]}...")
            
            return {
                "status": "success",
                "question": request.question,
                "response": response_text
            }
            
    except Exception as e:
        logger.error(f"Erreur lors de la question simple: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la question: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 