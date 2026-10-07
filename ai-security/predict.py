
import joblib
import pandas as pd
from cloudwatch import get_cloudwatch_metrics


# Load trained model
model = joblib.load("risk_model.pkl")


def predict_risk(
    critical,
    high,
    medium,
    low,
    sonar_bugs,
    code_smells,
    coverage
):
    # Get latest AWS CloudWatch metrics
    cloud_metrics = get_cloudwatch_metrics()

    cpu = cloud_metrics["cpu"]
    network_in = cloud_metrics["network_in"]
    network_out = cloud_metrics["network_out"]

    # Prepare input for ML model
    features = pd.DataFrame([{
        "critical": critical,
        "high": high,
        "medium": medium,
        "low": low,
        "sonar_bugs": sonar_bugs,
        "code_smells": code_smells,
        "coverage": coverage,
        "cpu": cpu,
        "network_in": network_in,
        "network_out": network_out
    }])

    # Predict risk
    prediction = model.predict(features)[0]

    return {
        "risk": prediction,
        "cloudwatch": cloud_metrics
    }


if __name__ == "__main__":

    # Example security scan metrics
    result = predict_risk(
        critical=0,
        high=3,
        medium=8,
        low=20,
        sonar_bugs=5,
        code_smells=35,
        coverage=70
    )

    print("AI Risk Prediction:")
    print(result)
