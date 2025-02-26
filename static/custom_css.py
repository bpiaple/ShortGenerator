"""
Ce module contient le CSS personnalisé pour l'interface utilisateur du générateur de shorts.
"""

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