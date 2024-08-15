# %% [markdown]
# Install the Google AI Python SDK
# See the getting started guide for more information:
# https://ai.google.dev/gemini-api/docs/get-started/python
#
# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
#
# safety_settings = Adjust safety settings
# See https://ai.google.dev/gemini-api/docs/safety-settings
#

# %%
# intalacao das libs

# !pip install google-generativeai
# !pip install deep-translator

# %%
# gemini
import google.generativeai as genai
# tradutor
from deep_translator import GoogleTranslator

# %%
# configurando a api
from creds_my import API_KEY
genai.configure(api_key=API_KEY)

# config do modelo de prompt
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# config do modelo q sera utilizando (gemini 1.5 pro)
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

# guardando o historico de perguntas
chat_session = model.start_chat(
    history=[
    ]
)


# %%
# tradutor de ingles pra br
gt_pt = GoogleTranslator('en', 'pt')
# tradutor de br  pra ingles
gt_en = GoogleTranslator('pt', 'en')


# %%
while True:
    # pegando a msg do usuario
    message = input('Start message:')
    if message == "parar":
        break

    # passando a msg para o ingles
    message = gt_en.translate(message)

    # passando a msg em ingles para o modelo
    response = chat_session.send_message(message)

    # pegando a resposta e taduzindo
    resp_trans = gt_pt.translate(response.text)

    print(resp_trans)
