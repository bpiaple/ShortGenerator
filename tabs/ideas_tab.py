import gradio as gr
import google.generativeai as genai
from utils.api_config import setup_gemini_api

def generate_script_with_gemini(prompt, language, style):
    """
    Génère un script avec l'API Gemini basé sur les paramètres fournis.
    """
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

        # Définition des événements spécifiques à cet onglet
        def update_script(generated_script):
            # Assurons-nous que le format markdown est correct
            if not generated_script.strip().startswith("#") and not generated_script.strip().startswith("*"):
                # Ajoutons un formatage minimal si aucun n'est présent
                generated_script = f"# Script généré\n\n{generated_script}"
            
            return generated_script, generated_script
        
        generate_script_btn.click(
            fn=generate_script_with_gemini,
            inputs=[prompt, language, style],
            outputs=gr.State("")  # État temporaire
        ).then(
            fn=update_script,
            inputs=gr.State(""),  # L'état sera remplacé par le résultat de generate_script_with_gemini
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