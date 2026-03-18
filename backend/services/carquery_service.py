"""
CarQuery API Service - Specs técnicas de autos.
API gratuita con specs de miles de modelos.
https://www.carqueryapi.com/
"""

import httpx
from models.car import CarSpec
from typing import Optional


BASE_URL = "https://www.carqueryapi.com/api/0.3/"


async def get_makes() -> list[dict]:
    """Obtener todas las marcas disponibles."""
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(BASE_URL, params={"cmd": "getMakes"})
        data = resp.json()
        return data.get("Makes", [])


async def get_models(make: str, year: Optional[int] = None) -> list[dict]:
    """Obtener modelos de una marca."""
    params = {"cmd": "getModels", "make": make}
    if year:
        params["year"] = year
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(BASE_URL, params=params)
        data = resp.json()
        return data.get("Models", [])


async def get_trims(make: str, model: str, year: Optional[int] = None) -> list[dict]:
    """Obtener trims/versiones de un modelo."""
    params = {"cmd": "getTrims", "make": make, "model": model}
    if year:
        params["year"] = year
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(BASE_URL, params=params)
        data = resp.json()
        return data.get("Trims", [])


async def get_specs(make: str, model: str, year: Optional[int] = None) -> list[CarSpec]:
    """Obtener specs completas de un auto."""
    trims = await get_trims(make, model, year)
    specs = []
    for trim in trims:
        spec = CarSpec(
            make=trim.get("model_make_id", make),
            model=trim.get("model_name", model),
            year=int(trim["model_year"]) if trim.get("model_year") else year,
            trim=trim.get("model_trim", ""),
            body_type=trim.get("model_body", ""),
            engine=trim.get("model_engine_type", ""),
            engine_cc=trim.get("model_engine_cc", ""),
            engine_cylinders=trim.get("model_engine_cyl", ""),
            horsepower=trim.get("model_engine_power_ps", ""),
            torque=trim.get("model_engine_torque_nm", ""),
            transmission=trim.get("model_transmission_type", ""),
            drive_type=trim.get("model_drive", ""),
            fuel_type=trim.get("model_engine_fuel", ""),
            doors=trim.get("model_doors", ""),
            seats=trim.get("model_seats", ""),
            weight_kg=trim.get("model_weight_kg", ""),
            top_speed_kph=trim.get("model_top_speed_kph", ""),
            acceleration_0_100=trim.get("model_0_to_100_kph", ""),
        )
        specs.append(spec)
    return specs
