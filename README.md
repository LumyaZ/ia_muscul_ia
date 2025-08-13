# Service IA - Muscul IA

Service Python FastAPI pour la génération de programmes d'entraînement personnalisés avec l'IA.

## 🚀 Fonctionnalités

- Génération de programmes d'entraînement personnalisés
- Intégration avec Ollama (modèles locaux gratuits)
- API REST complète avec documentation automatique
- Validation des données et gestion d'erreurs
- Logging détaillé et structuré
- Tests unitaires et d'intégration complets

## 📋 Prérequis

- Python 3.11+
- Ollama installé et configuré
- Modèle Llama 2 ou autre modèle compatible

## 🛠️ Installation

### 1. Cloner le projet
```bash
cd ai_muscul_ia
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Configurer l'environnement
```bash
cp env.example .env
# Éditer .env selon vos besoins
```

### 4. Installer et configurer Ollama

#### Sur Windows :
```bash
# Télécharger depuis https://ollama.ai/
# Ou utiliser winget
winget install Ollama.Ollama
```

#### Sur Linux/macOS :
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 5. Télécharger un modèle
```bash
ollama pull llama2
# Ou pour un modèle plus léger
ollama pull llama2:7b
```

## 🏃‍♂️ Démarrage

### Mode développement
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Mode production
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Avec Docker
```bash
docker build -t ai-muscul-ia .
docker run -p 8000:8000 ai-muscul-ia
```

## 📚 API Documentation

Une fois le service démarré, la documentation est disponible à :
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc
- **Documentation technique** : `docs/API_DOCUMENTATION.md`

## 🧪 Tests

### Tests unitaires (C2.2.2)
```bash
# Tests du service IA
pytest app/tests/test_ai_service.py

# Tests avec couverture
pytest app/tests/test_ai_service.py --cov=app.services
```

### Tests d'intégration (C2.2.4)
```bash
# Tests des endpoints
pytest app/tests/test_integration.py

# Tous les tests
pytest app/tests/
```

### Tests des endpoints IA
Les tests des endpoints IA se trouvent dans `back_muscul_ia/scripts/` :
- **`test_ai_endpoints.py`** - Tests complets des endpoints
- **`test_ai_request.json`** - Données de test
- **`test-ollama-direct.py`** - Test direct d'Ollama

### Exécution des tests
```bash
# Depuis la racine du projet
python back_muscul_ia/scripts/test_ai_endpoints.py
python back_muscul_ia/scripts/test-ollama-direct.py
```

## 🔧 Endpoints

### POST /generate-training-program
Génère un programme d'entraînement personnalisé.

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

**Response :**
```json
{
  "name": "Programme Prise de Masse Débutant",
  "description": "Programme complet pour débutants...",
  "category": "Musculation",
  "difficulty_level": "Débutant",
  "target_audience": "Débutants en musculation",
  "duration_weeks": 8,
  "sessions_per_week": 3,
  "estimated_duration_minutes": 60,
  "equipment_required": "Salle de sport"
}
```

### GET /health
Vérifie l'état du service.

### POST /test-ai-connection
Teste la connexion avec le service IA.

### POST /simple-question
Pose une question simple à l'IA.

## 🔗 Intégration avec le Backend

Le service IA est conçu pour être appelé par le backend Spring Boot :

```java
@Service
public class ExternalAIService {
    
    @Value("${ai.service.url:http://localhost:8000}")
    private String aiServiceUrl;
    
    public TrainingProgramDto generateProgramWithAI(Long userId) {
        // Récupérer les données utilisateur
        UserProfile userProfile = userProfileService.getByUserId(userId);
        TrainingInfo trainingInfo = trainingInfoService.getByUserId(userId);
        
        // Préparer les données pour l'IA
        Map<String, Object> userData = buildUserDataForAI(userProfile, trainingInfo);
        
        // Appeler le service IA
        ResponseEntity<Map> response = restTemplate.postForEntity(
            aiServiceUrl + "/generate-training-program",
            userData,
            Map.class
        );
        
        return createTrainingProgramFromAIResponse(response.getBody(), userId);
    }
}
```

## 🐳 Docker Compose

Pour déployer l'ensemble du projet :

```yaml
version: '3.8'

services:
  ai-service:
    build: ./ai_muscul_ia
    ports:
      - "8000:8000"
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    depends_on:
      - ollama

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama

volumes:
  ollama_data:
```

## 🔍 Troubleshooting

### Problème de connexion à Ollama
```bash
# Vérifier qu'Ollama fonctionne
curl http://localhost:11434/api/tags

# Redémarrer Ollama
ollama serve
```

### Modèle non trouvé
```bash
# Lister les modèles disponibles
ollama list

# Télécharger un modèle
ollama pull llama2
```

### Erreur de parsing JSON
- Vérifier que le modèle IA génère bien du JSON valide
- Ajuster les paramètres de température et top_p si nécessaire

## 📝 Logs

Les logs sont disponibles dans la console et incluent :
- Requêtes reçues
- Appels à l'IA
- Erreurs de parsing
- Temps de réponse
- Profils utilisateurs complets

## 📊 Conformité aux blocs

### C2.2.2 - Tests unitaires
- ✅ Tests complets du service IA
- ✅ Tests de parsing JSON
- ✅ Tests de validation des données
- ✅ Tests de gestion d'erreurs

### C2.2.4 - Tests d'intégration
- ✅ Tests des endpoints FastAPI
- ✅ Tests de validation des modèles
- ✅ Tests de gestion des erreurs HTTP

### C2.4.1 - Documentation technique
- ✅ Documentation API complète
- ✅ Architecture détaillée
- ✅ Guide d'utilisation
- ✅ Exemples de code

### C4.2.1 - Logging des anomalies
- ✅ Logging structuré
- ✅ Détection d'erreurs
- ✅ Traçabilité complète

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature
3. Commiter les changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet fait partie de Muscul IA. 