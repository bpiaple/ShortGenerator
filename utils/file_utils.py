from PIL import Image
import glob
import os

def load_images(template_dir="Templates"):
    """Chargement des images depuis le dossier Templates."""
    # Charger toutes les images jpg dans le dossier Templates
    image_paths = sorted(glob.glob(f'{template_dir}/*.jpg'))
    images = []
    for path in image_paths:
        try:
            img = Image.open(path)
            images.append(img)
        except Exception as e:
            print(f"Erreur lors du chargement de {path}: {e}")
    return images

def generate_video():
    """Simulation de la génération de vidéo."""
    # Fonction à développer pour générer réellement une vidéo
    return "Vidéo en cours de génération..."