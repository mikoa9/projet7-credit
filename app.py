from flask import Flask

app = Flask(__name__)

@app.route("/")
def running():
    return "<p>Serveur en route...</p>"

@app.route("/predict/<client_id>")
def predict(client_id):
  return { c:client_id };

if __name__ == "__main__":
  app.run(threaded=True, port=5000)