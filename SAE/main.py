import streamlit as st
import pandas as pd

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 20px !important; # Set the width to your desired value
           background-color: #061E42 !important;
           background-image: none !important;
        }
        section[data-testid="stTabs"]{
             width: 100px !important; # Set the width to your desired value
        }  

    </style>
    """,
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Accueil", "Exploration", "Visualisation","Réduction de dimension", "Classement", "Aide"] )

with tab1:
   st.header("Accueil")
   st.write("Accueil du site")
   uploaded_file = st.file_uploader("Choose a file")
   if uploaded_file is not None:
      st.session_state["data_name"] = uploaded_file
      df = pd.read_csv(uploaded_file) # utiliser --server.maxUploadSize 500 pour modifier la taille max du fichier
      st.write(df)

with tab2:
   st.header("Exploration")
   st.write("Exploration des données")

with tab3:
   st.header("Visualisation")
   st.write("visualiser des graphes")

with tab4:
   st.header("Analyse factorielle")
   st.write("ACP et AFDM") 

with tab5:
   st.header("Classement")
   st.write("faire un classement")

with tab6:   
   st.header("help")
   st.write("aide pour les models")  
   

#sidebar 
# Inject custom CSS to set the width of the sidebar

# Example sidebar content
st.sidebar.header("This is the sidebar")
st.sidebar.text("This is some text in the sidebar")



    