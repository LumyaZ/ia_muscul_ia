from pydantic import BaseModel, Field
from typing import Optional

class UserProfile(BaseModel):
    """Modèle pour le profil utilisateur / Model for user profile"""
    age: int = Field(..., description="Âge de l'utilisateur / User age", ge=13, le=100)
    gender: str = Field(..., description="Genre de l'utilisateur / User gender")
    weight: float = Field(..., description="Poids en kg / Weight in kg", ge=30.0, le=300.0)
    height: float = Field(..., description="Taille en cm / Height in cm", ge=100.0, le=250.0)
    experience_level: str = Field(..., description="Niveau d'expérience / Experience level")
    main_goal: str = Field(..., description="Objectif principal / Main goal")
    session_frequency: str = Field(..., description="Fréquence d'entraînement / Training frequency")
    session_duration: str = Field(..., description="Durée de session / Session duration")
    equipment: str = Field(..., description="Équipement disponible / Available equipment")
    training_preference: str = Field(..., description="Préférences d'entraînement / Training preferences")
    
    body_fat_percentage: Optional[float] = Field(None, description="Pourcentage de graisse corporelle / Body fat percentage", ge=5.0, le=50.0)
    phone_number: Optional[str] = Field(None, description="Numéro de téléphone / Phone number")
    first_name: Optional[str] = Field(None, description="Prénom / First name")
    last_name: Optional[str] = Field(None, description="Nom de famille / Last name")

class TrainingProgramResponse(BaseModel):
    """Modèle pour la réponse d'un programme d'entraînement généré / Model for generated training program response"""
    name: str = Field(..., description="Nom du programme / Program name")
    description: str = Field(..., description="Description du programme / Program description", min_length=10, max_length=1000)
    category: str = Field(..., description="Catégorie du programme / Program category")
    difficulty_level: str = Field(..., description="Niveau de difficulté / Difficulty level")
    target_audience: str = Field(..., description="Public cible / Target audience")
    duration_weeks: int = Field(..., description="Durée en semaines / Duration in weeks", ge=1, le=52)
    sessions_per_week: int = Field(..., description="Sessions par semaine / Sessions per week", ge=1, le=7)
    estimated_duration_minutes: int = Field(..., description="Durée estimée par session en minutes / Estimated duration per session in minutes", ge=15, le=300)
    equipment_required: str = Field(..., description="Équipement requis / Required equipment")
    
    exercises: Optional[list] = Field(None, description="Liste des exercices recommandés / List of recommended exercises")
    tips: Optional[str] = Field(None, description="Conseils et recommandations / Tips and recommendations")
    progression_plan: Optional[str] = Field(None, description="Plan de progression / Progression plan")

class AIHealthResponse(BaseModel):
    """Modèle pour la réponse de santé du service IA / Model for AI service health response"""
    status: str = Field(..., description="Statut du service / Service status")
    ai_response: Optional[str] = Field(None, description="Réponse du service IA / AI service response")
    error: Optional[str] = Field(None, description="Message d'erreur si applicable / Error message if applicable") 