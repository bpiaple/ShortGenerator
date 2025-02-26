import gradio as gr

def create_legend_tab():
    """
    Crée l'onglet "Légende" avec ses composants.
    """
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
        
    return legend_tab