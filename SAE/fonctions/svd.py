import streamlit as st
import matplotlib.pyplot as plt
from sklearn.decomposition import TruncatedSVD


def svd(data, n_components) :
    """
        cette fonction applique la décomposition en valeurs singulières (SVD) à un jeu de données avec des options 
        interactives pour la visualisation.

        Paramètres :
            data : le DataFrame contenant les données numériques à analyser.

        Retour : None
    """

    # Créer une instance de SVD
    svd = TruncatedSVD(n_components=n_components)
    TruncatedSVD(n_components=n_components)

    # Adapter AFMD à nos données numériques
    svd.fit_transform(data)

    return svd



def plot_svd(svd, data, n_components) :

    # Affichage des valeurs singulières
    st.title("Valeurs singulières")
    st.write(svd.singular_values_)
    
    # Affichage des composantes
    st.title(f"Données après réduction  de dimension")
    st.write(data)

    # Résumé des valeurs singulières
    st.title("Variance expliquée par chaque composante")
    st.write(svd.explained_variance_ratio_)

    # Paramètres interactifs
    x_component = st.selectbox('X Component', options=list(range(n_components)), index=0)
    y_component = st.selectbox('Y Component', options=list(range(1, n_components)), index=0)

    # Afficher le graphe
    fig, ax = plt.subplots()
    ax.scatter(data.iloc[:, x_component], data.iloc[:, y_component])
    ax.set_xlabel(f'Composante {x_component}')
    ax.set_ylabel(f'Composante {y_component}')
    st.pyplot(fig)