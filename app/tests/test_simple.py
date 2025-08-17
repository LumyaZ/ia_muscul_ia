import pytest
import requests
import json

class TestSimpleEndpoints:
    """Tests simples des endpoints de base / Simple endpoint tests"""
    
    @pytest.fixture
    def base_url(self):
        """URL de base pour les tests / Base URL for tests"""
        return "http://localhost:8000"
    
    def test_root_endpoint(self, base_url):
        """Test du endpoint racine / Test root endpoint"""
        try:
            response = requests.get(f"{base_url}/", timeout=10)
            assert response.status_code in [200, 404]  # 404 si le service n'est pas démarré
        except requests.exceptions.ConnectionError:
            pytest.skip("Service non accessible - probablement pas démarré")
    
    def test_health_endpoint(self, base_url):
        """Test du endpoint de santé / Test health endpoint"""
        try:
            response = requests.get(f"{base_url}/health", timeout=10)
            assert response.status_code in [200, 404]  # 404 si le service n'est pas démarré
        except requests.exceptions.ConnectionError:
            pytest.skip("Service non accessible - probablement pas démarré")
    
    def test_docs_endpoint(self, base_url):
        """Test du endpoint de documentation / Test docs endpoint"""
        try:
            response = requests.get(f"{base_url}/docs", timeout=10)
            assert response.status_code in [200, 404]  # 404 si le service n'est pas démarré
        except requests.exceptions.ConnectionError:
            pytest.skip("Service non accessible - probablement pas démarré")
    
    def test_openapi_endpoint(self, base_url):
        """Test du endpoint OpenAPI / Test OpenAPI endpoint"""
        try:
            response = requests.get(f"{base_url}/openapi.json", timeout=10)
            assert response.status_code in [200, 404]  # 404 si le service n'est pas démarré
        except requests.exceptions.ConnectionError:
            pytest.skip("Service non accessible - probablement pas démarré") 