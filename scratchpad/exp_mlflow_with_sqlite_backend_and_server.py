import os
from random import randint, random
from config import Settings
import mlflow
from mlflow import log_artifacts, log_metric, log_param

settings = Settings()

mlflow.set_tracking_uri(settings.mlflow_database_uri)
mlflow.set_experiment("random_data_for_mlflow_experiment")


if __name__ == "__main__":
    print("Running mlflow_tracking.py")

    log_param("param1", randint(0, 100))

    log_metric("foo", random())
    log_metric("foo", random() + 1)
    log_metric("foo", random() + 2)

    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    with open("outputs/test.txt", "w") as f:
        f.write("hello world!")

    log_artifacts("outputs")
