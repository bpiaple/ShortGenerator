import gradio as gr

def create_hooks_tab():
    """
    Crée l'onglet "Hooks" avec ses composants.
    """
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
        
        # Fonction pour activer/désactiver le champ CTA
        def toggle_cta(is_checked):
            return gr.Textbox.update(visible=is_checked)
            
        call_to_action.change(fn=toggle_cta, inputs=call_to_action, outputs=cta_text)
        
    return hooks_tab