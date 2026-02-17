# main.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CHATBOT FRANÇAIS ULTRA
Point d'entrée principal
"""

import sys
import os

# Ajouter le répertoire courant au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import MODELES, COLORS
from chatbot import FrenchChatbotPro
from utils import DisplayUtils

def menu_principal():
    """Affiche le menu principal"""
    display = DisplayUtils()
    display.afficher_banniere()
    
    print("\n📦 MODÈLES DISPONIBLES :")
    print("-" * 50)
    
    for key, (name, desc, details) in MODELES.items():
        print(f"  {COLORS['stats']}{key}. {name}{COLORS['reset']}")
        print(f"     📝 {desc}")
        print(f"     ⚡ {details}\n")
    
    print("-" * 50)
    
    choix = input(f"\n{COLORS['user']}➤ Choisis un modèle (1-5) [1 par défaut]: {COLORS['reset']}").strip() or "1"
    
    if choix in MODELES:
        model_name = MODELES[choix][0]
        print(f"\n{COLORS['system']}📦 Chargement du modèle: {model_name}{COLORS['reset']}")
        return model_name
    else:
        print(f"{COLORS['error']}❌ Choix invalide, utilisation du modèle par défaut{COLORS['reset']}")
        return MODELES["1"][0]

def main():
    """Fonction principale"""
    try:
        # Afficher le menu et obtenir le modèle
        model_name = menu_principal()
        
        # Créer et lancer le chatbot
        bot = FrenchChatbotPro(model_name)
        
        # Message de bienvenue
        bienvenues = [
            "Salut ! Je suis ton chatbot français préféré !",
            "Bonjour ! Prêt pour une conversation incroyable ?",
            "Coucou ! J'ai hâte de discuter avec toi !",
            "Hey ! L'aventure conversationnelle commence maintenant !"
        ]
        
        print(f"\n{COLORS['bot']}🤖 {random.choice(bienvenues)}{COLORS['reset']}")
        print(f"{COLORS['system']}💡 Tape 'aide' pour voir les commandes disponibles{COLORS['reset']}\n")
        
        # Lancer la conversation
        bot.run()
        
    except KeyboardInterrupt:
        print(f"\n\n{COLORS['system']}👋 Au revoir ! À bientôt !{COLORS['reset']}")
    except Exception as e:
        print(f"\n{COLORS['error']}❌ Erreur: {e}{COLORS['reset']}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())