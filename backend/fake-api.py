"""
DOCUMENTATION

Lance FastAPI avec Uvicorn: uvicorn fake-api:app --reload
"""
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


# Initialiser FastAPI
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (replace "*" with your frontend URL in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

class CarRequest(BaseModel):
    # features: list
    description: str
    price: int

@app.get("/")
def healthcheck():
    return "It works"

# Endpoint pour générer une image
@app.post("/generate")
def generate_car_image(request: CarRequest):
    print(request.description, request.price)
    # Retourner l'URL de l'image
    return {"image_url": "https://www.electromobiliste.fr/wp-content/uploads/2022/01/tesla-roadster.jpg"}

