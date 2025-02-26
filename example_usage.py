from utils.srt_utils import transcribe_audio

# Exemple 1 : Création d'un fichier SRT à partir d'un fichier audio avec langue spécifiée
transcribe_audio(
    audio_file_path="D:/ShortGenerator/utils/audio.mp3",
    model_size="base",  # Options: "tiny", "base", "small", "medium", "large"
    language="fr",
    output_file="sous-titres_fr.srt",
    format="srt",
    quiet=True  # Pour supprimer les messages dans le terminal
)

# Exemple 2 : Création d'un fichier SRT avec détection automatique de la langue
transcribe_audio(
    audio_file_path="D:/ShortGenerator/utils/audio.mp3",
    model_size="base",  
    language="auto",  # Utiliser "auto" pour la détection automatique de la langue
    output_file="sous-titres_auto.srt",
    format="srt",
    quiet=False  # Afficher les messages pour voir la langue détectée
)
