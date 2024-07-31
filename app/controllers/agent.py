from fastapi import HTTPException
import requests
from config import settings
import json


class AgentController:
    def __init__(self):
        self.issuer = settings.ISSUER_CONFIG
        self.endpoint = settings.AGENT_URL
        self.headers = {"X-API-KEY": settings.SECRET_KEY}

    async def create_did(self):
        endpoint = f"{self.endpoint}/wallet/did/create"
        body = {
            "method": "web",
            "options": {"did": self.issuer["id"], "key_type": "ed25519"},
        }
        requests.post(endpoint, headers=self.headers, json=body)

    def resolve_did(self):
        endpoint = f"{self.endpoint}/resolver/resolve/{self.did}"
        r = requests.get(endpoint, headers=self.headers)
        try:
            return r.json()
        except:
            raise HTTPException(status_code=r.status_code, content={"message": r.text})

    def get_credential(self, credential_id):
        return ""

    def issue_credential(self, credential, options):
        credential["issuer"] = self.issuer

        body = {
            "credential": credential,
            "options": options,
        }

        endpoint = f"{self.endpoint}/vc/credentials/issue"
        r = requests.post(endpoint, headers=self.headers, json=body)
        try:
            return r.json()["verifiableCredential"]
        except:
            raise HTTPException(status_code=r.status_code, content={"message": r.text})

    async def create_credential_offer(self, cred_ref_id, credential, options):
        cred_offer = {
            "auto_issue": True,
            "auto_remove": False,
            # "replacement_id": cred_ref_id,
            "filter": {
                "ld_proof": {
                    "credential": credential,
                    "options": options,
                }
            },
        }
        endpoint = f"{self.endpoint}/issue-credential-2.0/create"
        r = requests.post(endpoint, headers=self.headers, json=cred_offer)
        try:
            return r.json()["cred_ex_id"]
        except:
            raise HTTPException(status_code=r.status_code, content={"message": r.text})

    async def create_oob_invitation(
        self,
        exchange_id,
        handshake=False,
        # present-proof/credential-offer
        exchange_type="credential-offer",
    ):
        invitation = {
            "accept": ["didcomm/aip2;env=rfc19"],
            "attachments": [
                {
                    "id": exchange_id,
                    "type": exchange_type,
                }
            ],
            # "use_did": self.issuer["id"],
            "my_label": self.issuer["name"],
            "handshake_protocols": (
                ["https://didcomm.org/didexchange/1.0"] if handshake else []
            ),
        }
        endpoint = f"{self.endpoint}/out-of-band/create-invitation"
        r = requests.post(endpoint, headers=self.headers, json=invitation)
        try:
            return r.json()["invitation"]
        except:
            raise HTTPException(status_code=r.status_code, content={"message": r.text})

    async def recieve_oob_invitation(
        self,
        oob_invitation,
    ):
        endpoint = f"{self.endpoint}/out-of-band/receive-invitation"
        r = requests.post(endpoint, headers=self.headers, json=oob_invitation)
        try:
            return r.json()
        except:
            raise HTTPException(status_code=r.status_code, content={"message": r.text})
