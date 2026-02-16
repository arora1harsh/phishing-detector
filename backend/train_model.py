import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

# Sample dataset (we'll upgrade later with real dataset)
data = {
    "url": [
        "https://google.com",
        "https://github.com",
        "http://192.168.0.1/login@fake.com",
        "http://verify-account-secure-login.com",
        "https://bank-update-confirm.com/login",
        "https://wikipedia.org"
    ],
    "label": [0, 0, 1, 1, 1, 0]  # 0 = Safe, 1 = Phishing
}

df = pd.DataFrame(data)


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


# Feature extraction
X = df["url"].apply(extract_features).tolist()
y = df["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, predictions))

# Save model
joblib.dump(model, "model.pkl")
print("Model saved as model.pkl")
