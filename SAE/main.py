import streamlit as st
import pandas as pd

# Configurer la page pour utiliser toute la largeur
st.set_page_config(layout="wide")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🏠 Accueil", "🔍 Exploration", "📊 Visualisation","📅 Réduction de dimension", "🥇 Classement", "❓ Aide"] )


with tab1:
  exec(open("pages/accueil.py", encoding="utf-8").read())

with tab2:
  exec(open("pages/exploration.py", encoding="utf-8").read())

with tab3:
   exec(open("pages/visualisation.py", encoding="utf-8").read())  # Importer le code directement

with tab4:
   exec(open("pages/reduction_dimension.py", encoding="utf-8").read()) 

with tab5:
   exec(open("pages/classement.py", encoding="utf-8").read())

with tab6:   
   exec(open("pages/aide.py", encoding="utf-8").read())  





    