"""Router de fuentes de datos."""

from fastapi import APIRouter
from services.listing_sources import get_all_sources

router = APIRouter()


@router.get("/")
async def list_sources():
    """Listar todas las fuentes de listings disponibles."""
    sources = get_all_sources()
    return {
        "total": len(sources),
        "sources": [
            {
                "name": s.name,
                "country": s.country,
                "country_code": s.country_code,
                "base_url": s.base_url,
            }
            for s in sources
        ],
    }
