# sentiment.py
import re
from collections import Counter

class SentimentAnalyzer:
    """
    Analyseur de sentiment pour les conversations
    """
    
    def __init__(self):
        self.mots_positifs = {
            'super': 2, 'génial': 2, 'cool': 1, 'content': 2, 'heureux': 3,
            'aime': 2, 'merci': 2, 'parfait': 2, 'excellent': 3, 'bravo': 2,
            '👍': 1, '❤️': 3, '😊': 2, '😄': 2, '🌟': 1,
            'bien': 1, 'bon': 1, 'magnifique': 3, 'adorable': 2
        }
        
        self.mots_negatifs = {
            'triste': 3, 'mal': 2, 'problème': 2, 'déteste': 3, 'nul': 2,
            'pas bien': 2, '😢': 3, '😠': 3, '😞': 3, 'horrible': 3,
            'mauvais': 2, 'dommage': 1, 'ennuyeux': 2, 'fatigué': 1
        }
        
        self.mots_intensite = {
            'très': 1.5, 'vraiment': 1.3, 'tellement': 1.4,
            'extrêmement': 1.8, 'un peu': 0.7, 'peu': 0.5
        }
    
    def analyser(self, texte):
        """
        Analyse le sentiment d'un texte
        Retourne: score (-100 à 100), humeur, détails
        """
        texte_lower = texte.lower()
        
        # Calcul du score de base
        score_pos = 0
        score_neg = 0
        intensite = 1.0
        
        # Détection des intensificateurs
        for mot, coef in self.mots_intensite.items():
            if mot in texte_lower:
                intensite *= coef
        
        # Analyse des mots positifs
        for mot, poids in self.mots_positifs.items():
            if mot in texte_lower:
                score_pos += poids * intensite
        
        # Analyse des mots négatifs
        for mot, poids in self.mots_negatifs.items():
            if mot in texte_lower:
                score_neg += poids * intensite
        
        # Score normalisé entre -100 et 100
        score_total = ((score_pos - score_neg) / (score_pos + score_neg + 1)) * 100
        
        # Déterminer l'humeur
        if score_total > 30:
            humeur = "joyeux"
        elif score_total > 10:
            humeur = "content"
        elif score_total > -10:
            humeur = "neutre"
        elif score_total > -30:
            humeur = "triste"
        else:
            humeur = "énervé"
        
        return {
            'score': round(score_total, 2),
            'humeur': humeur,
            'positif': round(score_pos, 2),
            'negatif': round(score_neg, 2),
            'intensite': round(intensite, 2)
        }
    
    def get_couleur_humeur(self, humeur):
        """Retourne une couleur selon l'humeur"""
        couleurs = {
            'joyeux': '\033[92m',  # Vert
            'content': '\033[96m',  # Cyan
            'neutre': '\033[93m',   # Jaune
            'triste': '\033[94m',   # Bleu
            'énervé': '\033[91m'    # Rouge
        }
        return couleurs.get(humeur, '\033[0m')