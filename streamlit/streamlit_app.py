import streamlit as st
from PIL import Image

img = Image.open("https://www.faire-un-credit.fr/wp-content/uploads/2021/02/faire-un-credit-en-ligne.png") 
  
st.image(img, width=200) 
st.header("Scoring crédit client")
st.subheader("Prédiction de la solvabilité d'un client pour l'obtention d'un crédit")
st.text("Veuillez saisir l'identifiant du client")
name = st.text_input("", "Exemple d'identifiant : 122136...") 
  
if(st.button('Envoyez')): 
    result = name.title() 
    st.success(result) 

st.success("Success") 
  
st.info("Information") 
  
st.warning("Warning") 
  
st.error("Error") 

feature = st.selectbox("features: ", 
                     ['Genre', 'Salaire', 'Type de logement']) 
  
st.write("Your feature: ", feature) 

