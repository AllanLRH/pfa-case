import pydantic


class Settings(pydantic.BaseSettings):
    mlflow_server_port: str
    mlflow_ui_port: str
    mlflow_database_uri: str

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
