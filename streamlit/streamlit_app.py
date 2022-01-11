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

if 'clicked' not in st.session_state:
    st.session_state['clicked'] = False

# Impression image (features globale)
threshold = 0.5538

#Méthode pour afficher le force plot de shap
def st_shap(plot, height=None):
    shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
    components.html(shap_html, height=height)

#Top N colonne pour un client
def get_top_columns(shap_vals, index, f_names, num):
    l = []
    # https://github.com/slundberg/shap/issues/632
    for name in np.flip(np.argsort(np.abs(shap_vals[index]))[-num:]):
        l.append(f_names[name])
    return l

# Shap values de la classe 0 
base_path = "/app/projet7-credit/streamlit"
# base_path = os.getcwd()
expected_value = [0.7214676881413614, -0.7214676881413614]
with open(base_path + '/shap/shap_values.shap', "rb") as input_file:
  shap_values = pickle.load(input_file)
# Chargement de données 
sample = pd.read_csv(base_path + '/model/app_sample_normalized.csv')
feature_names = sample.columns[~sample.columns.isin(["SK_ID_CURR","TARGET"])].tolist()
sample = sample.reset_index()

# Image features globales
image = Image.open(base_path + '/shap/distribution.png')
image_logo = Image.open(base_path + '/image/dash3.PNG')
st.image(image_logo)

#Textes
st.header("Scoring crédit client")
st.subheader("1. Prédiction de la solvabilité d'un client pour l'obtention d'un prêt")

#champ identifiant client
st.text("Veuillez saisir l'identifiant du client. Ex : 332641, 369125, 104353...")
name = st.text_input("", "Numéro d'identifiant") 

if st.button('Envoyez') or st.session_state.clicked: 
    st.session_state.clicked = True
    client_id = name.title() 
    response = requests.get("https://projet7-credit.herokuapp.com/predict/"+client_id)
    # https://community.plotly.com/t/plotly-js-gauge-pie-chart-data-order/8686
    # https://gist.github.com/tvst/b7bc2cb257ed88557037cb46e4baf80b
    zero_proba = response.json()["score"][0]

    # Création jauge
    fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = response.json()["score"][0],
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Score"},
    gauge = { 'axis': {'range':[0,1]}}))

    if(zero_proba > threshold):
        st.success("Le client a " + "{:.2%}".format(zero_proba) + " de probabilité de remboursement.")
        fig.update_traces(gauge_bar_color="green")
    else:
        fig.update_traces(gauge_bar_color="red")
        st.error("Le client a " +"{:.2%}".format(1 - zero_proba)+ " de probabilité de défaut de paiement.")

    # Affichage de la jauge
    st.write(fig)
    start = int(sample[sample["SK_ID_CURR"] == int(client_id)]["index"])
    #end = start + 1


    st.subheader("2. Influence des variables sur le score du client– TOP 10")
    st.write("Conseil au chargé clientèle : en cas de refus ou d'obtention de prêt, vous pouvez expliquer au client les variables qui ont impacté ce choix")
    # Force plot (features locales)
    st_shap(shap.plots.force(expected_value[0], shap_values[start], feature_names))


    # waterfall (features locales)
    fig, ax = plt.subplots()
    shap.plots._waterfall.waterfall_legacy(expected_value[0], shap_values[start], feature_names=feature_names)
    st.pyplot(fig, bbox_inches='tight',dpi=300,pad_inches=0)
    plt.clf()
    
    st.subheader("3. Importance  des variables tout client confondu")
    st.write("Conseil au chargé clientèle : il peut être intéressant d'expliquer au client, quelles sont les variables qui influencent le plus pour l'obtention d'un prêt")
    # Impression image (features globale)
    st.image(image, caption='L\'importance de chaque caractéristique dans la décision')
    

    st.subheader("4. Distribution des variables et situation du client sur les 10 principales variables")
    st.text("Le rond bleu représente la valeur du client sélectionné")
    #boxplot
    # Récupérer les top 10 colonnes
    top_cols = get_top_columns(shap_values, start, feature_names, 10)
    fig, ax = plt.subplots()
    fig.set_figwidth(30)
    fig.set_figheight(10)
    sns.boxplot(data=sample[top_cols])
    sns.stripplot(data=sample[sample["SK_ID_CURR"] == int(client_id)][top_cols], color='blue',linewidth=1, size=20)
    st.pyplot(fig, bbox_inches='tight',dpi=300,pad_inches=0)
    plt.clf()

    st.subheader("5. Visualisation d'une ou plusieurs variables sélectionnées")
    # Liste déroulante
    Variable = st.selectbox("feature_names 1:", feature_names) 
    fig, ax = plt.subplots()
    histplot = sns.histplot(data=sample, x=Variable, hue="TARGET")
    histplot.axvline(float(sample[sample["SK_ID_CURR"] == int(client_id)][Variable]), color='red')
    st.pyplot(fig, bbox_inches='tight',dpi=300,pad_inches=0)
    plt.clf()

    # Liste déroulante
    Variable2 = st.selectbox("feature_names 2:", feature_names) 
    fig, ax = plt.subplots()
    histplot2 = sns.histplot(data=sample, x=Variable2, hue="TARGET")
    histplot2.axvline(float(sample[sample["SK_ID_CURR"] == int(client_id)][Variable2]), color='red')
    st.pyplot(fig, bbox_inches='tight',dpi=300,pad_inches=0)
    plt.clf()

    


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


