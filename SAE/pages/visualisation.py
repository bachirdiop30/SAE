import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.header("Visualisation")

if 'data_name' in st.session_state:
    df = st.session_state['data_name']  # Accède directement au DataFrame stocké

    # Visualisation des variables catégorielles
    st.subheader("Visualisation des variables catégorielles")
    if df.select_dtypes(include=['object', 'category']).columns.empty:
        st.write("Aucune variable catégorielle trouvée.")
    else:
        variable_cat = st.selectbox("Choisir une variable catégorielle", df.select_dtypes(include=['object', 'category']).columns)
        sns.set_style("darkgrid")
        fig, ax = plt.subplots(figsize=(20, 6))
        if len(df[variable_cat].unique()) > 50:
            unique_categories = df[variable_cat].unique()
            window = 50
            part = st.slider("Choisir la partie à afficher", 0, len(unique_categories) // window - 1)
            categories = unique_categories[part * window:part * window + window]
            sns.histplot(data=df[df[variable_cat].isin(categories)][variable_cat], ax=ax)
        else:
            sns.histplot(data=df[variable_cat], ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        plt.xlabel('Catégorie')
        plt.ylabel('Fréquence')
        plt.title(f'Diagramme en barres: {variable_cat}')
        st.pyplot(fig)
        ab=pd.DataFrame(df[variable_cat].value_counts().sort_values(ascending=False)).head(20)
        st.write(ab)

    # Visualisation des variables numériques
    st.subheader("Visualisation des variables numériques")
    numerical_variables = df.select_dtypes(include=['int', 'float']).columns.tolist()
    if not numerical_variables:
        st.write("Aucune variable numérique trouvée.")
    else:
        @st.cache_data  # Utilisation du cache pour éviter de recalculer à chaque interaction
        def plot_data(variable):
            fig, axs = plt.subplots(1,2, figsize=(12, 6))
            sns.histplot(data=df, x=variable, ax=axs[0], bins=10)
            axs[0].set_xlabel(variable)
            axs[0].set_ylabel('Fréquence')
            axs[0].set_title('Histogramme')

            sns.boxplot(data=df, y=variable, ax=axs[1])
            axs[1].set_xlabel(variable)
            axs[1].set_ylabel('Valeur')
            axs[1].set_title('Boîte à moustaches')

            # Adapter la disposition
            plt.tight_layout()

            # Afficher le graphique
            st.pyplot(fig)
            return pd.DataFrame(df[variable].describe())

        variable_num = st.selectbox("Choisir une variable numérique", numerical_variables)
        plot_data(variable_num)

    # Analyse multivariée
    st.header("Analyse multi-variée")

    if 'data_name' in st.session_state:
        df = st.session_state['data_name']  # Accède directement au DataFrame stocké

        numerical_variables = df.select_dtypes(include=['int', 'float']).columns.tolist()
        categorical_variables = df.select_dtypes(include=['object', 'category']).columns.tolist()

        x_variable = st.selectbox("Choisir une variable pour l'axe x", numerical_variables + categorical_variables)
        y_variable = st.selectbox("Choisir une variable pour l'axe y", [None] + numerical_variables + categorical_variables)
        hue_variable = st.selectbox("Choisir une variable pour la teinte", [None] + categorical_variables)
        plot_type = st.selectbox("Choisir un type de graphique", ["scatter", "boxplot", "histplot"])

        if plot_type == "scatter" and x_variable and y_variable and x_variable in numerical_variables and y_variable in numerical_variables:
            fig, ax = plt.subplots()
            sns.scatterplot(data=df, x=x_variable, y=y_variable, hue=hue_variable, ax=ax)
            ax.set_xlabel(x_variable)
            ax.set_ylabel(y_variable)
            ax.set_title("Nuage de points")
            st.pyplot(fig)

        elif plot_type == "boxplot" and x_variable and y_variable and x_variable in categorical_variables and y_variable in numerical_variables:
            fig, ax = plt.subplots()
            sns.boxplot(data=df, x=x_variable, y=y_variable, hue=hue_variable, ax=ax)
            ax.set_xlabel(x_variable)
            ax.set_ylabel(y_variable)
            ax.set_title("Boxplot")
            st.pyplot(fig)

        elif plot_type == "histplot" and x_variable and hue_variable and x_variable in categorical_variables:
            fig, ax = plt.subplots()
            sns.histplot(data=df, x=x_variable, hue=hue_variable, multiple="stack", ax=ax)
            ax.set_xlabel(x_variable)
            ax.set_ylabel("Fréquence")
            ax.set_title("Histogramme")
            st.pyplot(fig)

        if y_variable and y_variable in numerical_variables:
            st.write(df.groupby([x_variable, hue_variable])[y_variable].describe())

    else:
        st.write("Aucune donnée chargée. Veuillez retourner à l'accueil et télécharger un fichier.")
