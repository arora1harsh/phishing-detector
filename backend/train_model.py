import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load dataset
df = pd.read_csv("phishing.csv")

# Drop unnecessary column
df = df.drop(columns=["index"])

# Features and target
X = df.drop(columns=["Result"])
y = df["Result"]

# Convert target: (-1 → 0), (1 → 1)
y = y.replace(-1, 0)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train Random Forest
model = RandomForestClassifier(n_estimators=200, random_state=42)
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
