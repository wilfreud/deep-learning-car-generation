"""
DOCUMENTATION

Lance FastAPI avec Uvicorn: uvicorn api:app --reload
"""
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import random
import string
import os
import keras
from diffusers import StableDiffusionPipeline
from fastapi.middleware.cors import CORSMiddleware

# Initialiser FastAPI
app = FastAPI()

# Activer CORS pour React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Charger le modèle de prédiction
model_path = "v1.keras"
model = keras.saving.load_model(model_path)
print("✅ Modèle de prédiction chargé.")

# Charger Stable Diffusion
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
try:
    pipe.to("cuda")  # Utiliser le GPU si disponible
except:
    print("🪧 Echec de la tentative d'utilisation du GPU (CUDA), fallback sur le CPU")
print("✅ Modèle Stable Diffusion chargé.")

# Fonction pour générer un nom de fichier aléatoire
def generate_random_filename(extension="png"):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + f".{extension}"

# Modèle de requête (seule la description est requise)
class CarRequest(BaseModel):
    description: str  # Description détaillée du véhicule

# Endpoint de test
@app.get("/")
def healthcheck():
    return {"status": "It works"}

# Endpoint pour générer une image
@app.post("/generate")
def generate_car_image(request: CarRequest):
    # Générer des features factices (jusqu'à ce qu'on intègre du NLP)
    dummy_features = [2015, 3, 1, 2, 1, 1, 4, 6]  # Exemples de valeurs encodées

    # Prédire le prix avec le modèle
    predicted_price = model.predict(np.array(dummy_features).reshape(1, -1))[0][0]
    print(f"💰 Prix prédit : {int(predicted_price)}€")

    # Construire le prompt pour Stable Diffusion
    prompt = f"Voiture {request.description}, estimée à {int(predicted_price)}€, design moderne et détaillé"
    
    print(f"🚗 Génération de l'image pour : {prompt}")
    image = pipe(prompt).images[0]

    # Sauvegarder l'image avec un nom unique
    filename = generate_random_filename()
    image_path = f"static/{filename}"
    os.makedirs("static", exist_ok=True)  # Créer le dossier si nécessaire
    image.save(image_path)
    print(f"✅ Image générée et sauvegardée sous '{image_path}'.")

    # Retourner l'URL de l'image et le prix prédit
    return {"image_url": f"http://localhost:8000/{image_path}", "predicted_price": int(predicted_price)}
