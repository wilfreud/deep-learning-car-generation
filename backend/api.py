"""
DOCUMENTATION

Lance FastAPI avec Uvicorn: uvicorn api:app --reload
"""
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import keras
from diffusers import StableDiffusionPipeline
import random
import string
import keras

# Initialiser FastAPI
app = FastAPI()

# Charger le modèle de prédiction
model_path = "v1.keras"
model = keras.saving.load_model(model_path)
print("✅ Modèle de prédiction chargé.")

# Charger Stable Diffusion
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
pipe.to("cuda")  # Utiliser le GPU si disponible
print("✅ Modèle Stable Diffusion chargé.")

# Fonction pour générer un nom de fichier aléatoire
def generate_random_filename(extension="png"):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + f".{extension}"

# Modèle de requête
class CarRequest(BaseModel):
    features: list
    description: str

# Endpoint pour générer une image
@app.post("/generate")
def generate_car_image(request: CarRequest):
    predicted_price = model.predict(np.array(request.features).reshape(1, -1))[0][0]
    prompt = f"Voiture {request.description}, estimée à {int(predicted_price)}€, design moderne et détaillé"
    
    print(f"🚗 Génération de l'image pour : {prompt}")
    image = pipe(prompt).images[0]

    # Sauvegarder l'image avec un nom unique
    filename = generate_random_filename()
    image_path = f"static/{filename}"
    image.save(image_path)
    print(f"✅ Image générée et sauvegardée sous '{image_path}'.")

    # Retourner l'URL de l'image
    return {"image_url": f"http://localhost:8000/{image_path}"}

