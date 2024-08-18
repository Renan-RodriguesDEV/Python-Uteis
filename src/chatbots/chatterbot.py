# %%
# !pip install ChatterBot spacy

from chatterbot.trainers import ListTrainer
# isso aqui só precisa para corrigir o bug
from spacy.cli.download import download

# %%
from chatterbot import ChatBot

download("en_core_web_sm")


class ENGSM:
    ISO_639_1 = 'en_core_web_sm'


# %%
chatBot = ChatBot("RenanChat", tagger_language=ENGSM)

dadosdetreino = [

    "Iae mano tudo bem",
    "Tudo numa boa e você como vai",
    "Tô bem também",
    "Mó paz",
    "Gosta de python?",
    "Adoro acho irado",
    "Eu também",
    "Que bom",
    "Qual é o seu nome meu mano?",
    "Meu nome é Rezzn Bot",
    "Qual é a sua plataforma favorita?",
    "Minha plataforma favorita é Playstation e a sua",
    "A minha é PC",
    "Meu jogo favorito é GTA San Andreas",
    "Qual é o seu jogo favorito ?",
    "Meu jogo favorito é Batman Arkham",
    "Qual é a sua série favorita ?",
    "Minha série favorita é The last of us",
    "Qual é o seu filme favorito ?",
    "Meu filme favorito é Sherek",
    "Qual é a sua música favorita ?",
    "Minha música favorita é Smells Like Teen Spirit",
    "Pode crer foi bom te conhecer mano"

]

trainer = ListTrainer(chatBot)
trainer.train(dadosdetreino)

# %%
while True:
    try:
        mensagem = input("Mande uma mensagem para o RenanChat:")
        if mensagem == "exit()":
            break
        resposta = chatBot.get_response(mensagem)
        print(resposta)
        dadosdetreino.append(str(mensagem))
    except KeyboardInterrupt:
        print("\nOperação interrompida pelo usuário.")
        break


# %%
chatBot.storage.drop()
