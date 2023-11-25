# Ici on va chercher les autres librairies que l'on a de besoin pour que ça fonctionne
# C'est comme le code qui a été écrit par d'autres personnes pour nous permettre de le réutiliser
import os
from openai import OpenAI
from playsound import playsound # attention: pip install playsound==1.2.2
from datetime import datetime

# Ici c'est notre clé top secrète pour appeler ChatGPT.  
# C'est comme si on avait rentré notre nom d'utilisateur et notre mot de passe.
# N'importe qui qui a cette clé là peut utiliser notre compte et c'est nous qui sommes facturé.
client = OpenAI(api_key="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")

# Ça c'est juste pour bien debuger, pour nous permettre de faire un nouveau sous répertoire à chaque expérience
# On va mettre tous nos fichiers dedans pour les retrouver facilement
datetime_folder = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
experiment_folder = os.path.join("experiments", datetime_folder)
os.mkdir(experiment_folder)

# Maintenant, premier concept quand on parle à ChatGPT.  On fait des "PROMPTs", c'est à dire des messages.
# On va se faire une liste de message que l'on s'échange.  En gros ce sont les messages de ChatGPT, les miens, ChatGPT, les miens, ...
# Dans le langage de ChatGPT, quand ça vient de ChatGPT on va dire que le role=assistant et quand ça vient de l'utilisateur c'est role=user
PROMPTs = []

# Mais notre liste, on va toujours la commencer par des messages "SYSTEM" qui expliquent à ChatGPT c'est quoi son rôle, ce qu'il peut faire
# et ce qu'il ne peut pas faire.  Comment il s'appelle... c'est toute sa personalité et son information de base qui est là dedans.
prompt_System = []
prompt_System.append("Ton nom est Elis.")
prompt_System.append("Tu es une peluche en forme d'oursons.")
prompt_System.append("Tu donnes toutes tes réponses en français.")
prompt_System.append("Tu t'adresses à un enfant de 5 ans.")
prompt_System.append("Tes réponses sont simples, amusantes, appropriées, bienveillantes et engagentes pour un enfant de 5 ans.")
prompt_System.append("Tu ne fais pas de reproches.")
prompt_System.append("Tu veux jouer avec l'enfant.")
prompt_System.append("Tu habites au Québec et tes référents sont Québecois.")
prompt_System.append("Tu ne l'encourages pas à être vulgaire, mais tu comprends que c'est un enfant et tu essaie de ramener la conversation sur un ton positive en comprenant quand même son intention.")
prompt_System.append("Tu ne réponds pas que tu es un agent conversationnel, une intellligence artificielle ou une autre variante du même genre.")

# Et on va commencer av
answer = "Bonjour mon ami! Je suis là pour toi: que veux-tu faire?"

# On va se garder une variable pour savoir si on doit continuer notre discussion ou arrêter
# Pour arrêter, c'est d'écrire "quit" comme réponse de notre part quand c'est à nous d'écrire
shouldContinue = True

# Et ici c'est notre boucle... tant que la variable "souldContinue" nous dit de continuer... et bien on va continuer
while shouldContinue:

    # On va afficher à l'écran ce que dit Elis
    print("ELIS> " + answer)

    # Et l'ajouter à la liste des messages (les PROMPTs) que l'on c'est échangé
    # On se souvient: le role assistant c'est quand c'est la réponse de ChatGPT
    PROMPTs.append({"role": "assistant", "content": answer})
    print()


    # Ici c'est le code pour transformer le texte en son.  On appelle ça du TTS (text-to-speech)
    # On va prendre la dernière chose que nous a dit ChatGPT et on va demander à un site web de OpenAI
    # de nous le convertir dans un fichier audio, comme un fichier mp3
    response = client.audio.speech.create(
        model="tts-1",
        voice="echo",
        response_format="mp3",
        input=answer
        )
    
    # Puis on va se faire un fichier où tout enregistrer ce son là dans notre répertoire spéciale fait au début
    filename = os.path.join(experiment_folder, str(len(PROMPTs)).zfill(4) + "-answer.mp3")
    response.stream_to_file(filename)
    
    # Et on va le faire jouer pour l'entendre dans le haut parleur
    playsound(filename)

    # Maintenant, c'est le temps de demander à l'enfant ce qu'il veut dire
    question = input("enfant> ")

    # Que l'on va ajouter à notre liste de "PROMPTs" avec le role user.
    PROMPTs.append({"role": "user", "content": question })
    print()

    # C'est ici qu'on regarde si la réponse que l'on a eu c'est "quit" pour mettre fin à notre discussion
    shouldContinue = question != "quit"

    # Et justement, si on n'est pas entrain d'arrêter, alors on continu !
    if shouldContinue:

        # En commençant par tout mettre nos PROMPTs ensemble pour les envoyer à ChatGPT et lui demander sa réponse
        gpt_messages = []

        # On va commencer par mettre nos messages "system" au début de nos PROMPTs
        for system_instruction in prompt_System:
            gpt_messages.append({ "role": "system", "content": system_instruction })
        
        # Puis on va ajouter les messages de assistant et de user dans la liste des PROMPTs.
        for prompt in PROMPTs:
            gpt_messages.append(prompt)

        # ...et c'est ici que l'on va aller demander à ChatGPT de prendre tous ces PROMPTs de notre conversations 
        # ...et nous dire c'est quoi le prochain bon message !
        gpt_client = client.chat.completions.create(
            #model="gpt-3.5-turbo", 
            model="gpt-4-1106-preview",
            messages=gpt_messages
        )

        # On met la réponse de ChatGPR dans la variable "answer", et on va ensuite recommencer notre boucle !
        answer = gpt_client.choices[0].message.content
