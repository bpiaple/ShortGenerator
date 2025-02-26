import whisper
import os  # Pour la gestion des chemins de fichiers
import argparse  # Pour gérer les arguments de ligne de commande

def format_timestamp(seconds):
    """
    Formate un timestamp en secondes au format SRT (HH:MM:SS,mmm).
    
    Args:
        seconds (float): Temps en secondes.
        
    Returns:
        str: Timestamp formaté.
    """
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds_remainder = seconds % 60
    milliseconds = int((seconds_remainder - int(seconds_remainder)) * 1000)
    
    return f"{hours:02d}:{minutes:02d}:{int(seconds_remainder):02d},{milliseconds:03d}"

def generate_srt(segments):
    """
    Génère un contenu au format SRT à partir des segments fournis par Whisper.
    
    Args:
        segments (list): Liste des segments contenant le texte et le timing.
        
    Returns:
        str: Le contenu au format SRT.
    """
    srt_content = ""
    for i, segment in enumerate(segments, start=1):
        # Formatage du temps de début et de fin en format SRT (HH:MM:SS,mmm)
        start_time = format_timestamp(segment["start"])
        end_time = format_timestamp(segment["end"])
        
        # Ajout du numéro de segment, du timing et du texte
        srt_content += f"{i}\n{start_time} --> {end_time}\n{segment['text'].strip()}\n\n"
    
    return srt_content.strip()

def transcribe_audio(audio_file_path, model_size="base", language="fr", output_file=None, format="txt", quiet=False):
    """
    Transcrit un fichier audio en texte en utilisant Whisper.

    Args:
        audio_file_path (str): Chemin vers le fichier audio.
        model_size (str, optional): Taille du modèle Whisper.  Options: "tiny", "base", "small", "medium", "large".  Par défaut: "base".
        language (str, optional): Code de langue (par exemple, "fr" pour le français, "en" pour l'anglais). 
                                 Utilisez "auto" ou None pour la détection automatique de la langue. Par défaut: "fr".
        output_file (str, optional): Chemin du fichier de sortie. Si non spécifié, affiche la transcription sur la console.
        format (str, optional): Format de sortie ("txt" ou "srt"). Par défaut: "txt".
        quiet (bool, optional): Si True, supprime les messages dans le terminal. Par défaut: False.

    Returns:
        str: Le texte transcrit ou le contenu SRT si la transcription réussit, None sinon.
    """

    # Vérification de l'existence du fichier
    if not os.path.exists(audio_file_path):
        if not quiet:
            print(f"Erreur : Fichier audio non trouvé à l'emplacement : {audio_file_path}")
        return None

    try:
        # Chargement du modèle Whisper
        model = whisper.load_model(model_size)

        # Gestion de la détection automatique de langue
        whisper_language = None if language == "auto" else language
        
        # Transcription du fichier audio
        result = model.transcribe(audio_file_path, language=whisper_language)
        
        # Si la langue a été détectée automatiquement, afficher l'information
        if language == "auto" or language is None:
            detected_language = result.get("language", "inconnue")
            if not quiet:
                print(f"Langue détectée : {detected_language}")

        # Traitement en fonction du format demandé
        if format.lower() == "srt":
            content = generate_srt(result["segments"])
            output_type = "sous-titres SRT"
        else:
            content = result["text"]
            output_type = "transcription"

        # Gestion de la sortie (console ou fichier)
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(content)
            if not quiet:
                print(f"{output_type.capitalize()} enregistrée dans : {output_file}")
        else:
            if not quiet:
                print(f"{output_type.capitalize()} :")
                print(content)

        return content

    except Exception as e:
        if not quiet:
            print(f"Une erreur s'est produite lors de la transcription : {e}")
        return None
