import streamlit as st
import prince


def acp(data, var_categoricals, n_components) :
    """
        cette fonction applique l'Analyse en Composantes Principales (PCA) à un jeu de données 

        Paramètres :
            data : le DataFrame contenant les données numériques à analyser.
            var_cat : la liste des noms de variables catégorielles dans les données.

        Retour : Objet ACP
    """
    
    # Créer une instance de PCA
    pca = prince.PCA(n_components=n_components, rescale_with_mean=False, rescale_with_std=False,)

    # Adapter PCA à nos données numériques
    pca.fit(data, supplementary_columns=var_categoricals)

    return pca