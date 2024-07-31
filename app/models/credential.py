from pydantic import BaseModel, Field
from typing import List

VCDM_V1_CONTEXT = ""


class IssuerField(BaseModel):
    type: List[str] = Field(None)
    id: str = Field(None)
    name: str = Field(None)
    description: str = Field(None)


class CredentialStatusEntry(BaseModel):
    type: str = Field("BitstringStatusListEntry")
    id: str = Field(None)
    statusIndex: str = Field(None)
    statusPurpose: str = Field("revocation")
    statusCredential: str = Field(None)


class CredentialBase(BaseModel):
    context: List[str] = Field([VCDM_V1_CONTEXT], alias="@context")
    type: List[str] = Field(["VerifiableCredential"])
    issuer: IssuerField = Field(None)
    credentialSubject: dict = Field(None)
    credentialStatus: dict = Field(None)
