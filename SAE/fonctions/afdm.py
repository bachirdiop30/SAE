import streamlit as st
import prince


def afdm(data, n_components):
    """
        cette fonction applique l'Analyse Factorielle de Données Mixtes (AFDM) à un jeu de données 
        
        Paramètres :
            data : le DataFrame contenant les données à analyser.

        Retour : Objet afdm
    """

    # Créer une instance de FAMD
    famd = prince.FAMD(n_components=n_components)

    # Adapter AFMD à nos données numériques
    famd.fit(data)

    return famd

