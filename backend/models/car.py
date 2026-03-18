"""Modelos de datos para autos."""

from pydantic import BaseModel
from typing import Optional


class CarSpec(BaseModel):
    make: str
    model: str
    year: Optional[int] = None
    trim: Optional[str] = None
    body_type: Optional[str] = None
    engine: Optional[str] = None
    engine_cc: Optional[str] = None
    engine_cylinders: Optional[str] = None
    horsepower: Optional[str] = None
    torque: Optional[str] = None
    transmission: Optional[str] = None
    drive_type: Optional[str] = None
    fuel_type: Optional[str] = None
    doors: Optional[str] = None
    seats: Optional[str] = None
    weight_kg: Optional[str] = None
    top_speed_kph: Optional[str] = None
    acceleration_0_100: Optional[str] = None


class CarListing(BaseModel):
    title: str
    price: Optional[str] = None
    price_usd: Optional[float] = None
    currency: Optional[str] = None
    location: Optional[str] = None
    country: str
    country_code: str
    year: Optional[int] = None
    mileage: Optional[str] = None
    url: str
    image_url: Optional[str] = None
    source: str
    description: Optional[str] = None


class PriceComparison(BaseModel):
    country: str
    country_code: str
    avg_price_usd: Optional[float] = None
    min_price_usd: Optional[float] = None
    max_price_usd: Optional[float] = None
    listing_count: int = 0
    currency: str = "USD"
    source: str = ""


class SearchResult(BaseModel):
    query: str
    specs: list[CarSpec] = []
    listings: list[CarListing] = []
    price_comparison: list[PriceComparison] = []
    sources_searched: list[str] = []
    total_listings: int = 0
