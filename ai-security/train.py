import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib


# Training data
data = [
    # critical, high, medium, low, sonar_bugs, code_smells, coverage, cpu, network_in, network_out, risk
    [0, 0, 2, 10, 0, 10, 85, 20, 10000, 10000, "LOW"],
    [0, 1, 3, 12, 1, 15, 80, 25, 12000, 15000, "LOW"],
    [0, 2, 5, 15, 2, 20, 75, 30, 15000, 18000, "MEDIUM"],
    [0, 3, 8, 20, 5, 35, 70, 40, 20000, 25000, "MEDIUM"],
    [1, 3, 8, 20, 5, 35, 65, 50, 30000, 35000, "HIGH"],
    [1, 5, 10, 25, 8, 45, 60, 60, 40000, 50000, "HIGH"],
    [2, 6, 12, 30, 10, 50, 55, 70, 50000, 60000, "HIGH"],
    [3, 8, 15, 40, 15, 70, 40, 80, 70000, 80000, "CRITICAL"],
    [5, 10, 20, 50, 20, 100, 30, 90, 90000, 100000, "CRITICAL"],
    [0, 0, 1, 5, 0, 5, 95, 10, 5000, 5000, "LOW"],
    [0, 1, 4, 10, 1, 12, 85, 35, 18000, 20000, "MEDIUM"],
    [2, 4, 10, 25, 7, 40, 55, 65, 45000, 55000, "HIGH"],
    [4, 9, 18, 45, 18, 90, 35, 95, 100000, 120000, "CRITICAL"],
]


columns = [
    "critical",
    "high",
    "medium",
    "low",
    "sonar_bugs",
    "code_smells",
    "coverage",
    "cpu",
    "network_in",
    "network_out",
    "risk"
]

df = pd.DataFrame(data, columns=columns)


# Features and target
X = df.drop("risk", axis=1)
y = df["risk"]


# Train Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)


# Save trained model
joblib.dump(model, "risk_model.pkl")

print("Model training completed successfully.")
print("Model saved as risk_model.pkl")
print("Risk classes:", model.classes_)