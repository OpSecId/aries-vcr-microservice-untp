from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from app.routers import mappings, credentials
from config import settings


app = FastAPI(
    title=settings.PROJECT_TITLE,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
    contact=settings.PROJECT_CONTACT,
    # license_info=settings.PROJECT_LICENSE_INFO,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter()

# api_router.include_router(mappings.router, tags=["Mappings"])
api_router.include_router(credentials.router, tags=["Credentials"])


@api_router.get(
    "/.well-known/did.json", response_class=HTMLResponse, include_in_schema=False
)
async def did_doc():
    did = settings.ISSUER_CONFIG["id"]
    did_document = {
        "@context": [
            "https://www.w3.org/ns/did/v1",
            "https://w3id.org/security/suites/ed25519-2020/v1",
        ],
        "id": did,
        "verificationMethod": [
            {
                "type": "Ed25519VerificationKey2020",
                "id": f"{did}#verkey",
                "controller": did,
                "publicKeyMultibase": settings.DID_KEY.split(":")[-1],
            }
        ],
        "authentication": [f"{did}#verkey"],
        "assertionMethod": [f"{did}#verkey"],
        "service": [
            {
                "type": "did-communication",
                "id": f"{did}#didcomm",
                "serviceEndpoint": settings.DIDCOMM_URL,
            }
        ],
    }
    return JSONResponse(status_code=200, content=did_document)


@api_router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url="/docs")


@api_router.get(
    "/server/status", tags=["Server"], summary="Status check", include_in_schema=False
)
async def status_check():
    return JSONResponse(status_code=200, content={"status": "ok"})


app.include_router(api_router)
