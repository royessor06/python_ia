# config.py
import os
from pathlib import Path

# Chemins
BASE_DIR = Path(__file__).parent
SOUVENIRS_FILE = BASE_DIR / "souvenirs_bot.json"
CONNAISSANCES_FILE = BASE_DIR / "connaissances.json"
PERSONNALITES_FILE = BASE_DIR / "personalities.json"

# Modèles disponibles
MODELES = {
    "1": ("microsoft/DialoGPT-small", "Dialogue conversationnel", "Léger et rapide"),
    "2": ("gpt2", "GPT-2 standard", "Polyvalent"),
    "3": ("asi/gpt-fr-cased-small", "Spécialisé français", "Meilleur en français"),
    "4": ("distilgpt2", "Version légère", "Ultra rapide"),
    "5": ("microsoft/DialoGPT-medium", "Dialogue avancé", "Plus intelligent mais plus lent"),
}

# Paramètres par défaut
DEFAULT_MAX_HISTORY = 10
DEFAULT_TEMPERATURE = 0.85
DEFAULT_TOP_P = 0.92
DEFAULT_REPETITION_PENALTY = 1.15

# Couleurs pour le terminal (si supporté)
COLORS = {
    'reset': '\033[0m',
    'bold': '\033[1m',
    'user': '\033[94m',      # Bleu
    'bot': '\033[92m',       # Vert
    'system': '\033[93m',    # Jaune
    'error': '\033[91m',     # Rouge
    'stats': '\033[95m',     # Magenta
}