"""
Car Finder App - Backend API
Busca autos en todo el mundo: specs técnicas, listings y comparación de precios.
"""

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from routers import search, specs, sources

app = FastAPI(
    title="Car Finder Global",
    description="Buscador global de autos - specs, listings y precios",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router, prefix="/api/search", tags=["search"])
app.include_router(specs.router, prefix="/api/specs", tags=["specs"])
app.include_router(sources.router, prefix="/api/sources", tags=["sources"])


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "Car Finder Global is running"}


# Serve frontend static files
static_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.exists(static_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(static_dir, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        file_path = os.path.join(static_dir, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(static_dir, "index.html"))
