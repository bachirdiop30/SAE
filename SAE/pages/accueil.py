import streamlit as st
import pandas as pd


st.header("Accueil")
st.write("Accueil du site")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file) # utiliser --server.maxUploadSize 500 pour modifier la taille max du fichier
    st.session_state["data_name"] = data
    st.write(data)
