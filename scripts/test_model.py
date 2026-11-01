import numpy as np
import joblib

model = joblib.load("../models/edgesentinel_model.pkl")


def features(temp, moisture):
    return [
        np.mean(temp),
        np.var(temp),
        np.min(temp),
        np.max(temp),
        temp[-1] - temp[0],

        np.mean(moisture),
        np.var(moisture),
        np.min(moisture),
        np.max(moisture),
        moisture[-1] - moisture[0]
    ]


# NORMAL: stable temperature + moisture
normal_temp = [27.0, 27.1, 27.0, 27.1, 27.0,
               27.1, 27.0, 27.1, 27.0, 27.1]

normal_moisture = [50, 50, 51, 50, 50,
                   51, 50, 50, 51, 50]


# WARNING: temperature rising + moisture falling
warning_temp = [27, 27.2, 27.4, 27.6, 27.8,
                28.0, 28.2, 28.4, 28.6, 28.8]

warning_moisture = [60, 59, 58, 57, 56,
                    55, 54, 53, 52, 51]


# CRITICAL: temperature rapidly rising + moisture rapidly falling
critical_temp = [28, 28.8, 29.6, 30.4, 31.2,
                 32.0, 32.8, 33.6, 34.4, 35.2]

critical_moisture = [70, 64, 58, 52, 46,
                     40, 34, 28, 22, 16]


tests = [
    ("NORMAL", normal_temp, normal_moisture),
    ("WARNING", warning_temp, warning_moisture),
    ("CRITICAL", critical_temp, critical_moisture)
]


for name, temp, moisture in tests:

    x = np.array(features(temp, moisture)).reshape(1, -1)

    prediction = model.predict(x)[0]
    probabilities = model.predict_proba(x)[0]

    labels = {
        0: "NORMAL",
        1: "WARNING",
        2: "CRITICAL"
    }

    confidence = probabilities[prediction] * 100

    print("--------------------------------")
    print("Expected :", name)
    print("Predicted:", labels[prediction])
    print("Confidence:", round(confidence, 2), "%")