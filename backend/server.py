"""
CultGig API — Thin proxy layer
Routes /api/waitlist requests to the Node.js Express backend on port 5000.
All waitlist business logic lives in /app/backend/server/ (Node.js + Mongoose).
"""
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
import httpx
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

app = FastAPI(title="CultGig Proxy", version="1.0.0")
api_router = APIRouter(prefix="/api")

NODE_BACKEND = os.getenv("NODE_BACKEND", "http://localhost:5000")

# ─── Proxy helper ──────────────────────────────────────────────
async def proxy_to_node(method: str, path: str, body: dict = None):
    """Forward request to Node.js backend"""
    url = f"{NODE_BACKEND}{path}"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            if method == "GET":
                resp = await client.get(url)
            elif method == "POST":
                resp = await client.post(url, json=body)
            else:
                resp = await client.request(method, url, json=body)
            return JSONResponse(status_code=resp.status_code, content=resp.json())
    except httpx.ConnectError:
        return JSONResponse(status_code=503, content={"success": False, "message": "Node.js backend unavailable"})
    except Exception as e:
        logging.error(f"Proxy error: {e}")
        return JSONResponse(status_code=500, content={"success": False, "message": "Proxy error"})

# ─── Health checks ─────────────────────────────────────────────
@api_router.get("/")
async def root():
    return {"message": "CultGig API is running", "status": "ok"}

@api_router.get("/health")
async def health():
    return {"status": "healthy", "service": "CultGig API", "version": "1.0.0"}

# ─── Waitlist proxy routes (→ Node.js) ─────────────────────────
@api_router.post("/waitlist")
async def proxy_waitlist_post(request: Request):
    body = await request.json()
    return await proxy_to_node("POST", "/api/waitlist", body)

@api_router.get("/waitlist")
async def proxy_waitlist_get():
    return await proxy_to_node("GET", "/api/waitlist")

@api_router.get("/waitlist/count")
async def proxy_waitlist_count():
    return await proxy_to_node("GET", "/api/waitlist/count")

# ─── Include router & middleware ───────────────────────────────
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
