# Fichier : api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import pandas as pd
import joblib
from tensorflow import keras
from diffusers import StableDiffusionPipeline
import torch
import uuid
import os

# Configuration de l'API
app = FastAPI()

# Créer le dossier "static" si inexistant
os.makedirs("static", exist_ok=True)

# Modèle Pydantic pour les entrées
class CarFeatures(BaseModel):
    manufacturer: str
    model: str
    year: int
    condition: str
    cylinders: str
    size: str
    type: str
    paint_color: str
    state: str

# Chargement du modèle et du préprocesseur
model = keras.models.load_model("car_price_model.keras")
preprocessor = joblib.load("preprocessor.joblib")

# Chargement de Stable Diffusion (à exécuter une fois)
pipe = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    torch_dtype=torch.float16
)
pipe = pipe.to("cuda")

@app.post("/predict")
async def predict(features: CarFeatures):
    try:
        # Conversion en DataFrame pour le préprocessing
        input_df = pd.DataFrame([features.dict()])
        
        # Préprocessing
        processed_input = preprocessor.transform(input_df)
        
        # Prédiction
        predicted_price = model.predict(processed_input).flatten()[0]
        
        # Génération d'image avec Stable Diffusion
        prompt = (
            f"Realistic {features.year} {features.manufacturer} {features.model}, "
            f"{features.paint_color}, {features.condition} condition, "
            f"price {predicted_price:.0f}$"
        )
        image = pipe(prompt, guidance_scale=9.5, num_inference_steps=50).images[0]
        
        # Sauvegarde de l'image
        image_name = f"static/{uuid.uuid4()}.png"
        image.save(image_name)
        
        return {
            "predicted_price": float(predicted_price),
            "image_url": f"http://localhost:8000/{image_name}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Pour lancer l'API : uvicorn api:app --reload