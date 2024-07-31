from fastapi import APIRouter, Security
from fastapi.responses import JSONResponse
from app.controllers.agent import AgentController
from app.auth import get_api_key
from config import settings

router = APIRouter()


@router.post(
    "/lob/{lob_id}/credentials/{credential_type}", summary="Map DB Object to Credential"
)
async def map_credential(
    lob_id: str, credential_type: str, apiKey: str = Security(get_api_key)
):
    return JSONResponse(status_code=200, content={})
