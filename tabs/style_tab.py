import gradio as gr

def create_style_tab():
    """
    Crée l'onglet "Style" avec ses composants.
    """
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
        
    return style_tab