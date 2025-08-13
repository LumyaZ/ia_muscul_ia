import requests
import json

def test_endpoint(url, method="GET", data=None):
    """Test un endpoint et affiche les détails"""
    print(f"\n=== Test {method} {url} ===")
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Content: {response.text[:200]}...")
        
        if response.status_code == 200:
            try:
                json_data = response.json()
                print(f"JSON: {json.dumps(json_data, indent=2)}")
            except:
                pass
                
    except Exception as e:
        print(f"Error: {e}")

# Test des différents endpoints
test_endpoint("http://localhost:8000/")
test_endpoint("http://localhost:8000/health")
test_endpoint("http://localhost:8000/docs")
test_endpoint("http://localhost:8000/openapi.json") 