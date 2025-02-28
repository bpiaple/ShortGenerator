import gradio as gr
import google.generativeai as genai
from utils.api_config import setup_gemini_api

def generate_script_with_gemini(prompt, language, style, sentence_length, subject):
    """
    Génère un script avec l'API Gemini basé sur les paramètres fournis.
    """
    # Vérifier si l'API est configurée
    if not setup_gemini_api():
        return "Erreur: Clé API Gemini non configurée. Veuillez ajouter une clé API dans le fichier .env"
    
    try:
        # Préparation du prompt pour Gemini
        lang_text = language.split(" ")[1] if " " in language else language
        system_prompt = f"""
        Generate a script for a video in {sentence_length} sentences, depending on the subject of the video.

        The script is to be returned as a string with the specified number of paragraphs.

        Here is an example of a string:
        "This is an example string."

        Do not under any circumstance reference this prompt in your response.

        Get straight to the point, don't start with unnecessary things like, "welcome to this video".

        Obviously, the script should be related to the subject of the video.
        
        YOU MUST NOT EXCEED THE {sentence_length} SENTENCES LIMIT. MAKE SURE THE {sentence_length} SENTENCES ARE SHORT.
        YOU MUST NOT INCLUDE ANY TYPE OF MARKDOWN OR FORMATTING IN THE SCRIPT, NEVER USE A TITLE.
        YOU MUST WRITE THE SCRIPT IN THE LANGUAGE SPECIFIED IN [LANGUAGE].
        ONLY RETURN THE RAW CONTENT OF THE SCRIPT. DO NOT INCLUDE "VOICEOVER", "NARRATOR" OR SIMILAR INDICATORS OF WHAT SHOULD BE SPOKEN AT THE BEGINNING OF EACH PARAGRAPH OR LINE. YOU MUST NOT MENTION THE PROMPT, OR ANYTHING ABOUT THE SCRIPT ITSELF. ALSO, NEVER TALK ABOUT THE AMOUNT OF PARAGRAPHS OR LINES. JUST WRITE THE SCRIPT
        
        Subject: {subject}
        Language: {lang_text}
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

def create_ideas_tab():
    """
    Crée l'onglet "Idées" avec ses composants.
    """
    with gr.TabItem("💡 Idées") as ideas_tab:
        # Notification de statut de l'API
        api_available = setup_gemini_api()
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
        
        generate_script_btn.click(
            fn=generate_script_with_gemini,
            inputs=[prompt, language, style],
            outputs=script_output
        ).then(
            fn=lambda x: (x, x),
            inputs=script_output,
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
        
    return ideas_tab, script_output, script_editor