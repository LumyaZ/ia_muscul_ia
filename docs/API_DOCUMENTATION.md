# Documentation API - Service IA Muscul IA

## Vue d'ensemble / Overview

Le service IA de Muscul IA fournit des endpoints pour la génération de programmes d'entraînement personnalisés utilisant l'intelligence artificielle via Ollama.

The Muscul IA AI service provides endpoints for generating personalized training programs using artificial intelligence via Ollama.

## Endpoints

### GET /
**Description :** Point d'entrée principal du service / Main service entry point  
**Réponse / Response :**
```json
{
  "message": "Service IA Muscul IA",
  "version": "1.0.0",
  "status": "running"
}
```

### GET /health
**Description :** Vérification de l'état du service / Service health check  
**Réponse / Response :**
```json
{
  "status": "healthy",
  "service": "ai-muscul-ia"
}
```

### POST /generate-training-program
**Description :** Génère un programme d'entraînement personnalisé / Generates personalized training program  
**Body :**
```json
{
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
```

**Réponse / Response :**
```json
{
  "name": "Programme Prise de Masse Débutant",
  "description": "Programme personnalisé pour débutants...",
  "category": "Musculation",
  "difficulty_level": "Débutant",
  "target_audience": "Débutants en musculation",
  "duration_weeks": 8,
  "sessions_per_week": 3,
  "estimated_duration_minutes": 60,
  "equipment_required": "Salle de sport"
}
```

### POST /test-ai-connection
**Description :** Teste la connexion avec le service IA / Tests AI service connection

### POST /simple-question
**Description :** Pose une question simple à l'IA / Asks simple question to AI  
**Body :**
```json
{
  "question": "Votre question ici"
}
```

## Codes d'erreur / Error Codes

- **200 :** Succès / Success
- **422 :** Erreur de validation / Validation error
- **500 :** Erreur interne du serveur / Internal server error

## Tests / Testing

```bash
# Tests unitaires / Unit tests
pytest app/tests/test_ai_service.py

# Tests d'intégration / Integration tests
pytest app/tests/test_integration.py

# Tous les tests / All tests
pytest app/tests/
```

## Configuration / Configuration

### Variables d'environnement / Environment Variables

- `OLLAMA_BASE_URL` : URL du service Ollama (défaut: http://localhost:11434)
- `OLLAMA_MODEL` : Modèle IA à utiliser (défaut: llama2:7b)
- `AI_TIMEOUT` : Timeout en millisecondes (défaut: 300000)

### Démarrage / Startup

```bash
# Mode développement / Development mode
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Mode production / Production mode
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Architecture / Architecture

### Structure des fichiers / File Structure

```
ai_muscul_ia/
├── app/
│   ├── main.py              # Point d'entrée FastAPI / FastAPI entry point
│   ├── api/
│   │   └── models.py        # Modèles Pydantic / Pydantic models
│   ├── services/
│   │   └── ai_service.py    # Service IA / AI service
│   ├── models/
│   │   └── prompt_templates.py  # Templates de prompts / Prompt templates
│   └── tests/
│       ├── test_ai_service.py   # Tests unitaires / Unit tests
│       └── test_integration.py  # Tests d'intégration / Integration tests
├── docs/
│   └── API_DOCUMENTATION.md # Cette documentation / This documentation
├── requirements.txt         # Dépendances Python / Python dependencies
└── Dockerfile              # Configuration Docker / Docker configuration
```

### Flux de données / Data Flow

1. **Réception de requête** / Request Reception
   - Validation des données avec Pydantic
   - Logging de la requête

2. **Génération de prompt** / Prompt Generation
   - Construction du prompt personnalisé
   - Adaptation selon le profil utilisateur

3. **Appel IA** / AI Call
   - Communication avec Ollama
   - Gestion des timeouts et erreurs

4. **Parsing de réponse** / Response Parsing
   - Extraction du JSON
   - Validation et nettoyage des données

5. **Retour de réponse** / Response Return
   - Formatage de la réponse
   - Logging du résultat

## Monitoring et logs / Monitoring and Logs

### Logs disponibles / Available Logs

- **Requêtes entrantes** / Incoming requests
- **Profils utilisateurs** / User profiles
- **Prompts générés** / Generated prompts
- **Réponses IA** / AI responses
- **Erreurs et exceptions** / Errors and exceptions

### Métriques / Metrics

- Temps de réponse des endpoints
- Taux de succès des générations
- Erreurs de parsing JSON
- Timeouts IA

## Sécurité / Security

### Validation des données / Data Validation

- Validation automatique avec Pydantic
- Contraintes sur les valeurs (âge, poids, taille)
- Sanitisation des entrées

### Gestion des erreurs / Error Handling

- Gestion centralisée des exceptions
- Messages d'erreur appropriés
- Logging des erreurs pour debugging

## Évolutions futures / Future Evolutions

- Support de plusieurs modèles IA
- Cache des programmes générés
- Métriques avancées
- Interface d'administration
- Tests de charge 