import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from urllib.parse import urlparse


# Load dataset
df = pd.read_csv("URL_dataset.csv")

def normalize_url(url):
    try:
        url = str(url).lower().strip()
        parsed = urlparse(url)
        domain = parsed.netloc

        if domain.startswith("www."):
            domain = domain[4:]

        return domain

    except Exception:
        return ""   # return empty string if malformed


df = pd.read_csv("URL_dataset.csv")

df["label"] = df["type"].map({
    "legitimate": 0,
    "phishing": 1
})

# 🔥 THIS IS CRITICAL
df["url"] = df["url"].apply(normalize_url)

X = df["url"]
y = df["label"]


# Train-test split with stratification
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Character-level TF-IDF
vectorizer = TfidfVectorizer(
    analyzer="char",
    ngram_range=(3,5),   # character n-grams
    max_features=50000
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Logistic Regression (regularized)
model = LogisticRegression(
    max_iter=200,
    class_weight="balanced"
)

model.fit(X_train_vec, y_train)

# Evaluate
predictions = model.predict(X_test_vec)

print("Model Accuracy:", accuracy_score(y_test, predictions))
print("\nClassification Report:")
print(classification_report(y_test, predictions))

# Save model + vectorizer
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("\nModel and vectorizer saved.")
