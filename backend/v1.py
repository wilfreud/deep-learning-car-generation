import numpy as np
import keras
from diffusers import StableDiffusionPipeline
import os
import random
import string

model_path = "v1.keras"
model = keras.saving.load_model(model_path)
print("✅ Modèle de prédiction chargé.")

# Charger Stable Diffusion
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
pipe.to("cuda")  # Utiliser le GPU si disponible
print("✅ Modèle Stable Diffusion chargé.")

def generate_random_filename(extension="png"):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + f".{extension}"

# Fonction pour prédire le prix et générer une image
def generate_car_image(features, description, promt="Une mercedes benz à 1500000 USD"):
    predicted_price = model.predict(np.array(features).reshape(1, -1))[0][0]
    prompt = f"Voiture {description}, estimée à {int(predicted_price)}€, design moderne et détaillé"
    
    print(f"🚗 Génération de l'image pour : {prompt}")
    image = pipe(prompt).images[0]
    
    # Afficher et sauvegarder l'image
    image.show()


    random_filename = generate_random_filename()
    image.save(random_filename)
    print(f"✅ Image générée et sauvegardée sous '{random_filename}'.")
    image.save("generated_car.png")
    print("✅ Image générée et sauvegardée sous 'generated_car.png'.")
    # Retourner le chemin du fichier généré
    generated_image_path = os.path.abspath("generated_car.png")
    print(f"📁 Chemin du fichier généré : {generated_image_path}")
    return generated_image_path

# Exemple d'utilisation : (mettre des vraies valeurs correspondant aux features du dataset)
features_example = [2015, 3, 1, 2, 1, 1, 4, 6]  # Ex : année, manufacturer, model, condition, etc.
description_example = "SUV noir, intérieur cuir, toit panoramique"

generate_car_image(features_example, description_example)
