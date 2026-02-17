# chatbot.py
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import json
import random
from collections import deque
from datetime import datetime

from config import *
from sentiment import SentimentAnalyzer
from souvenirs_manager import SouvenirsManager
from utils import DisplayUtils, StatsUtils, TexteUtils

class FrenchChatbotPro:
    """
    Chatbot français avec personnalité modulaire
    """
    
    def __init__(self, model_name="microsoft/DialoGPT-small"):
        self.display = DisplayUtils()
        self.stats_utils = StatsUtils()
        self.texte_utils = TexteUtils()
        self.sentiment = SentimentAnalyzer()
        self.souvenirs = SouvenirsManager()
        
        print("⚡ Initialisation du chatbot...")
        self.display.spinner_animation(3, "Chargement du modèle")
        
        # Charger le modèle
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        
        self.generator = pipeline(
            'text-generation',
            model=self.model,
            tokenizer=self.tokenizer,
            device=0 if torch.cuda.is_available() else -1
        )
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Charger les personnalités
        self.personnalites = self.charger_personnalites()
        
        # Charger les connaissances
        self.connaissances = self.charger_connaissances()
        
        # État du bot
        self.personnalite_active = "1"
        self.humeur = "neutre"
        self.history = deque(maxlen=DEFAULT_MAX_HISTORY)
        
        # Statistiques
        self.stats = {
            "messages_echanges": 0,
            "mots_total": 0,
            "debut_conversation": datetime.now()
        }
        
        print("✅ Chatbot prêt !")
        self.afficher_personnalite()
    
    def charger_personnalites(self):
        """Charge les personnalités depuis le fichier JSON"""
        try:
            with open(PERSONNALITES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Personnalités par défaut
            return {
                "1": {"name": "Amical", "emoji": "😊", "description": "Chaleureux", 
                      "temperature": 0.85, "top_p": 0.92, "emojis": ["😊"]}
            }
    
    def charger_connaissances(self):
        """Charge les connaissances depuis le fichier JSON"""
        try:
            with open(CONNAISSANCES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def afficher_personnalite(self):
        """Affiche la personnalité actuelle"""
        perso = self.personnalites[self.personnalite_active]
        print(f"\n🎭 Personnalité : {perso['name']} {perso.get('emoji', '')}")
        print(f"   {perso.get('description', '')}")
    
    # ... (les autres méthodes seront importées des modules)