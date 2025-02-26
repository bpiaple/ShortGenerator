import gradio as gr
from PIL import Image
import glob
import google.generativeai as genai
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import os
from dotenv import load_dotenv



# Chargement des variables d'environnement (pour la clé API)
load_dotenv()

# Configuration de l'API ElevenLabs
def setup_elevenlabs_api():
    """
    The function `setup_elevenlabs_api` checks for the presence of an API key for ElevenLabs and prompts
    the user to define it if not found.
    :return: The function `setup_elevenlabs_api()` is returning `False` if the API key for ElevenLabs is
    not found in the environment variables.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("⚠️ Clé API ElevenLabs non trouvée. Veuillez définir ELEVENLABS_API_KEY dans un fichier .env")
        return False

# Configuration de l'API Gemini
def setup_gemini_api():
    """
    The function `setup_gemini_api` checks for the presence of a Gemini API key and configures the API
    if the key is found.
    :return: The function `setup_gemini_api()` returns a boolean value - `True` if the Gemini API key is
    successfully configured, and `False` if the API key is not found.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠️ Clé API Gemini non trouvée. Veuillez définir GEMINI_API_KEY dans un fichier .env")
        return False
    
    genai.configure(api_key=api_key)
    return True

# Générer un script avec Gemini
def generate_script_with_gemini(prompt, language, style):
    # Vérifier si l'API est configurée
    if not setup_gemini_api():
        return "Erreur: Clé API Gemini non configurée. Veuillez ajouter une clé API dans le fichier .env"
    
    try:
        # Préparation du prompt pour Gemini
        lang_text = language.split(" ")[1] if " " in language else language
        system_prompt = f"""Tu es un expert en création de contenu pour les réseaux sociaux.
        Génère un script court et accrocheur pour une vidéo {lang_text} au format court.
        Le script doit suivre un {style} et être optimisé pour capter l'attention rapidement.
        Format: Introduction accrocheuse, contenu principal avec 3-4 points clés, conclusion avec call-to-action.
        Longueur: 60-90 secondes de narration (environ 150-200 mots).
        
        Formate ta réponse en Markdown avec:
        - Des titres pour les sections (utilise # pour les titres)
        - Des listes à puces pour les points clés (utilise - pour les puces)
        - Du texte en gras pour les moments importants (utilise ** autour du texte)
        - Des émojis appropriés pour rendre le script plus vivant

        IMPORTANT: Le script doit etre en 1 seul bloc de texte, sans sauts de ligne, juste un paragraphe continu.
        """
        
        user_prompt = prompt

        # Utilisation du modèle Gemini Pro (utilisons le modèle standard qui est plus stable)
        try:
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            response = model.generate_content([system_prompt, user_prompt])
            return response.text
        except:
            # Fallback sur un autre modèle si le premier échoue
            model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-01-21')
            response = model.generate_content([system_prompt, user_prompt])
            return response.text
            
    except Exception as e:
        return f"Erreur lors de la génération du script: {str(e)}"


def load_images():
    # Charger toutes les images jpg dans le dossier Templates
    image_paths = sorted(glob.glob('Templates/*.jpg'))
    images = []
    for path in image_paths:
        try:
            img = Image.open(path)
            images.append(img)
        except Exception as e:
            print(f"Erreur lors du chargement de {path}: {e}")
    return images


def generate_video():
    # Simulation de la génération de vidéo
    return "Vidéo en cours de génération..."

def generate_audio(script: str):
    audio_client = ElevenLabs()
    audio = audio_client.text_to_speech.convert(
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        output_format="mp3_44100_128",
        text=script,
        model_id="eleven_multilingual_v2"
    )
    # Simulation de la génération de l'audio
    return audio

# Définition du style personnalisé
custom_css = """
.container {
    max-width: 1200px;
    margin: 0 auto;
}

.primary-button {
    background: linear-gradient(90deg, #00c853, #00e676) !important;
    border: none !important;
    padding: 12px 24px !important;
    border-radius: 8px !important;
    color: white !important;
    font-weight: bold !important;
    transition: all 0.3s !important;
}

.primary-button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(0, 200, 0, 0.2) !important;
}

.secondary-button {
    border: 2px solid #00c853 !important;
    background: transparent !important;
    color: #00c853 !important;
    padding: 10px 20px !important;
    border-radius: 8px !important;
    transition: all 0.3s !important;
}

.secondary-button:hover {
    background: rgba(0, 200, 0, 0.1) !important;
}

.script-markdown {
    background: #f9f9f9 !important;
    border: 1px solid #eaeaea !important;
    border-radius: 8px !important;
    padding: 15px !important;
    max-height: 400px !important;
    overflow-y: auto !important;
}

.script-markdown h1, .script-markdown h2, .script-markdown h3 {
    color: #00b341 !important;
    margin-top: 10px !important;
    margin-bottom: 10px !important;
}

.script-markdown ul {
    margin-left: 20px !important;
}

.script-markdown strong {
    color: #00a03e !important;
}

.video-preview {
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
}
"""

def main():
    # Vérification initiale de l'API Gemini
    api_available = setup_gemini_api()
    
    with gr.Blocks(
        theme=gr.themes.Soft(
            primary_hue="green",
            neutral_hue="zinc",
            font=["Inter", "ui-sans-serif", "system-ui"]
        ),
        css=custom_css
    ) as demo:
        gr.Markdown("# 🎬 Générateur de Shorts Vidéo")
        
        # État pour stocker le script généré
        script_raw = gr.State("")
        
        with gr.Row():
            # Colonne de gauche pour les paramètres (avec tabbed interface)
            with gr.Column(scale=2):
                # Création des différents onglets
                with gr.Tabs() as tabs:

                    # Onglet Idées
                    with gr.TabItem("💡 Idées") as ideas_tab:
                        # Notification de statut de l'API
                        if not api_available:
                            gr.Markdown("""⚠️ **API Gemini non configurée**. 
                            Veuillez créer un fichier `.env` avec votre clé API au format: `GEMINI_API_KEY=votre_clé_api`""", 
                            elem_classes="warning-message")
                        
                        # Zone de saisie de l'idée
                        prompt = gr.TextArea(
                            placeholder="exemple : Générez moi une vidéo sur la motivation...",
                            label="Donnez une idée qui va servir de base à votre vidéo",
                            elem_classes="input-box"
                        )

                        with gr.Row():
                            # Sélection du style et de la langue
                            with gr.Column(scale=2):
                                style = gr.Dropdown(
                                    choices=["Style de script personnalisé 📝", "Style informatif", "Style humoristique", "Style émotionnel"],
                                    label="Style",
                                    value="Style de script personnalisé 📝",
                                    container=False
                                )
                            
                            with gr.Column(scale=3):
                                with gr.Row():
                                    language = gr.Dropdown(
                                        choices=["🇫🇷 Français", "🇺🇸 Anglais", "🇪🇸 Espagnol", "🇩🇪 Allemand"],
                                        label="Langue",
                                        value="🇫🇷 Français",
                                        container=False
                                    )
                                    generate_script_btn = gr.Button(
                                        "Générer le script 10 ⚡",
                                        elem_classes="primary-button"
                                    )

                        # Zone du script en markdown
                        gr.Markdown("### Votre script 📄")
                        
                        # Affichage du script formaté en markdown
                        script_output = gr.Markdown(
                            elem_classes="script-markdown",
                            value="*Le script de votre vidéo apparaîtra ici*"
                        )
                        
                        # Bouton pour éditer le script manuellement
                        with gr.Accordion("Modifier le script", open=False):
                            script_editor = gr.Textbox(
                                label="Éditeur de script (format Markdown)",
                                lines=10,
                                placeholder="# Titre\n\n**Texte en gras**\n\n- Point 1\n- Point 2\n\n## Conclusion"
                            )
                            apply_edit_btn = gr.Button("Appliquer les modifications", elem_classes="secondary-button")
                    
                    # Onglet Légende
                    with gr.TabItem("📝 Légende") as legend_tab:
                        gr.Markdown("## Options de légende")
                        legend_style = gr.Dropdown(
                            choices=["Standard", "Minimaliste", "Détaillée", "Citation"],
                            label="Style de légende",
                            value="Standard"
                        )
                        legend_size = gr.Slider(minimum=8, maximum=36, value=16, step=2, label="Taille de police")
                        legend_color = gr.ColorPicker(label="Couleur du texte", value="#FFFFFF")
                        legend_position = gr.Dropdown(
                            choices=["Bas", "Haut", "Centre", "Personnalisé"],
                            label="Position de la légende",
                            value="Bas"
                        )

                    # Onglet Style
                    with gr.TabItem("🎨 Style") as style_tab:
                        gr.Markdown("## Options de style")
                        video_style = gr.Dropdown(
                            choices=["Moderne", "Vintage", "Minimaliste", "Dynamique", "Cinématique"],
                            label="Style visuel",
                            value="Moderne"
                        )
                        video_ratio = gr.Radio(
                            choices=["16:9", "9:16 (Stories/Shorts)", "1:1 (Carré)", "4:5 (Instagram)"],
                            label="Ratio d'aspect",
                            value="9:16 (Stories/Shorts)"
                        )
                        video_duration = gr.Slider(minimum=15, maximum=60, value=30, step=5, label="Durée (secondes)")

                    # Onglet Images
                    with gr.TabItem("🖼️ Images") as images_tab:
                        gr.Markdown("## Images et médias")
                        
                        with gr.Tabs():
                            with gr.TabItem("Télécharger"):
                                image_upload = gr.File(label="Télécharger vos propres images", file_types=["image"])
                            
                            with gr.TabItem("Banque d'images"):
                                image_search = gr.Textbox(label="Rechercher des images", placeholder="nature, business, technologie...")
                                image_gallery = gr.Gallery(load_images(), label="Images disponibles")
                            
                            with gr.TabItem("Générer"):
                                image_prompt = gr.Textbox(label="Description de l'image à générer", placeholder="Un coucher de soleil sur la plage...")
                                generate_image_btn = gr.Button("Générer une image", elem_classes="secondary-button")

                    # Onglet Overlay
                    with gr.TabItem("⚙️ Overlay") as overlay_tab:
                        gr.Markdown("## Options d'overlay")
                        overlay_type = gr.Dropdown(
                            choices=["Aucun", "Logo", "Filigrane", "Sous-titres animés"],
                            label="Type d'overlay",
                            value="Aucun"
                        )
                        overlay_position = gr.Dropdown(
                            choices=["Coin supérieur droit", "Coin supérieur gauche", "Coin inférieur droit", "Coin inférieur gauche", "Centre"],
                            label="Position",
                            value="Coin inférieur droit"
                        )
                        overlay_opacity = gr.Slider(minimum=0.1, maximum=1.0, value=0.8, step=0.1, label="Opacité")

                    # Onglet Hooks
                    with gr.TabItem("🎣 Hooks") as hooks_tab:
                        gr.Markdown("## Hooks et appels à l'action")
                        hook_style = gr.Dropdown(
                            choices=["Question captivante", "Statistique surprenante", "Citation inspirante", "Challenge"],
                            label="Style de hook",
                            value="Question captivante"
                        )
                        hook_position = gr.Radio(
                            choices=["Début de vidéo", "Fin de vidéo", "Les deux"],
                            label="Position du hook",
                            value="Début de vidéo"
                        )
                        call_to_action = gr.Checkbox(label="Ajouter un appel à l'action", value=True)
                        cta_text = gr.Textbox(
                            label="Texte de l'appel à l'action", 
                            placeholder="Abonne-toi pour plus de contenu !",
                            visible=True
                        )
                
                gr.Markdown("---")

                # Boutons communs à tous les onglets
                with gr.Row():
                    # Utilisation de gr.File au lieu de gr.Audio pour une meilleure sélection de fichiers MP3
                    music_file = gr.File(
                        label="🎵 Sélectionner une musique de fond",
                        file_types=["audio/mpeg", ".mp3"],
                        elem_id="music-picker",
                        elem_classes="secondary-button"
                    )
                    voice_btn = gr.Button(
                        "🎙 Sélectionner la voix off",
                        elem_classes="secondary-button"
                    )
            
            # Colonne de droite pour la prévisualisation
            with gr.Column(scale=1):
                # Prévisualisation vidéo
                video_output = gr.Video(
                    label="Votre vidéo apparaîtra ici !",
                    elem_classes="video-preview"
                )

                # Prévisualisation audio
                audio_output = gr.Audio(
                    label="Votre musique de fond apparaîtra ici !",
                    elem_classes="video-preview"
                )
                
                generate_video_btn = gr.Button(
                    "Générer la vidéo 60 ⚡",
                    elem_classes="primary-button"
                )

                generate_audio_btn = gr.Button(
                    "Générer l'audio 40 ⚡",
                    elem_classes="secondary-button"
                )

        # Événements pour la génération du script
        def update_script(generated_script):
            # Assurons-nous que le format markdown est correct
            if not generated_script.strip().startswith("#") and not generated_script.strip().startswith("*"):
                # Ajoutons un formatage minimal si aucun n'est présent
                generated_script = f"# Script généré\n\n{generated_script}"
            
            return generated_script, generated_script
        
        generate_script_btn.click(
            fn=generate_script_with_gemini,
            inputs=[prompt, language, style],
            outputs=script_raw
        ).then(
            fn=update_script,
            inputs=script_raw,
            outputs=[script_output, script_editor]
        )
        
        # Événement pour appliquer les modifications manuelles au script
        def apply_script_edit(edited_script):
            return edited_script
            
        apply_edit_btn.click(
            fn=apply_script_edit,
            inputs=script_editor,
            outputs=script_output
        )

        generate_video_btn.click(
            fn=generate_video,
            outputs=video_output
        )

        generate_audio_btn.click(
            fn=generate_audio,
            inputs=script_output,
            outputs=audio_output
        )

        # Activation/désactivation de l'appel à l'action
        def toggle_cta(is_checked):
            return gr.Textbox.update(visible=is_checked)
            
        call_to_action.change(fn=toggle_cta, inputs=call_to_action, outputs=cta_text)

    demo.launch()


if __name__ == "__main__":
    main()