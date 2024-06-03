import os
import sys

from fonctions.afdm import afdm
from fonctions.svd import plot_svd 
package_dir = os.getcwd() # C:\\Users\\amina\\SAE
sys.path.append(os.path.join(package_dir, "pages"))
import streamlit as st
from pages.fonction  import *
from fonctions.acp import  *
from fonctions.svd import svd
from fonctions.afdm import  *
from fonctions.plot_acp import  *
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler


#Récuperer le dataframe 
if "data_name" in st.session_state :
    df = st.session_state["data_name"]


    # Sélectionner une mèthode d'analyse
    option = st.sidebar.selectbox(
        'Méthode d\'analyse factorielle',
        ('Analyse des Composantes Principales (ACP)', 'Analyse Factorielle de Données Mixtes (AFDM)', 'Décomposition en valeurs singulières (SVD)'),
        index=None,
        placeholder="sélectionnez une méthode d'analyse factorielle",)

    # Supprimer les identifiants
    identifiants = st.sidebar.multiselect("Supprimer les identifiants",df.columns.tolist())
    df = df.drop(columns=identifiants)

    # Récupérer les données catégorielles, numériques et le dataframe nettoyé
    data,numerical_variables, categorical_variables = nettoyage(df)

    #Analyse des Composantes Principales (ACP)
    if option == 'Analyse des Composantes Principales (ACP)' or option == 'Décomposition en valeurs singulières (SVD)':

        #Prétraitement des données
        st.write("""
                Pour une réduction de dimension efficace dans notre application, le prétraitement des données est une étape essentielle. 
                """)
        pretraitement = st.sidebar.radio("Nous offrons deux options pour les données catégorielles :",
            ["***Supprimer les données catégorielles***", "***Encoder les données catégorielles***"],
            captions = ("si elles ne sont pas pertinentes pour votre analyse, cette option les éliminera de l'ensemble de données.", 
                        "convertissez-les en valeurs numériques pour les utiliser dans l'analyse factorielle."))
        
        # Supprimer les variables catégorielles
        if pretraitement == "***Supprimer les données catégorielles***" : 
            # Supprimer les colonnes qui contient que des Nan
            data = data.drop(columns=categorical_variables)
            categorical_variables = []         

        # Encoder les variables catégorielles   
        elif pretraitement == "***Encoder les données catégorielles***" : 
            # Encoder les variables 
            data = encoder(data,numerical_variables, categorical_variables)

        # Prétraitement des données
        st.write(""" Après le prétraitement des données, nous les normalisons pour les préparer à l'analyse ou à la modélisation.. """)
                
        normalisation = st.sidebar.radio("Nous présentons maintenant trois méthodes pour la normalisation des données :",
        ["***StandardScaler***", "***MinMaxScaler***", "***RobustScaler***"],
        captions = (" Centre les données autour de zéro et les met à l'échelle de manière à avoir une variance unitaire. Sensible aux valeurs aberrantes car utilise la moyenne et l'écart type.", 
                    " Met à l'échelle les données dans une plage spécifiée (par défaut, entre 0 et 1) en utilisant les valeurs min et max. Moins sensible aux valeurs aberrantes que StandardScaler.",
                    "Similaire à StandardScaler, mais utilise des estimations robustes pour la moyenne et l'écart type (médiane et écart interquartile). Moins sensible aux valeurs aberrantes."),
                    )
        # Normaliser avec StandardScaler
        if normalisation =='***StandardScaler***' : 
            norm = StandardScaler()
            data[numerical_variables] = norm.fit_transform(data[numerical_variables])

        # Normaliser avec MinMaxScaler
        elif normalisation =='***MinMaxScaler***' : 
            scaler_minmax = MinMaxScaler()
            data[numerical_variables] = scaler_minmax.fit_transform(data[numerical_variables])

        # Normaliser avec RobustScaler
        elif normalisation =='***RobustScaler***' : 
            scaler_robust = RobustScaler() 
            data[numerical_variables] = scaler_robust.fit_transform(data[numerical_variables])


    # Analyse Factorielle de Données Mixtes (AFDM)
    elif option =='Analyse Factorielle de Données Mixtes (AFDM)':

        # choisir les variables à appliquer à AFDM
        variables = st.sidebar.multiselect("Choisirles variables à appliquer a AFMD",data.columns.tolist())

        # Supprimer les variables sélectionnés
        if len(variables) != 0  : 
            data = data[variables]
           
    # Choisir le nombre de composant
    n_components =int(st.sidebar.number_input("Choisir le nombre de composant", value=2))
 
    # Soumettre ses choix
    soumettre = st.sidebar.button("Run", type="primary", use_container_width=True)

    
    if soumettre :

        # Appliquer ACP aux données
        if option =='Analyse des Composantes Principales (ACP)':
            pca = acp(data, categorical_variables, n_components)

            # Créer une session
            st.session_state["model"] = pca
            st.session_state["selected"] = "ACP"

        # Appliquer SVD aux données
        elif option == 'Décomposition en valeurs singulières (SVD)': 
            svd = svd(data, n_components)

            # Créer une session
            st.session_state["model"] = svd
            st.session_state["selected"] = "SVD"

        # Appliquer AFDM aux données
        elif option == 'Analyse Factorielle de Données Mixtes (AFDM)' :
            famd = afdm(data, n_components)

            # Créer une session
            st.session_state["model"] = famd
            
            st.session_state["selected"] = "FAMD"
        
        
    # Afficher  ACP / SVD /AFDM
    if "selected" in st.session_state:
        if st.session_state["selected"] == "ACP":
            plot_acp_afmd(st.session_state["model"], data, n_components)
        elif st.session_state["selected"] == "SVD":
            plot_svd(st.session_state["model"], data, n_components)
        else:
            plot_acp_afmd(st.session_state["model"], data, n_components)

        


else :
    st.warning("Veuillez choisir un fichier svp !",  icon="⚠️")


