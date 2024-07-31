from pydantic import BaseModel, Field
from datetime import datetime
import uuid

EXAMPLE_CREDENTIAL = {
    "@context": [
        "https://www.w3.org/2018/credentials/v1",
        "https://www.w3.org/ns/credentials/examples/v2",
        {"@vocab": "urn:vocab#"},
    ],
    "type": ["ExampleCredential", "VerifiableCredential"],
    "validFrom": str(datetime.now().isoformat()),
    "validUntil": str(datetime.now().isoformat()),
    "credentialSubject": {
        "issuedTo": {"name": "Open Security and Identity", "identifier": "OpSecId"}
    },
}

EXAMPLE_ISSUANCE_OPTIONS = {"proofType": "Ed25519Signature2020"}


class SendCredentialOffer(BaseModel):
    credential: dict = Field(example=EXAMPLE_CREDENTIAL)
    options: dict = Field(example=EXAMPLE_ISSUANCE_OPTIONS)
