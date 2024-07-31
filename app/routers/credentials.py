from fastapi import APIRouter, Security, HTTPException
from fastapi.responses import JSONResponse
from app.controllers.agent import AgentController
from app.auth import get_api_key
from app.models.web_requests import SendCredentialOffer
from config import settings
from datetime import datetime
import uuid

router = APIRouter()


@router.get("/entity/{entity_id}/credentials/{credential_id}", summary="Get Credential")
async def get_credential(entity_id: str, credential_id: str):

    credential_id = (
        f"https://{settings.DOMAIN}/entity/{entity_id}/credentials/{credential_id}"
    )

    vc = AgentController().get_credential(credential_id)

    return JSONResponse(status_code=200, content=vc)


@router.post("/credential-offer", summary="Send Credential Offer")
async def send_credential_offer(
    request_body: SendCredentialOffer, apiKey: str = Security(get_api_key)
):

    credential = vars(request_body)["credential"]
    options = vars(request_body)["options"]

    credential["issuer"] = settings.ISSUER_CONFIG
    if credential["@context"][0] == "https://www.w3.org/2018/credentials/v1":
        credential["issuanceDate"] = str(datetime.now().isoformat())

    entity_id = credential["credentialSubject"]["issuedTo"]["identifier"]
    cred_ref_id = str(uuid.uuid4())
    credential["id"] = (
        f"https://{settings.DOMAIN}/entity/{entity_id}/credentials/{cred_ref_id}"
    )
    cred_ex_id = await AgentController().create_credential_offer(
        cred_ref_id, credential, options
    )
    oob_invitation = await AgentController().create_oob_invitation(
        cred_ex_id, handshake=True
    )
    # oob_invitation_response = await AgentController().recieve_oob_invitation(oob_invitation)

    return JSONResponse(status_code=201, content=oob_invitation)
