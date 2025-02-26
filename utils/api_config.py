import os
from dotenv import load_dotenv
import google.generativeai as genai

# Chargement des variables d'environnement
load_dotenv()

# Configuration de l'API ElevenLabs
def setup_elevenlabs_api():
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("⚠️ Clé API ElevenLabs non trouvée. Veuillez définir ELEVENLABS_API_KEY dans un fichier .env")
        return False
    
    # Configuration réussie
    return True

# Configuration de l'API Gemini
def setup_gemini_api():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠️ Clé API Gemini non trouvée. Veuillez définir GEMINI_API_KEY dans un fichier .env")
        return False
    
    genai.configure(api_key=api_key)
    return True