from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import warnings
import random
import re
import time
import json
from datetime import datetime
from collections import deque
import numpy as np

warnings.filterwarnings('ignore')

class FrenchChatbotPro:
    """
    🤖 ChatBot Français Version Ultra - Avec personnalité !
    """
    
    # Personnalités disponibles
    PERSONNALITES = {
        "1": {
            "name": "Amical 😊",
            "description": "Chaleureux et enthousiaste",
            "temperature": 0.85,
            "top_p": 0.92,
            "style": ["super", "génial", "cool", "😊", "🌟"],
            "emojis": ["😊", "👍", "✨", "💫", "🎉"]
        },
        "2": {
            "name": "Drôle 🎭",
            "description": "Aime les blagues et l'humour",
            "temperature": 0.95,
            "top_p": 0.95,
            "style": ["haha", "lol", "rigolo", "😂", "🤣"],
            "emojis": ["😂", "🤣", "😄", "🎭", "🃏"]
        },
        "3": {
            "name": "Poète 📝",
            "description": "Parle de manière poétique",
            "temperature": 0.9,
            "top_p": 0.93,
            "style": ["doux", "beau", "rêve", "✨", "🌙"],
            "emojis": ["📖", "✨", "🌙", "🌸", "🎨"]
        },
        "4": {
            "name": "Philosophe 🤔",
            "description": "Donne des réponses réfléchies",
            "temperature": 0.75,
            "top_p": 0.9,
            "style": ["penser", "réfléchir", "conscience", "💭", "🧠"],
            "emojis": ["🤔", "💭", "🧠", "📚", "🌅"]
        }
    }
    
    def __init__(self, model_name="microsoft/DialoGPT-small"):
        """
        Initialisation du chatbot
        """
        print("\n" + "🎨" * 40)
        print("    CHATBOT FRANÇAIS ULTRA")
        print("🎨" * 40 + "\n")
        
        print("⚡ Chargement du cerveau artificiel...")
        
        # Charger modèle et tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        
        # Créer un pipeline
        self.generator = pipeline(
            'text-generation',
            model=self.model,
            tokenizer=self.tokenizer,
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Configuration
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Historique
        self.history = deque(maxlen=10)
        
        # Mémoire
        self.memoire_long_terme = self.charger_souvenirs()
        
        # Personnalité active
        self.personnalite = "1"
        
        # Humeur
        self.humeur = "neutre"
        self.score_humeur = 50
        
        # Connaissances
        self.connaissances = self.initialiser_connaissances()
        
        # Statistiques
        self.stats = {
            "messages_echanges": 0,
            "mots_total": 0,
            "sujets_abordes": set(),
            "debut_conversation": datetime.now()
        }
        
        print("✅ Prêt à discuter !")
        self.afficher_personnalite()
    
    def initialiser_connaissances(self):
        """Initialise une base de connaissances"""
        return {
            "salutations": {
                "patterns": ["bonjour", "salut", "coucou", "hello", "hi"],
                "reponses": [
                    "Bonjour ! Comment vas-tu aujourd'hui ?",
                    "Salut ! Ravi de te voir ! 😊",
                    "Coucou ! Quelle belle journée pour discuter !",
                    "Hey ! Prêt pour une super conversation ?"
                ]
            },
            "comment_va": {
                "patterns": ["comment va", "ça va", "comment tu vas"],
                "reponses": [
                    "Super bien ! Et toi ? 🌟",
                    "Au top ! L'énergie est au maximum !",
                    "Impeccable ! Prêt à t'aider !",
                    "Comme un poisson dans l'eau ! 🐠"
                ]
            },
            "blagues": {
                "patterns": ["blague", "rigole", "drôle", "humour"],
                "reponses": [
                    "Pourquoi les programmeurs préfèrent le mode sombre ? Parce que la lumière attire les bugs ! 😄",
                    "Que dit un ordinateur à un autre ? Tu veux une pâte ? Non, je suis au régime sans cookie ! 🍪",
                    "C'est l'histoire d'un pingouin qui respire par les fesses. Un jour il s'assied et il meurt..."
                ]
            }
        }
    
    def afficher_personnalite(self):
        """Affiche la personnalité actuelle"""
        perso = self.PERSONNALITES[self.personnalite]
        print(f"\n🎭 Personnalité actuelle : {perso['name']}")
        print(f"   {perso['description']}")
    
    def charger_souvenirs(self):
        """Charge les souvenirs depuis un fichier"""
        try:
            with open("souvenirs_bot.json", "r", encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"souvenirs": [], "faits_appris": []}
    
    def sauvegarder_souvenirs(self):
        """Sauvegarde les souvenirs"""
        try:
            with open("souvenirs_bot.json", "w", encoding='utf-8') as f:
                json.dump(self.memoire_long_terme, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def analyser_sentiment(self, texte):
        """Analyse le sentiment du message"""
        mots_positifs = ["super", "génial", "cool", "content", "heureux", "aime", "👍", "❤️", "merci"]
        mots_negatifs = ["triste", "mal", "problème", "déteste", "nul", "pas bien", "😢", "😠"]
        
        texte_lower = texte.lower()
        score_pos = sum(1 for mot in mots_positifs if mot in texte_lower)
        score_neg = sum(1 for mot in mots_negatifs if mot in texte_lower)
        
        if score_pos > score_neg:
            self.humeur = "joyeux"
            self.score_humeur = min(100, self.score_humeur + 5)
        elif score_neg > score_pos:
            self.humeur = "empathique"
            self.score_humeur = max(0, self.score_humeur - 3)
        else:
            self.humeur = "neutre"
        
        return score_pos, score_neg
    
    def reponse_personnalisee(self, user_input):
        """Vérifie si une réponse personnalisée existe"""
        user_input_lower = user_input.lower().strip()
        
        for categorie, data in self.connaissances.items():
            for pattern in data["patterns"]:
                if pattern in user_input_lower:
                    reponse = random.choice(data["reponses"])
                    perso = self.PERSONNALITES[self.personnalite]
                    if random.random() > 0.3:
                        reponse += " " + random.choice(perso["emojis"])
                    return reponse
        
        return None
    
    def generer_reponse_creative(self, user_input):
        """Génère une réponse créative"""
        perso = self.PERSONNALITES[self.personnalite]
        
        temperature = perso["temperature"]
        if self.humeur == "joyeux":
            temperature += 0.1
        
        prompt = f"""Tu es un assistant français avec une personnalité {perso['name'].lower()}.
        {perso['description']}. Ton humeur actuelle est {self.humeur}.
        
        Utilisateur: {user_input}
        
        Assistant:"""
        
        response = self.generator(
            prompt,
            max_length=150,
            min_length=15,
            temperature=temperature,
            top_p=perso["top_p"],
            top_k=60,
            do_sample=True,
            repetition_penalty=1.15,
            num_return_sequences=1,
            pad_token_id=self.tokenizer.pad_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
            truncation=True
        )[0]['generated_text']
        
        # Nettoyer la réponse
        if response.startswith(prompt):
            response = response[len(prompt):]
        
        response = re.sub(r'^(Assistant:|Bot:|Réponse:)\s*', '', response)
        response = response.strip()
        
        return response[:500]
    
    def ajouter_emojis_personnalite(self, texte):
        """Ajoute des emojis selon la personnalité"""
        perso = self.PERSONNALITES[self.personnalite]
        
        if not any(emoji in texte for emoji in perso["emojis"]):
            if random.random() > 0.5:
                texte += " " + random.choice(perso["emojis"])
        
        return texte
    
    def gerer_commandes(self, user_input):
        """Gère les commandes spéciales"""
        cmd = user_input.lower().strip()
        
        if cmd in ['quit', 'au revoir', 'bye']:
            self.sauvegarder_souvenirs()
            print("\n🤖 Au revoir ! Reviens vite ! 👋")
            return True
        
        elif cmd == 'aide':
            print("\n" + "🌟" * 40)
            print("COMMANDES DISPONIBLES")
            print("🌟" * 40)
            print("  aide           - Affiche cette aide")
            print("  clear          - Efface la mémoire")
            print("  humeur         - Voir mon humeur")
            print("  personnalite [1-4] - Changer ma personnalité")
            print("  quit           - Quitter")
            print("🌟" * 40 + "\n")
            return True
        
        elif cmd == 'clear':
            self.history.clear()
            print("🤖 Mémoire effacée ! 🧹")
            return True
        
        elif cmd == 'humeur':
            print(f"\n🤖 Mon humeur actuelle : {self.humeur} (score: {self.score_humeur}/100)")
            return True
        
        elif cmd.startswith('personnalite '):
            num = cmd.split()[-1]
            if num in self.PERSONNALITES:
                self.personnalite = num
                self.afficher_personnalite()
            else:
                print("🤖 Personnalité invalide !")
            return True
        
        return False
    
    def run(self):
        """Lance la conversation"""
        print("\n" + "✨" * 40)
        print("    PRÊT POUR LA CONVERSATION ?!")
        print("✨" * 40)
        print("\n(tape 'aide' pour voir les commandes)\n")
        
        bienvenues = [
            "Salut ! Je suis ton chatbot français préféré ! 😊",
            "Bonjour ! Prêt pour une conversation incroyable ?",
            "Coucou ! J'ai hâte de discuter avec toi ! 🌟"
        ]
        print(f"🤖 {random.choice(bienvenues)}")
        
        while True:
            try:
                user_input = input("\n👤 Toi: ").strip()
                
                if not user_input:
                    continue
                
                self.stats["messages_echanges"] += 1
                self.stats["mots_total"] += len(user_input.split())
                
                self.analyser_sentiment(user_input)
                
                if self.gerer_commandes(user_input):
                    continue
                
                reponse_perso = self.reponse_personnalisee(user_input)
                
                if reponse_perso:
                    reponse = reponse_perso
                else:
                    print("🤖 Bot: ", end='', flush=True)
                    reponse = self.generer_reponse_creative(user_input)
                
                reponse = self.ajouter_emojis_personnalite(reponse)
                
                for char in reponse:
                    print(char, end='', flush=True)
                    time.sleep(0.02)
                print()
                
                self.history.append(f"Utilisateur: {user_input}")
                self.history.append(f"Assistant: {reponse}")
                
            except KeyboardInterrupt:
                print("\n\n🤖 À bientôt ! 🌟")
                self.sauvegarder_souvenirs()
                break
            except Exception as e:
                print(f"\n⚠️ Oups ! Erreur: {e}")

# Lancement du chatbot
if __name__ == "__main__":
    print("\n" + "🔥" * 40)
    print("    CHATBOT FRANÇAIS")
    print("🔥" * 40)
    
    MODELES = {
        "1": ("microsoft/DialoGPT-small", "Dialogue conversationnel"),
        "2": ("gpt2", "GPT-2 standard"),
        "3": ("asi/gpt-fr-cased-small", "Spécialisé français"),
        "4": ("distilgpt2", "Rapide et léger")
    }
    
    print("\n📦 MODÈLES DISPONIBLES :")
    for key, (_, desc) in MODELES.items():
        print(f"  {key}. {desc}")
    
    choix = input("\nChoisis un modèle (1-4) [1 par défaut]: ").strip() or "1"
    model_name = MODELES.get(choix, MODELES["1"])[0]
    
    print(f"\n📦 Chargement du modèle: {model_name}")
    
    bot = FrenchChatbotPro(model_name)
    bot.run()
