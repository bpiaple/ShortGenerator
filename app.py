import gradio as gr
from utils.api_config import setup_gemini_api
from utils.audio_utils import generate_audio
from utils.file_utils import generate_video
from utils.srt_utils import transcribe_audio
from static.custom_css import custom_css

# Import des onglets
from tabs.ideas_tab import create_ideas_tab
from tabs.legend_tab import create_legend_tab
from tabs.style_tab import create_style_tab
from tabs.images_tab import create_images_tab
from tabs.overlay_tab import create_overlay_tab
from tabs.hooks_tab import create_hooks_tab

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
                    # Création des onglets à partir des modules dédiés
                    ideas_tab, script_output, script_editor = create_ideas_tab()
                    legend_tab = create_legend_tab()
                    style_tab = create_style_tab()
                    images_tab = create_images_tab()
                    overlay_tab = create_overlay_tab()
                    hooks_tab = create_hooks_tab()
                
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
                    voice_list = gr.Dropdown(
                        choices=["Laura", "George", "River"],
                        label="Voix off",
                        value="George",
                        container=False
                    )
            
            # Colonne de droite pour la prévisualisation
            with gr.Column(scale=1):
                # Prévisualisation vidéo
                video_output = gr.Video(
                    label="Votre vidéo apparaîtra ici !",
                    elem_classes="video-preview"
                )
                
                audio_status = gr.Markdown("*L'audio apparaîtra ici après génération*")
                
                generate_video_btn = gr.Button(
                    "Générer la vidéo 60 ⚡",
                    elem_classes="primary-button"
                )
                
                # Prévisualisation audio
                audio_output = gr.Audio(
                    label="Prévisualisation audio",
                    type="filepath",
                    elem_classes="audio-preview"
                )
                
                # Ajout d'un élément pour les timestamps (sous-titres)
                timestamps_output = gr.File(
                    label="Timestamps générés (SRT)",
                    file_types=[".srt"],
                    interactive=False
                )

                generate_audio_btn = gr.Button(
                    "Générer l'audio 40 ⚡",
                    elem_classes="secondary-button"
                )

        # Événement pour générer la vidéo
        generate_video_btn.click(
            fn=generate_video,
            outputs=video_output
        )

        # Événement pour générer l'audio
        def process_audio_generation(script, voix):
            # Génération de l'audio
            audio_data, status_message = generate_audio(script, voix)
            
            # Si l'audio a été généré avec succès, générer également les timestamps
            if audio_data:
                # Générer les sous-titres SRT à partir de l'audio
                srt_output_path = audio_data.replace('.mp3', '.srt')
                srt_content = transcribe_audio(
                    audio_data, 
                    model_size="base", 
                    language="auto", 
                    output_file=srt_output_path,
                    format="srt", 
                    quiet=True
                )
                
                if srt_content:
                    status_message += "<br>✅ Timestamps générés avec succès!"
                else:
                    status_message += "<br>❌ Échec de la génération des timestamps."
                    srt_output_path = None
                
                return audio_data, status_message, srt_output_path
            
            # En cas d'échec de la génération audio
            return None, status_message, None
            
        generate_audio_btn.click(
            fn=process_audio_generation,
            inputs=[script_editor, voice_list],
            outputs=[audio_output, audio_status, timestamps_output]
        )

    demo.launch()


if __name__ == "__main__":
    main()