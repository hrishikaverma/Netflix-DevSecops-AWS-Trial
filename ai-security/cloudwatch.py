import boto3
from datetime import datetime, timedelta, timezone


REGION = "ap-southeast-2"
INSTANCE_ID = "i-0c1aa57f6644d1e58"

session = boto3.Session(
    profile_name="netflix-trial",
    region_name=REGION
)

cloudwatch = session.client("cloudwatch")


def get_metric(metric_name):
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=15)

    response = cloudwatch.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName=metric_name,
        Dimensions=[
            {
                "Name": "InstanceId",
                "Value": INSTANCE_ID
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=["Average"]
    )

    datapoints = response.get("Datapoints", [])

    if not datapoints:
        return 0

    latest = max(datapoints, key=lambda x: x["Timestamp"])

    return latest["Average"]


def get_cloudwatch_metrics():
    return {
        "cpu": get_metric("CPUUtilization"),
        "network_in": get_metric("NetworkIn"),
        "network_out": get_metric("NetworkOut")
    }


if __name__ == "__main__":
    metrics = get_cloudwatch_metrics()
    print(metrics)