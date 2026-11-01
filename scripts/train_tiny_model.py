import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score

import joblib


# Load dataset
data = pd.read_csv("../data/tinyml_dataset.csv")

X = data.drop("label", axis=1)
y = data["label"]


# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Small decision tree
model = DecisionTreeClassifier(
    max_depth=5,
    min_samples_leaf=10,
    random_state=42
)


print("Training TinyML model...")

model.fit(X_train, y_train)


# Test
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print()
print("==============================")
print("TINYML MODEL")
print("==============================")

print("Accuracy:", round(accuracy * 100, 2), "%")


print()
print("==============================")
print("MODEL RULES")
print("==============================")

print(
    export_text(
        model,
        feature_names=list(X.columns)
    )
)


# Save
joblib.dump(
    model,
    "../models/edgesentinel_tiny_model.pkl"
)

print("TinyML model saved!")