#Importation des librairies
import streamlit as st
import streamlit.components.v1 as components

from PIL import Image
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import requests
import os
import shap
import pickle

# https://projet7-credit.herokuapp.com/predict/218461
# Lecture des données


# Lecture du modèle
# clf_pipe = pickle.load(open('modele_final_Lightgbm_bank.md', 'rb'))

# Initialisation des algo : n plus proches voisins? pour comparaison avec autres clients
# Interprétation du modèle SHAP

# Dasboard avec streamlit

#img = Image.open("https://www.faire-un-credit.fr/wp-content/uploads/2021/02/faire-un-credit-en-ligne.png") 
#st.image(img, width=200) 
def st_shap(plot, height=None):
    shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
    components.html(shap_html, height=height)

base_path = "/app/projet7-credit/streamlit"
# base_path = os.getcwd()
expected_value = [0.7219468377624242, -0.7219468377624242]
shap_values0 = pd.read_csv(base_path + '/shap/shap_values_0.shap')
shap_values1 = pd.read_csv(base_path + '/shap/shap_values_1.shap')
shap_values = [np.array(shap_values0), np.array(shap_values1)]
st_shap(shap.plots.force(expected_value[0], shap_values[0][99:100]))

#Textes
st.header("Scoring crédit client")
st.subheader("Prédiction de la solvabilité d'un client pour l'obtention d'un crédit")

#champ identifiant client
st.text("Veuillez saisir l'identifiant du client. Ex : 340061, 187416...")
name = st.text_input("", "Numéro d'identifiant") 
  
if(st.button('Envoyez')): 
    client_id = name.title() 
    response = requests.get("https://projet7-credit.herokuapp.com/predict/"+client_id)
    #https://community.plotly.com/t/plotly-js-gauge-pie-chart-data-order/8686
    # https://gist.github.com/tvst/b7bc2cb257ed88557037cb46e4baf80b
    fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = response.json()["score"][0],
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Score"}))

    st.write(fig)
    st.success(response.json()["score"])
    #client = sample_df[sample_df["SK_ID_CURR"] == int(client_id)]
    #explainer = shap.TreeExplainer(model)
    #shap_values = explainer.shap_values(client)
    #shap.summary_plot(shap_values, client)

# faire une jauge
# N° client, crédit accepté ou non, score détaillé sous forme de jauge colorée 
# selon qu’il est en dessous ou au-dessus du seuil : 
#permet de juger s’il est loin du seuil ou non.




# Divers messages :
# st.success("Success") 
  
# st.info("Information") 
  
# st.warning("Warning") 
  
# st.error("Error") 

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
