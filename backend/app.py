from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import joblib
from feature_extractor import extract_features
from urllib.parse import urlparse


app = Flask(__name__)
CORS(app)

# Load trained ML model
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")


def normalize_url(url):
    url = url.lower().strip()

    parsed = urlparse(url)

    domain = parsed.netloc

    if domain.startswith("www."):
        domain = domain[4:]

    return domain


@app.route("/check-url", methods=["POST"])
def check_url():
    
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    features = [extract_features(url)]

    normalized = normalize_url(url)
    url_vector = vectorizer.transform([normalized])
    prediction = model.predict(url_vector)[0]
    probability = model.predict_proba(url_vector)[0][1]


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
