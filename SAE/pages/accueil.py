import os
import streamlit as st
import pandas as pd

# Définir les formats de fichiers supportés
file_formats = {
    "csv": pd.read_csv,
    "xls": pd.read_excel,
    "xlsx": pd.read_excel,
    "xlsm": pd.read_excel,
    "xlsb": pd.read_excel,
}

# Fonction pour charger les données avec mise en cache
@st.cache_data(ttl="2h")
def load_data(uploaded_file):
    try:
        ext = os.path.splitext(uploaded_file.name)[1][1:].lower()
    except Exception as e:
        st.error(f"Erreur lors de l'obtention de l'extension du fichier: {e}")
        return None
    
    if ext in file_formats:
        try:
            data = file_formats[ext](uploaded_file)
            return data
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier: {e}")
            return None
    else:
        st.error(f"Format de fichier non supporté: {ext}")
        return None

# Section de la barre latérale
st.sidebar.title("Accueil du site")
uploaded_file = st.sidebar.file_uploader(
    "Choisir un fichier", 
    type=list(file_formats.keys()), 
    help="Formats de fichier supportés: CSV, XLS, XLSX, XLSM, XLSB"
)

if uploaded_file is not None:
    df = load_data(uploaded_file)
    if df is not None:
        st.dataframe(df)
        st.session_state["data_name"] = df
    else:
        st.error("Erreur lors du chargement du fichier.")
else:
    st.sidebar.warning("Veuillez charger un fichier svp !", icon="⚠️")
