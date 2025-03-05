from email.mime import image
from exceptiongroup import catch
import gradio as gr
from utils.file_utils import load_images

from diffusers import DiffusionPipeline

image_generator = DiffusionPipeline.from_pretrained("CompVis/ldm-text2im-large-256")
# image_generator.device = "cpu"
image_generator.to("cpu")

def create_images_tab():
    """
    Crée l'onglet "Images" avec ses composants.
    """
    with gr.TabItem("🖼️ Images") as images_tab:
        gr.Markdown("## Images et médias")
        
        with gr.Tabs():
            with gr.TabItem("Télécharger"):
                image_upload = gr.File(label="Télécharger vos propres images", file_types=["image"])
            
            with gr.TabItem("Générer"):
                with gr.Row():
                    # Composant d'image à gauche pour afficher l'image générée
                    generated_image = gr.Image(label="Image générée", interactive=False)
                    
                    # Contrôles à droite
                    with gr.Column():
                        image_prompt = gr.TextArea(
                            label="Description de l'image à générer", 
                            placeholder="Un coucher de soleil sur la plage...",
                            elem_classes="input-box"
                        )
                        negative_promt = gr.TextArea(
                            label="Inverser la description", 
                            placeholder="Image basse resolution...",
                            elem_classes="input-box"
                        )
                        generate_image_btn = gr.Button("Générer une image", elem_classes="secondary-button")
                
                # Fonction pour générer l'image
                def generate_image(prompt, negative):
                    try:
                        image = image_generator(prompt, negative).images[0]
                        return image
                    except Exception as e:
                        return f"Erreur lors de la génération de l'image: {str(e)}"
                
                # Connection du bouton à la fonction de génération
                generate_image_btn.click(
                    fn=generate_image, 
                    inputs=[image_prompt, negative_promt], 
                    outputs=[generated_image]
                )
   
    return images_tab