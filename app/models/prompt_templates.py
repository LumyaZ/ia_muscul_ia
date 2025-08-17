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
    
    # Extraction et traduction des données utilisateur
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
    
    # Traduction des niveaux d'expérience
    experience_translation = {
        'Débutant': 'beginner',
        'Intermédiaire': 'intermediate', 
        'Avancé': 'advanced',
        'Expert': 'expert'
    }
    
    # Traduction des objectifs
    goal_translation = {
        'Prise de masse': 'muscle_gain',
        'Perte de poids': 'weight_loss',
        'Force': 'strength',
        'Endurance': 'endurance',
        'Tonification': 'toning',
        'Réhabilitation': 'rehabilitation',
        'Performance sportive': 'sports_performance'
    }
    
    # Traduction des préférences d'entraînement
    preference_translation = {
        'Musculation': 'strength_training',
        'Cardio': 'cardio',
        'CrossFit': 'crossfit',
        'Yoga': 'yoga',
        'Pilates': 'pilates',
        'Fonctionnel': 'functional_training'
    }
    
    # Traduction de l'équipement
    equipment_translation = {
        'Salle de sport complète': 'full_gym',
        'Équipement basique': 'basic_equipment',
        'Poids libres': 'free_weights',
        'Machines': 'machines',
        'Sans équipement': 'bodyweight_only',
        'Équipement maison': 'home_equipment'
    }
    
    # Application des traductions
    translated_experience = experience_translation.get(experience_level, experience_level.lower())
    translated_goal = goal_translation.get(main_goal, main_goal.lower())
    translated_preference = preference_translation.get(training_preference, training_preference.lower())
    translated_equipment = equipment_translation.get(equipment, equipment.lower())
    
    # Calcul du BMI
    bmi = "N/A"
    if isinstance(weight, (int, float)) and isinstance(height, (int, float)) and height > 0:
        height_m = height / 100
        bmi = round(weight / (height_m ** 2), 1)
    
    # Détermination de la fréquence et durée des sessions
    sessions_per_week = 3
    if '3 fois' in str(session_frequency):
        sessions_per_week = 3
    elif '4 fois' in str(session_frequency):
        sessions_per_week = 4
    elif '5 fois' in str(session_frequency):
        sessions_per_week = 5
    elif '6 fois' in str(session_frequency):
        sessions_per_week = 6
    
    session_duration_minutes = 60
    if '45' in str(session_duration):
        session_duration_minutes = 45
    elif '90' in str(session_duration):
        session_duration_minutes = 90
    elif '120' in str(session_duration):
        session_duration_minutes = 120
    
    return f"""
You are an expert fitness trainer. Generate a personalized training program in JSON format for:

PROFILE:
- Age: {age} years old
- Gender: {gender}
- Experience Level: {translated_experience} (translated from: {experience_level})
- Main Goal: {translated_goal} (translated from: {main_goal})
- Training Preference: {translated_preference} (translated from: {training_preference})
- Available Equipment: {translated_equipment} (translated from: {equipment})
- Session Frequency: {sessions_per_week} times per week
- Session Duration: {session_duration_minutes} minutes
- BMI: {bmi}

REQUIREMENTS:
- Create a {translated_experience}-level program
- Focus on {translated_goal}
- Use {translated_equipment} equipment
- Include 4-6 exercises per session
- Adapt sets/reps based on experience level
- Ensure safety and progression

RESPOND ONLY WITH VALID JSON starting with {{ and ending with }}.

REQUIRED FORMAT:
{{
    "name": "Programme {translated_goal} - {translated_experience}",
    "description": "Programme personnalisé {translated_goal} pour {gender} de {age} ans, niveau {translated_experience}",
    "category": "{translated_preference}",
    "difficulty_level": "{translated_experience}",
    "target_audience": "{translated_experience} level - {age} years old",
    "duration_weeks": 8,
    "sessions_per_week": {sessions_per_week},
    "estimated_duration_minutes": {session_duration_minutes},
    "equipment_required": "{translated_equipment}",
    "exercises": [
        {{
            "name": "Exercise Name in French",
            "description": "Description in French",
            "muscle_group": "MUSCLE_GROUP",
            "equipment": "EQUIPMENT_TYPE",
            "difficulty_level": "{translated_experience}",
            "sets_count": 3,
            "reps_count": "10-12",
            "rest": "90 seconds",
            "notes": "Important notes in French"
        }}
    ]
}}

EXERCISE GUIDELINES:
- Beginner: 2-3 sets, 10-15 reps, longer rest periods
- Intermediate: 3-4 sets, 8-12 reps, moderate rest
- Advanced: 4-5 sets, 6-10 reps, shorter rest periods
- Expert: 5+ sets, 4-8 reps, minimal rest

MUSCLE GROUPS TO COVER:
- CHEST (pectoraux)
- BACK (dos) 
- LEGS (jambes)
- SHOULDERS (épaules)
- ARMS (bras)
- CORE (abdominaux)

EQUIPMENT TYPES:
- BODYWEIGHT (poids du corps)
- DUMBBELLS (haltères)
- BARBELL (barre)
- MACHINE (machine)
- RESISTANCE_BANDS (élastiques)
- CARDIO (cardio)

IMPORTANT: Ensure all exercise names and descriptions are in French, but use English for technical terms like muscle groups and equipment types.
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