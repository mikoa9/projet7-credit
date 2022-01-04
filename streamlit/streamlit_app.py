#Importation des librairies
import streamlit as st
from PIL import Image
import pandas as pd
import dash
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objs as go


# Lecture des données


# Lecture du modèle
clf_pipe = pickle.load(open('modele_final_Lightgbm_bank.md', 'rb'))

# Initialisation des algo : n plus proches voisins?
# Interprétation du modèle SHAP

# Dasboard avec streamlit

#img = Image.open("https://www.faire-un-credit.fr/wp-content/uploads/2021/02/faire-un-credit-en-ligne.png") 
#st.image(img, width=200) 

#Textes
st.header("Scoring crédit client")
st.subheader("Prédiction de la solvabilité d'un client pour l'obtention d'un crédit")

#champ identifiant client
st.text("Veuillez saisir l'identifiant du client")
name = st.text_input("", "Exemple d'identifiant : 122136...") 
  
if(st.button('Envoyez')): 
    result = name.title() 
    st.success(result) 

# faire une jauge
# N° client, crédit accepté ou non, score détaillé sous forme de jauge colorée 
# selon qu’il est en dessous ou au-dessus du seuil : 
#permet de juger s’il est loin du seuil ou non.

#https://community.plotly.com/t/plotly-js-gauge-pie-chart-data-order/8686

fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = 270,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Speed"}))

fig.show()

# Divers messages :
st.success("Success") 
  
st.info("Information") 
  
st.warning("Warning") 
  
st.error("Error") 

# Sa feature importance locale sous forme de graphique, 
#qui permet au chargé d’étude de comprendre quelles sont les données du client
# qui ont le plus influencé le calcul de son score


# Liste déroulante
feature = st.selectbox("features: ", 
                     ['Genre', 'Salaire', 'Type de logement']) 
  
st.write("Your feature: ", feature) 

# Le tableau de bord présentera également d’autres graphiques 
# sur les autres clients :
# 2 graphiques de features sélectionnées dans une liste déroulante, 
#présentant la distribution de la feature selon les classes, 
#ainsi que le positionnement de la valeur du client
# 	Un graphique d’analyse bi-variée entre les deux features sélectionnées, 
#avec un dégradé de couleur selon le score des clients, 
#et le positionnement du client
# 	La feature importance globale
# 	D’autres graphiques complémentaires
