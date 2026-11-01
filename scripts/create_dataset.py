import pandas as pd
import numpy as np

data = pd.read_csv("../data/normal.csv")

WINDOW = 10


def extract_features(temp, moisture):
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


dataset = []


# =====================================================
# NORMAL
# =====================================================

# Real normal sensor data
for i in range(len(data) - WINDOW + 1):

    temp = data["temperature"].iloc[i:i+WINDOW].values
    moisture = data["moisture"].iloc[i:i+WINDOW].values

    dataset.append(
        extract_features(temp, moisture) + [0]
    )


# Additional normal situations
for _ in range(500):

    start_temp = np.random.uniform(24, 35)
    start_moisture = np.random.uniform(20, 80)

    temp = start_temp + np.random.normal(0, 0.08, WINDOW)

    moisture = start_moisture + np.random.normal(0, 0.8, WINDOW)

    dataset.append(
        extract_features(temp, moisture) + [0]
    )


# =====================================================
# WARNING
# Temperature rises slowly
# Moisture falls slowly
# =====================================================

for _ in range(500):

    start_temp = np.random.uniform(24, 35)
    start_moisture = np.random.uniform(20, 80)

    temp_step = np.random.uniform(0.08, 0.25)
    moisture_step = np.random.uniform(0.5, 1.5)

    temp = (
        start_temp
        + np.arange(WINDOW) * temp_step
        + np.random.normal(0, 0.05, WINDOW)
    )

    moisture = (
        start_moisture
        - np.arange(WINDOW) * moisture_step
        + np.random.normal(0, 0.3, WINDOW)
    )

    dataset.append(
        extract_features(temp, moisture) + [1]
    )


# =====================================================
# CRITICAL
# Temperature rises rapidly
# Moisture falls rapidly
# =====================================================

for _ in range(500):

    start_temp = np.random.uniform(24, 35)
    start_moisture = np.random.uniform(20, 80)

    temp_step = np.random.uniform(0.3, 0.7)
    moisture_step = np.random.uniform(2.0, 4.0)

    temp = (
        start_temp
        + np.arange(WINDOW) * temp_step
        + np.random.normal(0, 0.05, WINDOW)
    )

    moisture = (
        start_moisture
        - np.arange(WINDOW) * moisture_step
        + np.random.normal(0, 0.3, WINDOW)
    )

    dataset.append(
        extract_features(temp, moisture) + [2]
    )


# =====================================================
# SAVE DATASET
# =====================================================

columns = [
    "temp_mean",
    "temp_variance",
    "temp_min",
    "temp_max",
    "temp_rate",
    "moisture_mean",
    "moisture_variance",
    "moisture_min",
    "moisture_max",
    "moisture_rate",
    "label"
]

df = pd.DataFrame(dataset, columns=columns)

df.to_csv("../data/tinyml_dataset.csv", index=False)

print("Dataset created!")
print("Shape:", df.shape)
print()
print(df["label"].value_counts())