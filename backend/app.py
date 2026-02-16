from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import joblib

app = Flask(__name__)
CORS(app)

# Load trained ML model
model = joblib.load("model.pkl")


def extract_features(url):
    return [
        len(url),
        url.count('.'),
        int("@" in url),
        int(bool(re.search(r"(\d{1,3}\.){3}\d{1,3}", url))),
        sum(keyword in url.lower() for keyword in [
            "login", "verify", "update", "secure",
            "bank", "account", "confirm", "password"
        ])
    ]


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
