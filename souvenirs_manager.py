# souvenirs_manager.py
import json
import time
from datetime import datetime
from collections import deque
from typing import List, Dict, Any
import hashlib

class SouvenirsManager:
    """
    Gère la mémoire à long terme du chatbot
    """
    
    def __init__(self, fichier="souvenirs_bot.json"):
        self.fichier = fichier
        self.souvenirs = self.charger()
        self.souvenirs_courts = deque(maxlen=20)  # Mémoire à court terme
        
    def charger(self) -> Dict[str, Any]:
        """Charge les souvenirs depuis le fichier"""
        try:
            with open(self.fichier, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "souvenirs": [],
                "faits_appris": [],
                "preferences_utilisateur": {},
                "statistiques": {
                    "total_conversations": 0,
                    "mots_echanges": 0,
                    "sujets_preferes": []
                }
            }
    
    def sauvegarder(self):
        """Sauvegarde les souvenirs dans le fichier"""
        try:
            with open(self.fichier, 'w', encoding='utf-8') as f:
                json.dump(self.souvenirs, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False
    
    def ajouter_souvenir(self, type_souvenir: str, contenu: Dict):
        """Ajoute un nouveau souvenir"""
        souvenir = {
            "id": self._generer_id(contenu),
            "type": type_souvenir,
            "contenu": contenu,
            "timestamp": datetime.now().isoformat(),
            "importance": self._calculer_importance(contenu)
        }
        
        self.souvenirs["souvenirs"].append(souvenir)
        self.souvenirs_courts.append(souvenir)
        
        # Limiter le nombre de souvenirs
        if len(self.souvenirs["souvenirs"]) > 1000:
            self.souvenirs["souvenirs"] = self.souvenirs["souvenirs"][-1000:]
        
        self.sauvegarder()
        return souvenir
    
    def _generer_id(self, contenu: Dict) -> str:
        """Génère un ID unique pour un souvenir"""
        chaine = str(contenu) + str(time.time())
        return hashlib.md5(chaine.encode()).hexdigest()[:8]
    
    def _calculer_importance(self, contenu: Dict) -> int:
        """Calcule l'importance d'un souvenir (1-10)"""
        importance = 5  # Importance par défaut
        
        # Plus d'importance si c'est une information personnelle
        if any(mot in str(contenu).lower() for mot in ['prénom', 'nom', 'âge', 'ville']):
            importance += 3
        
        # Plus d'importance si c'est une préférence
        if any(mot in str(contenu).lower() for mot in ['aime', 'préfère', 'adore']):
            importance += 2
        
        return min(importance, 10)
    
    def rechercher_souvenirs(self, requete: str, limite: int = 5) -> List[Dict]:
        """Recherche des souvenirs pertinents"""
        resultats = []
        requete_lower = requete.lower()
        
        for souvenir in reversed(self.souvenirs["souvenirs"]):
            contenu_str = str(souvenir["contenu"]).lower()
            if requete_lower in contenu_str:
                resultats.append(souvenir)
                if len(resultats) >= limite:
                    break
        
        return resultats
    
    def apprendre_fait(self, fait: str, confiance: float = 0.5):
        """Apprend un nouveau fait"""
        self.souvenirs["faits_appris"].append({
            "fait": fait,
            "confiance": confiance,
            "appris_le": datetime.now().isoformat(),
            "fois_cite": 1
        })
        self.sauvegarder()
    
    def get_contexte_conversation(self, n_derniers: int = 5) -> str:
        """Récupère le contexte récent de la conversation"""
        contexte = []
        for souvenir in list(self.souvenirs_courts)[-n_derniers:]:
            if souvenir["type"] == "conversation":
                contexte.append(souvenir["contenu"].get("message", ""))
        return "\n".join(contexte)
    
    def update_preferences(self, utilisateur: str, cle: str, valeur: Any):
        """Met à jour les préférences d'un utilisateur"""
        if utilisateur not in self.souvenirs["preferences_utilisateur"]:
            self.souvenirs["preferences_utilisateur"][utilisateur] = {}
        
        self.souvenirs["preferences_utilisateur"][utilisateur][cle] = {
            "valeur": valeur,
            "derniere_mise_a_jour": datetime.now().isoformat()
        }
        
        self.sauvegarder()