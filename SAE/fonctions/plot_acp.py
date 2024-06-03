import streamlit as st
import prince


def plot_acp_afmd(model, data, n_components) : 

    """
    Fonction interactive pour visualiser les résultats d'une ACP ou d'une AFMD.

    Paramètres :
        - model : Objet ACP ou AFDM ayant les attributs `eigenvalues_summary`, `row_contributions_`, et `column_contributions_`.
        - data : Jeu de données utilisé pour l'ACP ou AFMD.
        - n_components : Nombre de composantes principales.
  
    """

     # Résumer des valeurs propres
    st.title("Résumé des valeurs propres :")
    st.write(model.eigenvalues_summary)

     # Paramètres interactifs
    x_component = st.selectbox('X Component', options=list(range(n_components)), index=0)
    y_component = st.selectbox('Y Component', options=list(range(1, n_components)), index=0)

    axe = st.selectbox('Choisir les axes à afficher', ('Individus', 'Variables'))

    # Dessiner le graphique
    if axe =='Individus': 
        chart = model.plot(data, x_component=int(x_component), y_component=int(y_component),
                        show_row_markers=True,
                        show_column_markers=False,
                        show_row_labels=False,
                        row_labels_column=None,  # for DataFrames with a MultiIndex
                        show_column_labels=False
        )
    elif axe =='Variables':
        chart = model.plot(data, x_component=int(x_component), y_component=int(y_component),
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
    num_individuals = st.number_input("Nombre de personnes à afficher (max 20)", min_value=1, max_value=20, value=10)
    st.write(
        model.row_contributions_
        .sort_values(0, ascending=False)
        .head(num_individuals)
        .style.format('{:.3%}')
    )

    # Afficher les variables les plus contributives
    st.title("Les variables qui ont le plus contribué à la construction des composantes principales suivant la première composante :")
    # Choisir le nombre de variables à afficher
    num_variables = st.number_input("Nombre de variables à afficher (max 20)", min_value=1, max_value=20, value=5)
    sorted_contributions = model.column_contributions_.sort_values(ascending=False, by=0)
    top_contributions = sorted_contributions.head(num_variables)
    formatted_contributions = top_contributions.style.format('{:.0%}')
    st.write(formatted_contributions)


