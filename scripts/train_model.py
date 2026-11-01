import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

import joblib


# Load dataset
data = pd.read_csv("../data/tinyml_dataset.csv")

# Features
X = data.drop("label", axis=1)

# Labels
y = data["label"]


# Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Create ML model
model = RandomForestClassifier(
    n_estimators=50,
    max_depth=5,
    random_state=42
)


# TRAIN
print("Training model...")
model.fit(X_train, y_train)


# TEST
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print()
print("================================")
print("MODEL RESULTS")
print("================================")
print("Accuracy:", accuracy * 100, "%")
print()
print(classification_report(y_test, predictions))


# SAVE MODEL
joblib.dump(model, "../models/edgesentinel_model.pkl")

print("Model saved!")