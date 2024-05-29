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

# Fonction pour effacer l'état de soumission
def clear_submit():
    st.session_state["submit"] = False

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

# Configuration de la page
st.set_page_config(page_title="LangChain: Chat with pandas DataFrame", page_icon="🦜")
st.title("🦜 LangChain: Chat with pandas DataFrame")

# Téléchargement de fichier
uploaded_file = st.file_uploader(
    "Upload a Data file",
    type=list(file_formats.keys()),
    help="Formats de fichier supportés: CSV, XLS, XLSX, XLSM, XLSB",
    on_change=clear_submit,
)

if not uploaded_file:
    st.warning(
        "Cette application utilise le `PythonAstREPLTool` de LangChain qui est vulnérable à l'exécution de code arbitraire. Utilisez cette application avec précaution."
    )

if uploaded_file:
    df = load_data(uploaded_file)
    if df is not None:
        st.session_state["data_name"] = df  # Enregistrer le DataFrame dans le state de la session
        st.success("Fichier chargé avec succès!")
        st.dataframe(df.head())
        st.write("Colonnes de type 'object' ou 'category':")
        st.dataframe(df.select_dtypes(include=['object', 'category']))
    else:
        st.error("Erreur lors du chargement du fichier.")
