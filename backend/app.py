from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import joblib
from feature_extractor import extract_features


app = Flask(__name__)
CORS(app)

# Load trained ML model
model = joblib.load("model.pkl")



@app.route("/check-url", methods=["POST"])
def check_url():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    features = [extract_features(url)]

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    if prediction == 1:
        verdict = "Phishing"
    else:
        verdict = "Safe"

    return jsonify({
        "verdict": verdict,
        "phishing_probability": round(probability * 100, 2)
    })


if __name__ == "__main__":
    app.run(debug=True)
