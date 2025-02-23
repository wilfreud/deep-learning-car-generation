# Installer spaCy et télécharger le modèle français
# !pip install spacy
# !python -m spacy download fr_core_news_sm

import spacy
import re

# Charger le modèle spaCy
nlp = spacy.load("fr_core_news_sm")

# Fonction pour extraire les features
def extract_features(description):
    features = {
        "manufacturer": None,
        "model": None,
        "year": None,
        "condition": None,
        "cylinders": None,
        "size": None,
        "type": None,
        "paint_color": None,
        "state": None
    }

    # Exemple d'extraction avec des expressions régulières
    year_match = re.search(r"\b(19|20)\d{2}\b", description)
    if year_match:
        features["year"] = int(year_match.group())

    # Exemple d'extraction de marque et modèle (à adapter)
    doc = nlp(description)
    for ent in doc.ents:
        if ent.label_ == "ORG":  # Marque (ex: Ford, Toyota)
            features["manufacturer"] = ent.text
        elif ent.label_ == "PRODUCT":  # Modèle (ex: F-150, Corolla)
            features["model"] = ent.text

    # Exemple d'extraction de la couleur
    colors = ["rouge", "bleu", "noir", "blanc", "gris", "argent"]
    for color in colors:
        if color in description.lower():
            features["paint_color"] = color
            break

    # Retourner les features extraites
    return features

# Appliquer la fonction sur la colonne "description"
df["features"] = df["description"].apply(extract_features)

# Convertir les features en colonnes séparées
df = pd.concat([df, df["features"].apply(pd.Series)], axis=1)

# Supprimer la colonne "features" (devenue inutile)
df.drop(columns=["features"], inplace=True)

# Afficher un aperçu
print(df.head())