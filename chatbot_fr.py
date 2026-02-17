from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import warnings
warnings.filterwarnings('ignore')

class FrenchChatbot:
    def __init__(self, model_name="microsoft/DialoGPT-small"):
        """
        Initialise le chatbot avec un modèle adapté au dialogue
        DialoGPT est mieux pour la conversation que GPT-Neo
        """
        print("⚡ Chargement du modèle...")
        
        # Charger modèle et tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        
        # Créer un pipeline pour simplifier
        self.generator = pipeline(
            'text-generation',
            model=self.model,
            tokenizer=self.tokenizer,
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Configuration du tokenizer
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Historique de conversation
        self.history = []
        self.max_history = 4  # Garde les 4 derniers échanges
        
        print("✅ Prêt ! Tape 'aide' pour les commandes\n")
    
    def format_prompt(self, user_input):
        """Formate le prompt avec l'historique"""
        # Ajouter la nouvelle entrée
        self.history.append(f"Utilisateur: {user_input}")
        
        # Garder seulement les derniers échanges
        if len(self.history) > self.max_history * 2:
            self.history = self.history[-(self.max_history * 2):]
        
        # Créer le prompt
        prompt = "Tu es un assistant français intelligent et serviable.\n"
        prompt += "Réponds de manière naturelle et conversationnelle en français.\n\n"
        
        # Ajouter l'historique
        for i in range(0, len(self.history) - 1, 2):
            if i + 1 < len(self.history):
                prompt += f"{self.history[i]}\n{self.history[i+1]}\n"
        
        prompt += f"{self.history[-1]}\nAssistant:"
        return prompt
    
    def clean_response(self, response, user_input):
        """Nettoie la réponse générée"""
        # Supprimer la répétition de la question
        if response.startswith(user_input):
            response = response[len(user_input):]
        
        # Supprimer les préfixes indésirables
        prefixes = ["Assistant:", "Réponse:", "Bot:"]
        for prefix in prefixes:
            if response.startswith(prefix):
                response = response[len(prefix):]
        
        # Nettoyer les espaces
        response = response.strip()
        
        # Supprimer tout après un saut de ligne
        if '\n' in response:
            response = response.split('\n')[0]
        
        return response
    
    def generate_response(self, user_input):
        """Génère une réponse"""
        prompt = self.format_prompt(user_input)
        
        # Générer la réponse
        response = self.generator(
            prompt,
            max_length=200,
            min_length=20,
            temperature=0.85,  # Un peu créatif mais cohérent
            top_p=0.92,
            top_k=50,
            do_sample=True,
            repetition_penalty=1.2,  # Évite la répétition
            num_return_sequences=1,
            pad_token_id=self.tokenizer.pad_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
            truncation=True
        )[0]['generated_text']
        
        # Extraire seulement la nouvelle réponse
        response = response[len(prompt):]
        response = self.clean_response(response, user_input)
        
        # Ajouter à l'historique
        self.history.append(f"Assistant: {response}")
        
        return response
    
    def show_help(self):
        """Affiche l'aide"""
        print("\n" + "="*50)
        print("🤖 COMMANDES DISPONIBLES :")
        print("="*50)
        print("  'aide'      - Affiche ce message")
        print("  'clear'     - Efface l'historique")
        print("  'history'   - Affiche l'historique")
        print("  'quit'      - Quitte le programme")
        print("  'au revoir' - Quitte le programme")
        print("  'mode [x]'  - Change le mode (1=simple, 2=créatif)")
        print("="*50 + "\n")
    
    def run(self):
        """Lance la boucle de conversation"""
        print("\n" + "✨"*25)
        print("    CHATBOT FRANÇAIS AVANCÉ")
        print("✨"*25 + "\n")
        
        modes = {
            '1': {'temp': 0.7, 'top_p': 0.9},
            '2': {'temp': 0.9, 'top_p': 0.95}
        }
        current_mode = '1'
        
        while True:
            try:
                # Obtenir l'entrée utilisateur
                user_input = input("\n👤 Vous: ").strip()
                
                if not user_input:
                    continue
                
                # Commandes spéciales
                if user_input.lower() == 'quit' or user_input.lower() == 'au revoir':
                    print("\n🤖 Au revoir ! À bientôt ! 👋")
                    break
                
                elif user_input.lower() == 'aide':
                    self.show_help()
                    continue
                
                elif user_input.lower() == 'clear':
                    self.history = []
                    print("🤖 Historique effacé !")
                    continue
                
                elif user_input.lower() == 'history':
                    print("\n📜 Historique:")
                    for i, msg in enumerate(self.history):
                        print(f"  {i+1}. {msg}")
                    continue
                
                elif user_input.lower().startswith('mode '):
                    mode = user_input.split()[-1]
                    if mode in modes:
                        current_mode = mode
                        self.generator.task_kwargs['temperature'] = modes[mode]['temp']
                        print(f"🤖 Mode changé à {'Simple' if mode == '1' else 'Créatif'}")
                    else:
                        print("🤖 Mode invalide. Utilise 1 ou 2.")
                    continue
                
                # Générer et afficher la réponse
                print("🤖 Assistant: ", end='', flush=True)
                
                response = self.generate_response(user_input)
                
                # Afficher progressivement (effet de saisie)
                for char in response:
                    print(char, end='', flush=True)
                    import time
                    time.sleep(0.01)
                print()
                
                # Limiter la taille de l'historique
                if len(self.history) > 8:
                    self.history = self.history[-8:]
                    
            except KeyboardInterrupt:
                print("\n\n🤖 Interruption détectée. Au revoir !")
                break
            except Exception as e:
                print(f"\n⚠️  Erreur: {e}")
                print("Réessayez...")

# Configuration avancée
if __name__ == "__main__":
    # Liste de modèles possibles (choisir un)
    MODELS = {
        "1": "microsoft/DialoGPT-small",      # Bon pour dialogue
        "2": "gpt2",                          # GPT-2 standard
        "3": "asi/gpt-fr-cased-small",        # Français
        "4": "distilgpt2"                     # Léger et rapide
    }
    
    print("🧠 CHOIX DU MODÈLE :")
    for key, value in MODELS.items():
        print(f"  {key}. {value}")
    
    choice = input("\nChoisis un modèle (1-4) [1 par défaut]: ").strip() or "1"
    model_name = MODELS.get(choice, MODELS["1"])
    
    # Créer et lancer le chatbot
    bot = FrenchChatbot(model_name)
    bot.run()