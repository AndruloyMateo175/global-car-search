"""Router de búsqueda principal."""

from fastapi import APIRouter, Query
from typing import Optional
from models.car import SearchResult
from services.carquery_service import get_specs
from services.listing_sources import search_all_sources, get_price_comparison
import asyncio

router = APIRouter()


@router.get("/", response_model=SearchResult)
async def search_cars(
    make: str = Query(..., description="Marca del auto (ej: BMW, Toyota)"),
    model: str = Query(..., description="Modelo del auto (ej: 220i, Corolla)"),
    year: Optional[int] = Query(None, description="Año del modelo"),
):
    """Búsqueda global de autos: specs + listings + precios."""
    # Ejecutar specs y listings en paralelo
    specs_task = get_specs(make, model, year)
    listings_task = search_all_sources(make, model, year)

    specs, listings = await asyncio.gather(specs_task, listings_task)
    price_comparison = get_price_comparison(listings)

    # Obtener fuentes únicas
    sources_searched = list(set(l.source.split(" (")[0] for l in listings))

    return SearchResult(
        query=f"{make} {model} {year or ''}".strip(),
        specs=specs,
        listings=listings,
        price_comparison=price_comparison,
        sources_searched=sorted(sources_searched),
        total_listings=len(listings),
    )
