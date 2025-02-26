import gradio as gr

def create_overlay_tab():
    """
    Crée l'onglet "Overlay" avec ses composants.
    """
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
        
    return overlay_tab