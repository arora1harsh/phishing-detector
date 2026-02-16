from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

def calculate_risk(url):
    score = 0

    # Rule 1: Very long URL
    if len(url) > 75:
        score += 2

    # Rule 2: Contains @ symbol
    if "@" in url:
        score += 3

    # Rule 3: Too many dots
    if url.count('.') > 3:
        score += 2

    # Rule 4: IP address instead of domain
    ip_pattern = r"(\d{1,3}\.){3}\d{1,3}"
    if re.search(ip_pattern, url):
        score += 3

    # Rule 5: Suspicious keywords
    suspicious_keywords = [
        "login", "verify", "update", "secure",
        "bank", "account", "confirm", "password"
    ]

    for keyword in suspicious_keywords:
        if keyword in url.lower():
            score += 1

    return score



@app.route("/check-url", methods=["POST"])
def check_url():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    risk_score = calculate_risk(url)

    if risk_score >= 5:
        verdict = "High Risk"
    elif risk_score >= 2:
        verdict = "Suspicious"
    else:
        verdict = "Safe"


    return jsonify({
        "risk_score": risk_score,
        "verdict": verdict
    })


if __name__ == "__main__":
    app.run(debug=True)
