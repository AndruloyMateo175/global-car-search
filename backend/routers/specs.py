"""Router de especificaciones técnicas."""

from fastapi import APIRouter, Query
from typing import Optional
from services.carquery_service import get_makes, get_models, get_specs

router = APIRouter()


@router.get("/makes")
async def list_makes():
    """Listar todas las marcas disponibles."""
    makes = await get_makes()
    return {"makes": makes}


@router.get("/models")
async def list_models(
    make: str = Query(..., description="Marca"),
    year: Optional[int] = Query(None),
):
    """Listar modelos de una marca."""
    models = await get_models(make, year)
    return {"models": models}


@router.get("/detail")
async def get_car_specs(
    make: str = Query(...),
    model: str = Query(...),
    year: Optional[int] = Query(None),
):
    """Obtener specs técnicas detalladas."""
    specs = await get_specs(make, model, year)
    return {"specs": specs}
