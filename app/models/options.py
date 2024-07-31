from pydantic import BaseModel, Field


class IssuanceOptions(BaseModel):
    proofType: str = Field("Ed25519Signature2020")
    verificationMethod: str = Field(None)
