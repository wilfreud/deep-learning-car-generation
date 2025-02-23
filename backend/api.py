"""
DOCUMENTATION

Lance FastAPI avec Uvicorn: uvicorn api:app --reload
"""
from fastapi import FastAPI
from pydantic import BaseModel
import random
import string
from diffusers import StableDiffusionPipeline
from fastapi.middleware.cors import CORSMiddleware

# Initialiser FastAPI
app = FastAPI()

# Activer CORS pour que React puisse appeler l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autoriser tous les domaines (mettre ton URL en prod)
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Autoriser tous les headers
)

# Charger Stable Diffusion
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
pipe.to("cuda")  # Utiliser le GPU si disponible
print("✅ Modèle Stable Diffusion chargé.")

# Fonction pour générer un nom de fichier aléatoire
def generate_random_filename(extension="png"):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + f".{extension}"

# Modèle de requête
class CarRequest(BaseModel):
    description: str
    price: float

# Endpoint de test
@app.get("/")
def healthcheck():
    return {"status": "It works"}

# Endpoint pour générer une image
@app.post("/generate")
def generate_car_image(request: CarRequest):
    prompt = f"Voiture {request.description}, estimée à {int(request.price)}€, design moderne et détaillé"
    
    print(f"🚗 Génération de l'image pour : {prompt}")
    image = pipe(prompt).images[0]

    # Sauvegarder l'image avec un nom unique
    filename = generate_random_filename()
    image_path = f"static/{filename}"
    image.save(image_path)
    print(f"✅ Image générée et sauvegardée sous '{image_path}'.")

    # Retourner l'URL de l'image
    return {"image_url": f"http://localhost:8000/{image_path}"}
