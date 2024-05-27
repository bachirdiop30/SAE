import os
import sys 
package_dir = os.getcwd() # C:\\Users\\amina\\SAE
sys.path.append(os.path.join(package_dir, "pages"))
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import prince
from fonctions import nettoyage, acp, afdm, svd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler


st.title("Analyse factorielle des données")

#Récuperer le dataframe 
if "data_name" in st.session_state :
    df = st.session_state["data_name"]

    # Sélectionner une mèthode d'analyse
    option = st.selectbox(
        'Méthode d\'analyse factorielle',
        ('Analyse des Composantes Principales (ACP)', 'Analyse Factorielle de Données Mixtes (AFDM)', 'Décomposition en valeurs singulières (SVD)'),
        index=None,
        placeholder="sélectionnez une méthode d'analyse factorielle",)


    #Analyse des Composantes Principales (ACP)
    if option == 'Analyse des Composantes Principales (ACP)' or option == 'Décomposition en valeurs singulières (SVD)':

        #Prétraitement des données
        st.write("""
                Pour une réduction de dimension efficace dans notre application, le prétraitement des données est une étape essentielle. 
                """)
        pretraitement = st.radio("Nous offrons deux options pour les données catégorielles :",
            ["***Supprimer les données catégorielles***", "***Encoder les données catégorielles***"],
            captions = ("si elles ne sont pas pertinentes pour votre analyse, cette option les éliminera de l'ensemble de données.", 
                        "convertissez-les en valeurs numériques pour les utiliser dans l'analyse factorielle."),
            index=None)
        
        # Supprimer les variables catégorielles
        if pretraitement == "***Supprimer les données catégorielles***" : 

            data,numerical_variables, categorical_variables = nettoyage(df)
            # Supprimer les colonnes qui contient que des Nan
            data = data.drop(columns=categorical_variables)
            categorical_variables = []
            

        # Encoder les variables catégorielles   
        elif pretraitement == "***Encoder les données catégorielles***" :
            
            df,numerical_variables, categorical_variables = nettoyage(df)

            # Supprimer les colonnes numériques avec une très faible variance
            threshold = .8 * (1 - .8)
            numeric_cols_low_variance = df[numerical_variables].columns[df[numerical_variables].var() < threshold]
            df.drop(columns=numeric_cols_low_variance, inplace=True)

            # Supprimer les colonnes catégorielles avec une seule catégorie
            categorical_cols_one_category = df[categorical_variables].columns[df[categorical_variables].nunique() == 1]
            df.drop(columns=categorical_cols_one_category, inplace=True)

            # Mise à jour des variables
            numerical_variables = list(set(numerical_variables).difference(numeric_cols_low_variance))
            categorical_variables = list(set(categorical_variables).difference(categorical_cols_one_category))

            #Initialiser LabelEncoder
            data = df.copy()

            label_encoder = LabelEncoder()

            # Parcourir chaque variable catégorielle et l'encoder
            for col in categorical_variables:
                
                data[col] = label_encoder.fit_transform(data[col])

        # Si on choisit ACP
        if option == 'Analyse des Composantes Principales (ACP)' : 

            # Normalisation des données et ACP
            if pretraitement == "***Supprimer les données catégorielles***" or pretraitement == "***Encoder les données catégorielles***" :

                st.write("""Après avoir prétraité les données, nous passons maintenant à l'étape de normalisation, qui 
                        consiste à mettre à l'échelle les caractéristiques des données pour les préparer à l'analyse ou 
                        à la modélisation. """)
                
                normalisation = st.radio("Nous présentons maintenant trois méthodes pour la normalisation des données :",
                    ["***StandardScaler***", "***MinMaxScaler***", "***RobustScaler***"],
                    captions = (" Centre les données autour de zéro et les met à l'échelle de manière à avoir une variance unitaire. Sensible aux valeurs aberrantes car utilise la moyenne et l'écart type.", 
                                " Met à l'échelle les données dans une plage spécifiée (par défaut, entre 0 et 1) en utilisant les valeurs min et max. Moins sensible aux valeurs aberrantes que StandardScaler.",
                                "Similaire à StandardScaler, mais utilise des estimations robustes pour la moyenne et l'écart type (médiane et écart interquartile). Moins sensible aux valeurs aberrantes."),
                    index=None)

                if normalisation =='***StandardScaler***' : 
                    norm = StandardScaler()
                    data[numerical_variables] = norm.fit_transform(data[numerical_variables])

                    # Appliquer ACP auxdonnées
                    acp(data, categorical_variables)
                    
                elif normalisation =='***MinMaxScaler***' : 
                    scaler_minmax = MinMaxScaler()
                    data[numerical_variables] = scaler_minmax.fit_transform(data[numerical_variables])

                    # Appliquer ACP auxdonnées
                    acp(data, categorical_variables)

                elif normalisation =='***RobustScaler***' : 
                    scaler_robust = RobustScaler() 
                    data[numerical_variables] = scaler_robust.fit_transform(data[numerical_variables])

                    # Appliquer ACP auxdonnées
                    acp(data, categorical_variables )
        elif option == 'Décomposition en valeurs singulières (SVD)': 
            if 'data' not in locals():
                st.warning("Veuillez d'abord prétraiter les données.")
            else:
                svd(data)

    # Analayse factorielle des données mixtes(AFDM)
    elif option =='Analyse Factorielle de Données Mixtes (AFDM)' :  

        df, numerical_variables, categorical_variables = nettoyage(df)

        # Appliquer AFDM à nos données
        afdm(df)


else :
    st.warning("Veuillez choisir un fichier svp !",  icon="⚠️")


