from fastapi import FastAPI
from pydantic import BaseModel
from predict import predict_risk

app = FastAPI(
    title="Netflix DevSecOps AI Risk Prediction",
    description="AI-based security risk prediction using security scan and AWS CloudWatch metrics",
    version="1.0.0"
)


class SecurityMetrics(BaseModel):
    critical: int
    high: int
    medium: int
    low: int
    sonar_bugs: int
    code_smells: int
    coverage: float


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
def predict(metrics: SecurityMetrics):

    result = predict_risk(
        critical=metrics.critical,
        high=metrics.high,
        medium=metrics.medium,
        low=metrics.low,
        sonar_bugs=metrics.sonar_bugs,
        code_smells=metrics.code_smells,
        coverage=metrics.coverage
    )

    return result