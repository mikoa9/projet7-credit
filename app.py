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

@app.route("/predict/<client_id>")
def predict(client_id):
  sample_df = model["sample"]
  el = sample_df[sample_df["SK_ID_CURR"] == int(client_id)]
  el_mod = el.loc[:,~el.columns.isin(["SK_ID_CURR"])]
  s = model["lightgbm"].predict(el_mod)
  c = { "client": client_id, "score":s.tolist()[0] }
  return c

@app.before_first_request
def load_model():
  # https://www.kaggle.com/bogorodvo/starter-code-saving-and-loading-lgb-xgb-cb
  basedir = os.path.abspath(os.path.dirname(__file__))
  data_file = os.path.join(basedir, 'model/modele_final_Lightgbm_bank.sav')
  sample_file = os.path.join(basedir, 'model/app_sample.csv')
  model["lightgbm"] = lgb.Booster(model_file='model/modele_final_Lightgbm_bank.sav')
  with open(sample_file, "rb") as input_file:
    model["sample"] = pd.read_csv(input_file)

if __name__ == "__main__":
  app.run(threaded=True, port=5000)