from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"message": "API funcionando 🚀"})

@app.route("/pacientes")
def pacientes():
    data = [
        {"id":1,"nombre":"Juan"},
        {"id":2,"nombre":"Maria"}
    ]
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
