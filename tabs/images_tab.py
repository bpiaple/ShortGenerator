import gradio as gr
from utils.file_utils import load_images

def create_images_tab():
    """
    Crée l'onglet "Images" avec ses composants.
    """
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
                
    return images_tab