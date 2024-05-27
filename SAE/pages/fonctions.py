import prince.svd
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import prince
from sklearn.impute import SimpleImputer
from sklearn.decomposition import TruncatedSVD


def nettoyage(data) : 
    """
     Cette fonction effectue plusieurs opérations de nettoyage sur un DataFrame de données.

        Paramètre :
            data : le DataFrame contenant les données à nettoyer.

        Retour : 
            Le Dataframe nettoyé
            La liste des noms des variables numériques.
            La liste des noms des variables catégorielles.
    """
    # Supprimer les colonnes qui contient que des Nan
    data_NaN = data.loc[:, data.isna().sum() == data.shape[0]]
    data = data.drop(columns=data_NaN.columns.tolist())
    # Selectionner les colonnes datetime
    datetime_columns = data.select_dtypes(include=['datetime64']).columns
    # Supprimer
    data.drop(columns=datetime_columns, inplace=True)

    numeric_and_categorical_variables = []
    for column in data.columns:

    # Vérifier si la colonne contient au moins une valeur numérique
        if any(isinstance(val, (int, float)) for val in data[column] if not pd.isna(val)):
            numeric_and_categorical_variables.append(column)
    numerical_variables = numeric_and_categorical_variables
    categorical_variables = data.select_dtypes(include="O").columns.tolist()

    # Sélectionner uniquement les variables qui n'ont aucune valeur numérique
    categorical_variables = list(set(categorical_variables).difference(numeric_and_categorical_variables))
        
    # Remplacer les chaines de caractères dans les variables numériques par NaN
    for var in numerical_variables:
        data[var] = pd.to_numeric(data[var], errors='coerce')

    # Imputer avec la moyenne
    imputer_numerical = SimpleImputer(strategy='mean')
    data[numerical_variables] = imputer_numerical.fit_transform(data[numerical_variables])

    # Imputer avec les plus fréquents
    for col in categorical_variables:
        most_frequent_value = data[col].value_counts().idxmax()
        data[col].fillna(most_frequent_value, inplace=True)
    
    return data, numerical_variables, categorical_variables 


def acp(data, var_categoricals) :
    """
        cette fonction applique l'Analyse en Composantes Principales (PCA) à un jeu de données avec des options 
        interactives pour la visualisation.

        Paramètres :
            data : le DataFrame contenant les données numériques à analyser.
            var_cat : la liste des noms de variables catégorielles dans les données.

        Retour : None
    """
    # Choisir le nombre de composant
    n_components =int(st.number_input("Choisir le nombre de composant", value=2))

    # Créer une instance de PCA
    pca = prince.PCA(n_components=n_components, rescale_with_mean=False, rescale_with_std=False,)

    # Adapter PCA à nos données numériques
    pca.fit(data, supplementary_columns=var_categoricals)

    #Transformer les données dans l'espace des composantes principales
    pca_result = pca.transform(data)

    # Résumer des valeurs propres
    st.title("Résumé des valeurs propres :")
    st.write(pca.eigenvalues_summary)

    # Appliquer PCA aux données(df_encoded)
    pca.transform(data).tail()

    # Paramètres interactifs
    x_component = st.selectbox('X Component', options=list(range(n_components)), index=0)
    y_component = st.selectbox('Y Component', options=list(range(1, n_components)), index=0)

    axe = st.selectbox('Choisir les axes à afficher', ('Individus', 'Variables'))

    # Dessiner le graphique
    if axe =='Individus': 
        chart = pca.plot(data, x_component=int(x_component), y_component=int(y_component),
                        show_row_markers=True,
                        show_column_markers=False,
                        show_row_labels=False,
                        row_labels_column=None,  # for DataFrames with a MultiIndex
                        show_column_labels=False
        )
    else :
        chart = pca.plot(data, x_component=int(x_component), y_component=int(y_component),
                        show_row_markers=True,
                        show_column_markers=True,
                        show_row_labels=False,
                        row_labels_column=None,  # for DataFrames with a MultiIndex
                        show_column_labels=False
        )

    # Afficher le graphique
    st.altair_chart(chart, use_container_width=True)

    # Afficher les individus les plus contributifs
    st.title("Les individus les plus contributifs à la construction des composantes principales :")
    # Choisir le nombre de personnes à afficher
    num_individuals = st.number_input("Nombre de personnes à afficher (max 20)", min_value=1, max_value=20, value=5)
    st.write(
        pca.row_contributions_
        .sort_values(0, ascending=False)
        .head(num_individuals)
        .style.format('{:.3%}')
    )

    # Afficher les variables les plus contributives
    st.title("Les variables qui ont le plus contribué à la construction des composantes principales suivant la première composante :")
    # Choisir le nombre de variables à afficher
    num_variables = st.number_input("Nombre de variables à afficher (max 20)", min_value=1, max_value=20, value=10)
    sorted_contributions = pca.column_contributions_.sort_values(ascending=False, by=0)
    top_contributions = sorted_contributions.head(num_variables)
    formatted_contributions = top_contributions.style.format('{:.0%}')
    st.write(formatted_contributions)



def afdm(data) :
    """
        cette fonction applique l'Analyse en Composantes Principales (PCA) à un jeu de données avec des options 
        interactives pour la visualisation.

        Paramètres :
            data : le DataFrame contenant les données à analyser.

        Retour : None
    """
    # Choisir le nombre de composant
    n_components = int(st.number_input("Choisir le nombre de composant", value=2))
   
    variables = st.multiselect("Choisirles variables à appliquer a AFMD",data.columns.tolist())
    if len(variables) != 0  : 
        data = data[variables]
        # Créer une instance de FAMD
        famd = prince.FAMD(n_components=n_components)

        # Adapter AFMD à nos données numériques
        famd.fit(data)

        # Résumer des valeurs propres
        st.title("Résumé des valeurs propres")
        st.write(famd.eigenvalues_summary)

        # Appliquer FAMD aux données(df)
        famd.transform(data).head() 

        # Paramètres interactifs
        x_component = st.selectbox('X Component', options=list(range(n_components)), index=0)
        y_component = st.selectbox('Y Component', options=list(range(1, n_components)), index=0)

        axe = st.selectbox('Choisir les axes à afficher', ('Individus', 'Variables'))

        # Dessiner le graphique
        if axe =='Individus': 
            chart = famd.plot(data, x_component=int(x_component), y_component=int(y_component),
                            show_row_markers=True,
                            show_column_markers=False,
                            show_row_labels=False,
                            row_labels_column=None,  # for DataFrames with a MultiIndex
                            show_column_labels=False
            )
        else :
            chart = famd.plot(data, x_component=int(x_component), y_component=int(y_component),
                            show_row_markers=True,
                            show_column_markers=True,
                            show_row_labels=False,
                            row_labels_column=None,  # for DataFrames with a MultiIndex
                            show_column_labels=False
            )

        # Afficher le graphique
        st.altair_chart(chart, use_container_width=True)

        # Afficher les individus les plus contributifs
        st.title("Les individus les plus contributifs à la construction des composantes principales :")

        # Choisir le nombre de personnes à afficher
        num_individuals = st.number_input("Nombre de personnes à afficher (max 20)", min_value=1, max_value=20, value=5)
        st.write(
            famd.row_contributions_
            .sort_values(0, ascending=False)
            .head(num_individuals)
            .style.format('{:.3%}')
        )

        # Afficher les variables les plus contributives
        st.title("Les variables qui ont le plus contribué à la construction des composantes principales suivant la première composante :")
        # Choisir le nombre de variables à afficher
        num_variables = st.number_input("Nombre de variables à afficher (max 20)", min_value=1, max_value=20, value=10)
        sorted_contributions = famd.column_contributions_.sort_values(ascending=False, by=0)
        top_contributions = sorted_contributions.head(num_variables)
        formatted_contributions = top_contributions.style.format('{:.0%}')
        st.write(formatted_contributions)
    else : 
        st.warning("Veuillez choisir des variables",  icon="⚠️")




def svd(data) :
    """
        cette fonction applique la décomposition en valeurs singulières (SVD) à un jeu de données avec des options 
        interactives pour la visualisation.

        Paramètres :
            data : le DataFrame contenant les données numériques à analyser.

        Retour : None
    """
    if data is not None :
        # Choisir le nombre de composant
        n_components = int(st.number_input("Choisir le nombre de composant", value=2))

        # Créer une instance de SVD
        svd = TruncatedSVD(n_components=n_components)
        TruncatedSVD(n_components=n_components)

        # Adapter AFMD à nos données numériques
        data_svd = svd.fit_transform(data)

        # Affichage des valeurs singulières
        st.title("Valeurs singulières")
        st.write(svd.singular_values_)
        
        # Affichage des composantes
        st.title(f"Données après réduction  de dimension")
        st.write(data_svd)

        # Résumé des valeurs singulières
        st.title("Variance expliquée par chaque composante")
        st.write(svd.explained_variance_ratio_)

        # Paramètres interactifs
        x_component = st.selectbox('X Component', options=list(range(n_components)), index=0)
        y_component = st.selectbox('Y Component', options=list(range(1, n_components)), index=0)

        # Afficher le graphe
        fig, ax = plt.subplots()
        ax.scatter(data_svd[:, x_component], data_svd[:, y_component])
        ax.set_xlabel(f'Composante {x_component}')
        ax.set_ylabel(f'Composante {y_component}')
        st.pyplot(fig)
    else : 
        st.write(" ")