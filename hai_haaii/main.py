import os
import logging
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel, field_validator, conlist
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("hai_haaii")

OPENAI_BASE_URL: str  = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
OPENAI_API_KEY: str   = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL: str     = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")
INTERNAL_API_KEY: str = os.environ.get("HAI_INTERNAL_API_KEY", "")
ALLOWED_MODELS: set[str] = {m.strip() for m in os.environ.get("HAI_ALLOWED_MODELS", "").split(",") if m.strip()}

MAX_MESSAGES  = 50
MAX_CONTENT   = 8192
ALLOWED_ROLES = {"system", "user", "assistant"}

limiter = Limiter(key_func=get_remote_address)

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY is not set - chat requests will be rejected.")
    if INTERNAL_API_KEY:
        logger.info("Internal API key authentication ENABLED.")
    else:
        logger.warning("HAI_INTERNAL_API_KEY not set - endpoint is unauthenticated.")
    yield

app = FastAPI(
    title="hAI.HAAiI", version="0.2.0", lifespan=lifespan,
    docs_url=None, redoc_url=None, openapi_url=None,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

_allowed_hosts = [h.strip() for h in os.environ.get("HAI_ALLOWED_HOSTS", "localhost,127.0.0.1,homeassistant").split(",") if h.strip()]
app.add_middleware(TrustedHostMiddleware, allowed_hosts=_allowed_hosts)

def verify_internal_key(request: Request):
    if not INTERNAL_API_KEY:
        return
    if request.headers.get("X-HAI-API-Key", "") != INTERNAL_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

class ChatMessage(BaseModel):
    role: str
    content: str

    @field_validator("role")
    @classmethod
    def validate_role(cls, v):
        if v not in ALLOWED_ROLES:
            raise ValueError(f"Invalid role. Allowed: {ALLOWED_ROLES}")
        return v

    @field_validator("content")
    @classmethod
    def validate_content(cls, v):
        if len(v) > MAX_CONTENT:
            raise ValueError(f"Content exceeds {MAX_CONTENT} chars.")
        return v

class ChatRequest(BaseModel):
    messages: conlist(ChatMessage, min_length=1, max_length=MAX_MESSAGES)
    model: str | None = None

    @field_validator("model")
    @classmethod
    def validate_model(cls, v):
        if v and ALLOWED_MODELS and v not in ALLOWED_MODELS:
            raise ValueError("Model not in allowed list.")
        return v

@app.post("/v1/chat/completions")
@limiter.limit("20/minute")
async def chat_completions(request: Request, payload: ChatRequest, _: None = Depends(verify_internal_key)):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=503, detail="OPENAI_API_KEY not configured")
    model = payload.model or OPENAI_MODEL
    if ALLOWED_MODELS and model not in ALLOWED_MODELS:
        raise HTTPException(status_code=400, detail="Model not allowed.")
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "User-Agent": "hAI.HAAiI/0.2.0"}
    data = {"model": model, "messages": [m.model_dump() for m in payload.messages], "stream": False}
    try:
        async with httpx.AsyncClient(
            base_url=OPENAI_BASE_URL,
            timeout=httpx.Timeout(connect=5.0, read=60.0, write=10.0, pool=5.0),
            follow_redirects=False,
        ) as client:
            r = await client.post("/chat/completions", json=data, headers=headers)
            r.raise_for_status()
            return r.json()
    except httpx.HTTPStatusError as exc:
        logger.error("Upstream %s: %.256s", exc.response.status_code, exc.response.text)
        raise HTTPException(status_code=exc.response.status_code, detail="Upstream API error")
    except httpx.RequestError as exc:
        logger.error("Request error: %s", exc)
        raise HTTPException(status_code=502, detail="Could not reach upstream API")

@app.get("/health")
async def health():
    return {"name": "hAI.HAAiI", "status": "ok", "version": "0.2.0"}

@app.get("/")
async def root():
    return {"name": "hAI.HAAiI", "docs": "disabled in production"}
