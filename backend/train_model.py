import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from feature_extractor import extract_features

# Load dataset
df = pd.read_csv("URL_dataset.csv")

# Convert labels
df["label"] = df["type"].map({
    "legitimate": 0,
    "phishing": 1
})

# Extract features
X = df["url"].apply(extract_features).tolist()
y = df["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=None,
    random_state=42
)

model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, predictions)
print("Model Accuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, predictions))

# Save model
joblib.dump(model, "model.pkl")
print("\nModel saved as model.pkl")
