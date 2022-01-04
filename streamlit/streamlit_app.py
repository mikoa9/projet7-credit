import streamlit as st
from PIL import Image

st.header("Scoring crédit client")
st.subheader("Prédiction de la solvabilité d'un client pour l'obtention d'un crédit")
st.text("Veuillez saisir l'identifiant du client")
name = st.text_input( "Exemple d'identifiant : 122136...") 
  
if(st.button('Envoyez')): 
    result = name.title() 
    st.success(result) 