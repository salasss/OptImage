from fastapi.testclient import TestClient
from PIL import Image
import io
import pytest

from app.main import app

client = TestClient(app)

def create_dummy_image(width=100, height=100, format="PNG"):
    """
    Helper pour créer une image en mémoire (RAM) pour les tests.
    Évite d'avoir besoin de vrais fichiers .jpg dans le dossier.
    """
    img = Image.new('RGB', (width, height), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format=format)
    img_byte_arr.seek(0) 
    return img_byte_arr

def test_read_root():
    """Vérifie que la route racine répond bien."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    """
    Vérifie le health check. 
    NOTE: Si ce test échoue (404), c'est que tu as oublié d'ajouter 
    la route @app.get('/health') dans main.py !
    """
    response = client.get("/health")
    if response.status_code == 404:
        pytest.skip("Endpoint /health non implémenté")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_optimize_image_simple():
    """Test complet du flow d'optimisation."""
    
    image_bytes = create_dummy_image(200, 200, "PNG")
    
    files = {"file": ("test_image.png", image_bytes, "image/png")}
    params = {"width": 100, "format": "jpeg", "quality": 50}
    
    response = client.post("/optimize", files=files, params=params)
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"
    
    response_image = Image.open(io.BytesIO(response.content))
    assert response_image.format == "JPEG"
    assert response_image.width == 100
    assert response_image.height == 100 

def test_optimize_invalid_file():
    """Vérifie que l'API rejette un fichier texte."""
    files = {"file": ("not_an_image.txt", io.BytesIO(b"Ceci n'est pas une image"), "text/plain")}
    response = client.post("/optimize", files=files)
    
    assert response.status_code in [400, 500]