from elevenlabs.client import ElevenLabs
import uuid
import os
from utils.api_config import setup_elevenlabs_api

def convert_voice_id(voix: str) -> str:
    """Convertit le nom de la voix en identifiant ElevenLabs."""
    if voix == "River":
        return "SAz9YHcvj6GT2YYXdXww"
    elif voix == "Laura":
        return "FGY2WhTYpPnrIDTdsKH5"
    elif voix == "George":
        return "JBFqnCBsd6RMkjVDRZzb"

def generate_audio(script, voix):
    """Génère un fichier audio à partir d'un script en utilisant ElevenLabs."""
    try:
        # Vérification de l'API ElevenLabs
        if not setup_elevenlabs_api():
            return None, "Erreur: Clé API ElevenLabs non configurée. Veuillez ajouter une clé API dans le fichier .env"
        
        # Si le script est au format Markdown, extraction du texte brut
        # Suppression des balises Markdown simples pour une meilleure lecture audio
        clean_text = script
        if script.startswith("#") or "**" in script or "- " in script:
            # Supprimer les titres (#)
            clean_text = clean_text.replace("#", "")
            # Supprimer les marqueurs de gras (**)
            clean_text = clean_text.replace("**", "")
            # Remplacer les puces par des phrases
            clean_text = clean_text.replace("- ", ". ")
            # Supprimer les sauts de ligne excessifs
            clean_text = " ".join(line.strip() for line in clean_text.splitlines() if line.strip())
        
        # Initialiser le client ElevenLabs
        api_key = os.getenv("ELEVENLABS_API_KEY")
        audio_client = ElevenLabs(api_key=api_key)
        
        voix_id = convert_voice_id(voix)
        
        # Conversion texte en audio
        audio = audio_client.text_to_speech.convert(
            voice_id=voix_id,
            output_format="mp3_44100_128",
            text=clean_text,
            model_id="eleven_multilingual_v2"
        )

        # Generating a unique file name for the output MP3 file
        temp_dir = os.path.join(os.getcwd(), "temp_audio")
        os.makedirs(temp_dir, exist_ok=True)
        
        saved_audio_path = os.path.join(temp_dir, f"{uuid.uuid4()}.mp3")
        
        # Writing the audio stream to the file
        with open(saved_audio_path, "wb") as f:
            for chunk in audio:
                if chunk:
                    f.write(chunk)

        print(f"Un nouveau fichier audio a été enregistré avec succès: {saved_audio_path}")

        # Return the path of the saved audio file and a success message
        return saved_audio_path, "Audio généré avec succès!"

    except Exception as e:
        print(f"Erreur détaillée: {str(e)}")
        return None, f"Erreur lors de la génération de l'audio: {str(e)}"