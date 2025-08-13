from typing import Dict, Any

def build_training_program_prompt(user_profile: Dict[str, Any]) -> str:
    """
    Construit un prompt personnalisé pour la génération de programme d'entraînement.
    Builds a personalized prompt for training program generation.
    
    Args:
        user_profile: Dictionnaire contenant le profil utilisateur / Dictionary containing user profile
        
    Returns:
        str: Prompt personnalisé pour l'IA / Personalized prompt for AI
    """
    
    age = user_profile.get('age', 'N/A')
    gender = user_profile.get('gender', 'N/A')
    weight = user_profile.get('weight', 'N/A')
    height = user_profile.get('height', 'N/A')
    experience_level = user_profile.get('experience_level', 'N/A')
    main_goal = user_profile.get('main_goal', 'N/A')
    session_frequency = user_profile.get('session_frequency', 'N/A')
    session_duration = user_profile.get('session_duration', 'N/A')
    equipment = user_profile.get('equipment', 'N/A')
    training_preference = user_profile.get('training_preference', 'N/A')
    body_fat_percentage = user_profile.get('body_fat_percentage', 'N/A')
    
    bmi = "N/A"
    if isinstance(weight, (int, float)) and isinstance(height, (int, float)) and height > 0:
        height_m = height / 100
        bmi = round(weight / (height_m ** 2), 1)
    
    return f"""
Tu es un expert fitness français. Génère un programme d'entraînement personnalisé.

PROFIL UTILISATEUR COMPLET / COMPLETE USER PROFILE:
- Âge: {age} ans, Genre: {gender}
- Poids: {weight}kg, Taille: {height}cm, IMC: {bmi}
- Niveau: {experience_level}, Objectif: {main_goal}
- Fréquence: {session_frequency}, Durée: {session_duration}
- Équipement: {equipment}
- Préférence: {training_preference}
- % Graisse corporelle: {body_fat_percentage}

RÈGLES DE TRADUCTION / TRANSLATION RULES:
- Niveaux: {experience_level} → Débutant/Intermédiaire/Avancé
- Objectifs: {main_goal} → Perte de Poids/Prise de Muscle/Maintien/Performance/Fitness Général
- Équipement: {equipment} → Poids du corps/Haltères/Matériel complet
- Fréquence: {session_frequency} → 1-2/3-4/5+ sessions/semaine
- Durée: {session_duration} → 30/45/60 minutes

ADAPTATIONS SPÉCIFIQUES / SPECIFIC ADAPTATIONS:
- Si IMC > 25: Privilégier cardio et exercices poids du corps
- Si niveau débutant: Exercices simples, progression douce
- Si niveau avancé: Exercices complexes, intensité élevée
- Si objectif perte de poids: Cardio + musculation
- Si objectif prise de muscle: Musculation + nutrition

RÉPONDS UNIQUEMENT AVEC CE JSON / RESPOND ONLY WITH THIS JSON:

{{
    "name": "Programme [OBJECTIF_TRADUIT] [NIVEAU_TRADUIT]",
    "description": "Programme personnalisé pour {main_goal} niveau {experience_level}, adapté à votre profil ({age} ans, {weight}kg, {height}cm). Inclut {session_frequency} sessions de {session_duration} minutes par semaine.",
    "category": "[CATÉGORIE_ADAPTÉE]",
    "difficulty_level": "[NIVEAU_TRADUIT]",
    "target_audience": "Niveau [NIVEAU_TRADUIT] - {age} ans, {gender}",
    "duration_weeks": 6,
    "sessions_per_week": [NOMBRE_SESSIONS],
    "estimated_duration_minutes": [DURÉE_MINUTES],
    "equipment_required": "[ÉQUIPEMENT_TRADUIT]",
    "exercises": [
        {{
            "name": "Squats",
            "sets": 3,
            "reps": "10-12",
            "rest": "90s",
            "notes": "Exercice de base pour renforcer les jambes"
        }},
        {{
            "name": "Pompes",
            "sets": 3,
            "reps": "8-10",
            "rest": "90s",
            "notes": "Développe la force du haut du corps"
        }},
        {{
            "name": "Gainage",
            "sets": 3,
            "reps": "30s",
            "rest": "60s",
            "notes": "Renforce le core et améliore la posture"
        }}
    ]
}}
"""

def build_simple_test_prompt() -> str:
    """Prompt simple pour tester la connexion IA / Simple prompt to test AI connection"""
    return "Réponds simplement 'OK' si tu reçois ce message de test."

def build_program_validation_prompt(program_json: str) -> str:
    """
    Prompt pour valider un programme généré.
    Prompt to validate a generated program.
    
    Args:
        program_json: JSON du programme à valider / JSON of program to validate
        
    Returns:
        str: Prompt de validation / Validation prompt
    """
    return f"""
Tu es un expert en fitness. Valide ce programme d'entraînement :

{program_json}

Réponds uniquement par "VALID" si le programme est cohérent et sécurisé, 
ou "INVALID: [raison]" s'il y a des problèmes.
""" 