from flask import Flask
import pickle
import os
import lightgbm as lgb
from lightgbm import LGBMClassifier
import pandas as pd
import numpy as np
import joblib

app = Flask(__name__)
model = {}

@app.route("/")
def running():
    return "<p>Serveur en route...</p>"

# Fonction executée qd on fait appel à l'API
@app.route("/predict/<client_id>")
def predict(client_id):
  sample_df = model["sample"]
  el = sample_df[sample_df["SK_ID_CURR"] == int(client_id)]
  el_mod = el.loc[:,~el.columns.isin(["SK_ID_CURR"])]
  # question 2: je ne peux utiliser que predict et non pas predict_proba, 
  # je ne sais pas à quoi correspond exactement la valeur retournée
  s = model["lightgbm"].predict(el_mod)
  c = { "client": client_id, "score":s.tolist()[0] }
  return c

# code à executer pour charger le modèle et données
@app.before_first_request
def load_model():
  # https://www.kaggle.com/bogorodvo/starter-code-saving-and-loading-lgb-xgb-cb
  basedir = os.path.abspath(os.path.dirname(__file__))
  data_file = os.path.join(basedir, 'model/modele_final_Lightgbm_bank.model')
  sample_file = os.path.join(basedir, 'model/app_sample.csv')
  # question 1: je ne peux importer que le booster, cela ne marche pas quand je fais pickle
  with open(data_file, "rb") as input_file:
    model["lightgbm_witherrornotfitted"] = pickle.load(input_file)
  model["lightgbm"] = lgb.Booster(model_file='model/modele_final_Lightgbm_bank.model')
  with open(sample_file, "rb") as input_file:
    model["sample"] = pd.read_csv(input_file)

if __name__ == "__main__":
  app.run(threaded=True, port=5000)