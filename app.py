from flask import Flask

app = Flask(__name__)
model = None

@app.route("/")
def running():
    return "<p>Serveur en route...</p>"

@app.route("/predict/<client_id>")
def predict(client_id):
  c = { "o": client_id, "model":model }
  return c

@app.before_first_request
def load_model():
  model = 1

if __name__ == "__main__":
  app.run(threaded=True, port=5000)