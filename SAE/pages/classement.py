import streamlit as st


st.title("Classement des données")
#Récuperer le dataframe 
if "data_name" in st.session_state :
    df = st.session_state["data_name"]

    #Modèle linéaire
    st.title("Modèle linéaire")
    # Sélectionner un modèle
    modele_lineaire = st.selectbox(
        'Choisissez un modèle',
        ('Linear SVM', 'Logistic classification', 'Linear Discriminant Analysis'),
        index=None,
        placeholder="sélectionnez un modéle",)
    if modele_lineaire == 'Linear SVM':
        st.write("salut")

    #Modèle non linéaire
    st.title("Modèle non linéaire")
    # Sélectionner un modèle
    modele_non_lineaire = st.selectbox(
        'Choisissez un modèle',
        ('Kernal SVM', 'Quadratic Discriminant Analysis'),
        index=None,
        placeholder="sélectionnez un modéle",)

    # Modèle ensembliste
    st.title("Modèle ensembliste")
    # Sélectionner un modèle
    modele_ensembliste = st.selectbox(
        'Choisissez un modèle',
        ('Random Forest', 'XGBoost'),
        index=None,
        placeholder="sélectionnez un modéle",)

    # Modèle simple
    st.title("Modèle simple")
    # Sélectionner un modèle
    modele_simple = st.selectbox(
        'Choisissez un modèle',
        ('KNN', 'Naive Bayes', 'Tree Decision'),
        index=None,
        placeholder="sélectionnez un modéle",)


else :
    st.warning("Veuillez charger un fichier svp !",  icon="⚠️")