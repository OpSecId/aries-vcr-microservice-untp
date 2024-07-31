from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Settings(BaseSettings):
    PROJECT_TITLE: str = "Aries VCR UNTP Microservice"
    PROJECT_VERSION: str = "v0.0.1"
    PROJECT_DESCRIPTION: str = """
    Aries VCR UNTP Microservice
    """
    PROJECT_CONTACT: dict = {
        "name": "Open Security and Identity",
        "url": "https://opsecid.ca",
    }
    # PROJECT_LICENSE_INFO = {
    #     "name": "",
    #     "url": ""
    # }

    SECRET_KEY: str = os.environ["SECRET_KEY"]
    AGENT_URL: str = os.environ["AGENT_URL"]
    DIDCOMM_URL: str = os.environ["DIDCOMM_URL"]

    DOMAIN: str = os.environ["DOMAIN"]
    DID_WEB: str = os.environ["DID_WEB"]
    DID_KEY: str = os.environ["DID_KEY"]

    ISSUER_CONFIG: dict = {
        "id": DID_WEB,
        "name": os.environ["ISSUER_NAME"],
    }


settings = Settings()
