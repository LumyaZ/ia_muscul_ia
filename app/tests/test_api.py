import requests
import json

# Test de l'endpoint health
print("=== Test Health Endpoint ===")
try:
    response = requests.get("http://127.0.0.1:8000/health")
    print(f"Status: {response.status_code}")
    print(f"Content: {response.text}")
except Exception as e:
    print(f"Error: {e}")

# Test de l'endpoint racine
print("\n=== Test Root Endpoint ===")
try:
    response = requests.get("http://127.0.0.1:8000/")
    print(f"Status: {response.status_code}")
    print(f"Content: {response.text}")
except Exception as e:
    print(f"Error: {e}")

# Test de l'endpoint de génération
print("\n=== Test Generate Training Program ===")
test_data = {
    "age": 25,
    "gender": "male",
    "experience_level": "beginner",
    "goals": "muscle_gain",
    "available_equipment": "dumbbells",
    "training_frequency": 3,
    "session_duration": 45
}

try:
    response = requests.post(
        "http://127.0.0.1:8000/generate-training-program",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    print(f"Content: {response.text}")
except Exception as e:
    print(f"Error: {e}") 