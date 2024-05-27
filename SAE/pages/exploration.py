import streamlit as st
import pandas as pd

# Fonction pour calculer la corrélation entre les variables numériques
def calculate_correlation(df, variable):
    numerical_df = df.select_dtypes(include=['int64', 'float64'])
    correlations = numerical_df.corrwith(df[variable])
    return correlations

# Header de la page
st.header("Exploration de données")

# Récupération du dataframe depuis la session
if "data_name" in st.session_state:
    df = st.session_state["data_name"]

    # Premier slider pour afficher le DataFrame avec différentes options
    st.subheader("1er Slider : Afficher le dataframe")
    option_df = st.selectbox(
        "Veuillez choisir les variables que vous voulez afficher",
        ("Tout", "Variables Numériques", "Variables Catégorielles"))

    if option_df == "Tout":
        st.dataframe(df)
    elif option_df == "Variables Numériques":
        st.dataframe(df.select_dtypes(include=['int64', 'float64']))
    elif option_df == "Variables Catégorielles":
        st.dataframe(df.select_dtypes(include=['object', 'category']))

    # Deuxième slider pour afficher la description des données
    st.subheader("2e Slider : Description des données")
    option_desc = st.selectbox(
        "Choisissez le type de variables pour afficher leurs statistiques descriptives",
        ("Variables Numériques", "Variables Catégorielles"))

    if option_desc == "Variables Numériques":
        st.write(df.select_dtypes(include=['int64', 'float64']).describe())
    elif option_desc == "Variables Catégorielles":
        st.write(df.select_dtypes(include=['object', 'category']).describe())

    # Troisième slider pour filtrer les valeurs NaN
    st.subheader("3e Slider : Filtrage des valeurs NaN")
    percentage_nan = st.slider("Choisissez le pourcentage de NaN à filtrer", 0, 100, 0)
    threshold = (100 - percentage_nan) / 100
    df_filtered = df.dropna(axis=1, thresh=int(threshold * len(df)))
    st.write("DataFrame après filtration des NaN :")
    st.dataframe(df_filtered)

    # Quatrième slider pour afficher la corrélation entre les variables numériques
    st.subheader("4e Slider : Corrélation entre les variables numériques")
    numerical_variables = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    variable_corr = st.selectbox("Choisissez une variable numérique", numerical_variables)
    correlations = calculate_correlation(df, variable_corr)
    st.write("Corrélation avec", variable_corr, ":")
    st.write(correlations)

else:
    st.write("Aucune donnée chargée. Veuillez retourner à l'accueil et télécharger un fichier.")
