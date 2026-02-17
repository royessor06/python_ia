# utils.py
import time
import sys
from datetime import datetime, timedelta
from typing import Optional
import random

class DisplayUtils:
    """Utilitaires d'affichage"""
    
    @staticmethod
    def typing_effect(texte: str, delai: float = 0.03):
        """Affiche du texte avec effet de frappe"""
        for char in texte:
            print(char, end='', flush=True)
            time.sleep(delai)
        print()
    
    @staticmethod
    def spinner_animation(secondes: int = 2, texte: str = "Chargement"):
        """Affiche une animation spinner"""
        spin = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        fin = time.time() + secondes
        
        i = 0
        while time.time() < fin:
            sys.stdout.write(f'\r{spin[i % len(spin)]} {texte}...')
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        sys.stdout.write('\r' + ' ' * 20 + '\r')
    
    @staticmethod
    def afficher_banniere():
        """Affiche une bannière de bienvenue"""
        banniere = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     🤖 CHATBOT FRANÇAIS - ÉDITION ULTRA V2.0 🤖         ║
║                                                          ║
║         Intelligence Artificielle Conversationnelle     ║
║                    Avec Personnalité !                  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""
        print(banniere)

class StatsUtils:
    """Utilitaires de statistiques"""
    
    @staticmethod
    def calculer_temps_conversation(debut: datetime) -> str:
        """Calcule la durée de conversation"""
        duree = datetime.now() - debut
        minutes = duree.total_seconds() / 60
        
        if minutes < 1:
            return "moins d'une minute"
        elif minutes < 60:
            return f"{int(minutes)} minutes"
        else:
            heures = minutes / 60
            return f"{heures:.1f} heures"
    
    @staticmethod
    def generer_rapport(stats: dict) -> str:
        """Génère un rapport de statistiques"""
        rapport = []
        rapport.append("📊 RAPPORT DE CONVERSATION")
        rapport.append("=" * 40)
        
        for cle, valeur in stats.items():
            if cle != "debut_conversation":
                rapport.append(f"{cle.replace('_', ' ').title()}: {valeur}")
        
        rapport.append("=" * 40)
        return "\n".join(rapport)

class TexteUtils:
    """Utilitaires de traitement de texte"""
    
    @staticmethod
    def nettoyer_texte(texte: str) -> str:
        """Nettoie un texte"""
        # Enlever les espaces multiples
        texte = ' '.join(texte.split())
        
        # Enlever les caractères spéciaux en trop
        import re
        texte = re.sub(r'[^\w\s\?\.,!;:\'\"\-@#$%^&*()]', '', texte)
        
        return texte.strip()
    
    @staticmethod
    def extraire_mots_cles(texte: str, n: int = 5) -> list:
        """Extrait les mots-clés d'un texte"""
        mots = texte.lower().split()
        mots_importants = []
        
        # Mots à ignorer
        stopwords = ['le', 'la', 'les', 'un', 'une', 'des', 'et', 'ou', 
                    'mais', 'donc', 'car', 'pour', 'dans', 'sur', 'avec']
        
        for mot in mots:
            if mot not in stopwords and len(mot) > 3:
                mots_importants.append(mot)
        
        # Retourner les n premiers
        return list(set(mots_importants))[:n]
    
    @staticmethod
    def formatter_temps(timestamp: str) -> str:
        """Formate un timestamp"""
        try:
            dt = datetime.fromisoformat(timestamp)
            maintenant = datetime.now()
            
            if dt.date() == maintenant.date():
                return f"Aujourd'hui à {dt.strftime('%H:%M')}"
            elif dt.date() == maintenant.date() - timedelta(days=1):
                return f"Hier à {dt.strftime('%H:%M')}"
            else:
                return dt.strftime('%d/%m/%Y à %H:%M')
        except:
            return timestamp