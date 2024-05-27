import streamlit as st
from langchain_community.llms import HuggingFaceEndpoint
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from deep_translator import (GoogleTranslator,
                                ChatGptTranslator,
                             MicrosoftTranslator,
                             PonsTranslator,
                             LingueeTranslator,
                             MyMemoryTranslator,
                             YandexTranslator,
                             PapagoTranslator,
                             DeeplTranslator,
                             QcriTranslator,
                             single_detection,
                             batch_detection)

HUGGINGFACEHUB_API_TOKEN = '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'
import os
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN


st.title("Votre Assistant IA")


# Charger le modèle 
template = """Question: {question}
Answer: Let's think step by step."""
prompt_template = PromptTemplate.from_template(template)
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
llm = HuggingFaceEndpoint(
    repo_id=repo_id,  temperature=0.5, model_kwargs={"max_length":128, "token":HUGGINGFACEHUB_API_TOKEN}
)
llm_chain = LLMChain(prompt=prompt_template, llm=llm)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Comment puis-je vous aidez?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Traduire la question en anglais
    prompt = GoogleTranslator(source='auto', target='en').translate(prompt)

    # Poser la question au modèle Mistral (modèle crée en France)
    answer = llm_chain.run(prompt)

    # Traduire la reponse en français
    answer = GoogleTranslator(source='auto', target='fr').translate(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)