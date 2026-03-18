"""
Listing Sources Manager
Framework para buscar autos en venta en múltiples fuentes/países.

Cada fuente implementa la interfaz base y se registra automáticamente.
Para agregar una nueva fuente, crear una clase que herede de ListingSource.
"""

import httpx
from abc import ABC, abstractmethod
from models.car import CarListing, PriceComparison
from typing import Optional
import asyncio
from bs4 import BeautifulSoup
import re


class ListingSource(ABC):
    """Interfaz base para fuentes de listings."""

    name: str = "Unknown"
    country: str = "Unknown"
    country_code: str = "XX"
    base_url: str = ""

    @abstractmethod
    async def search(self, make: str, model: str, year: Optional[int] = None) -> list[CarListing]:
        pass

    def build_search_url(self, make: str, model: str, year: Optional[int] = None) -> str:
        return self.base_url


# ---- Registry ----
_sources: list[ListingSource] = []


def register_source(source: ListingSource):
    _sources.append(source)


def get_all_sources() -> list[ListingSource]:
    return _sources


# ========================================
# FUENTES DE LISTINGS
# ========================================


class AutoScout24Source(ListingSource):
    """AutoScout24 - Europa (Alemania, Italia, Francia, España, etc.)"""

    name = "AutoScout24"
    country = "Europe"
    country_code = "EU"
    base_url = "https://www.autoscout24.com"

    async def search(self, make: str, model: str, year: Optional[int] = None) -> list[CarListing]:
        listings = []
        search_url = f"{self.base_url}/lst/{make.lower()}/{model.lower().replace(' ', '-')}"
        params = {}
        if year:
            params["fregfrom"] = year
            params["fregto"] = year

        try:
            async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
                headers = {"User-Agent": "Mozilla/5.0 (compatible; CarFinder/1.0)"}
                resp = await client.get(search_url, params=params, headers=headers)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "lxml")
                    articles = soup.select("article")[:10]
                    for article in articles:
                        title_el = article.select_one("h2, [data-testid='title']")
                        price_el = article.select_one("[data-testid='price'], .Price")
                        link_el = article.select_one("a[href]")

                        title = title_el.get_text(strip=True) if title_el else f"{make} {model}"
                        price = price_el.get_text(strip=True) if price_el else None
                        url = link_el["href"] if link_el and link_el.get("href") else search_url
                        if url.startswith("/"):
                            url = self.base_url + url

                        listings.append(CarListing(
                            title=title,
                            price=price,
                            price_usd=self._parse_eur_to_usd(price),
                            currency="EUR",
                            country="Europe",
                            country_code="EU",
                            year=year,
                            url=url,
                            source=self.name,
                        ))
        except Exception:
            # Si falla scraping, devolver link directo a búsqueda
            listings.append(CarListing(
                title=f"{make} {model} {year or ''}".strip(),
                price=None,
                country="Europe",
                country_code="EU",
                year=year,
                url=f"{self.base_url}/lst/{make.lower()}/{model.lower().replace(' ', '-')}",
                source=f"{self.name} (link directo)",
            ))
        return listings

    @staticmethod
    def _parse_eur_to_usd(price_str: Optional[str]) -> Optional[float]:
        if not price_str:
            return None
        numbers = re.findall(r"[\d.,]+", price_str.replace(".", "").replace(",", "."))
        if numbers:
            try:
                return round(float(numbers[0]) * 1.08, 2)  # EUR->USD approx
            except ValueError:
                return None
        return None


class MobileDeSource(ListingSource):
    """Mobile.de - Alemania (mayor mercado de autos de Europa)"""

    name = "Mobile.de"
    country = "Germany"
    country_code = "DE"
    base_url = "https://suchen.mobile.de"

    async def search(self, make: str, model: str, year: Optional[int] = None) -> list[CarListing]:
        search_url = f"https://www.mobile.de/es/coche/{make.lower()}-{model.lower().replace(' ', '-')}"
        return [CarListing(
            title=f"{make} {model} {year or ''}".strip(),
            price=None,
            country="Germany",
            country_code="DE",
            year=year,
            url=search_url,
            source=f"{self.name} (link directo)",
        )]


class CarsComSource(ListingSource):
    """Cars.com - Estados Unidos"""

    name = "Cars.com"
    country = "United States"
    country_code = "US"
    base_url = "https://www.cars.com"

    async def search(self, make: str, model: str, year: Optional[int] = None) -> list[CarListing]:
        slug = f"{make}-{model}".lower().replace(" ", "_")
        year_str = str(year) if year else ""
        search_url = f"{self.base_url}/shopping/results/?stock_type=all&makes[]={make.lower()}&models[]={make.lower()}-{model.lower().replace(' ', '_')}"
        if year:
            search_url += f"&year_min={year}&year_max={year}"

        return [CarListing(
            title=f"{make} {model} {year or ''}".strip(),
            price=None,
            country="United States",
            country_code="US",
            year=year,
            url=search_url,
            source=f"{self.name} (link directo)",
        )]


class AutoTraderUKSource(ListingSource):
    """AutoTrader UK - Reino Unido"""

    name = "AutoTrader UK"
    country = "United Kingdom"
    country_code = "GB"
    base_url = "https://www.autotrader.co.uk"

    async def search(self, make: str, model: str, year: Optional[int] = None) -> list[CarListing]:
        search_url = f"{self.base_url}/car-search?make={make}&model={model}"
        if year:
            search_url += f"&year-from={year}&year-to={year}"
        return [CarListing(
            title=f"{make} {model} {year or ''}".strip(),
            price=None,
            country="United Kingdom",
            country_code="GB",
            currency="GBP",
            year=year,
            url=search_url,
            source=f"{self.name} (link directo)",
        )]


class MercadoLibreSource(ListingSource):
    """MercadoLibre - Latinoamérica (Argentina, México, Uruguay, etc.)"""

    name = "MercadoLibre"
    country = "Latin America"
    country_code = "LATAM"
    base_url = "https://autos.mercadolibre.com.ar"

    COUNTRY_URLS = {
        "AR": "https://autos.mercadolibre.com.ar",
        "MX": "https://autos.mercadolibre.com.mx",
        "UY": "https://autos.mercadolibre.com.uy",
        "CO": "https://autos.mercadolibre.com.co",
        "CL": "https://autos.mercadolibre.cl",
        "BR": "https://www.mercadolivre.com.br/veiculos",
        "PE": "https://autos.mercadolibre.com.pe",
        "EC": "https://autos.mercadolibre.com.ec",
    }

    async def search(self, make: str, model: str, year: Optional[int] = None) -> list[CarListing]:
        listings = []
        query = f"{make} {model}"
        if year:
            query += f" {year}"

        for code, base in self.COUNTRY_URLS.items():
            country_name = {
                "AR": "Argentina", "MX": "México", "UY": "Uruguay",
                "CO": "Colombia", "CL": "Chile", "BR": "Brasil",
                "PE": "Perú", "EC": "Ecuador"
            }.get(code, code)

            search_term = query.replace(" ", "-")
            search_url = f"{base}/{search_term}"

            listings.append(CarListing(
                title=f"{make} {model} {year or ''} - {country_name}".strip(),
                price=None,
                country=country_name,
                country_code=code,
                year=year,
                url=search_url,
                source=f"MercadoLibre {country_name}",
            ))
        return listings


class CarGurusSource(ListingSource):
    """CarGurus - US, Canada, UK"""

    name = "CarGurus"
    country = "US/Canada/UK"
    country_code = "US"
    base_url = "https://www.cargurus.com"

    async def search(self, make: str, model: str, year: Optional[int] = None) -> list[CarListing]:
        search_url = f"{self.base_url}/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?searchChanged=true&makeNames={make}&modelNames={model}"
        if year:
            search_url += f"&startYear={year}&endYear={year}"
        return [CarListing(
            title=f"{make} {model} {year or ''}".strip(),
            price=None,
            country="United States",
            country_code="US",
            year=year,
            url=search_url,
            source=f"{self.name} (link directo)",
        )]


class CopartSource(ListingSource):
    """Copart - Subastas de autos (global)"""

    name = "Copart"
    country = "Global (Auctions)"
    country_code = "GLOBAL"
    base_url = "https://www.copart.com"

    async def search(self, make: str, model: str, year: Optional[int] = None) -> list[CarListing]:
        query = f"{make}+{model}"
        if year:
            query += f"+{year}"
        search_url = f"{self.base_url}/lotSearchResults/?free=true&query={query}"
        return [CarListing(
            title=f"{make} {model} {year or ''} (Subasta)".strip(),
            price=None,
            country="Global",
            country_code="GLOBAL",
            year=year,
            url=search_url,
            source=f"{self.name} (subastas)",
        )]


class JapanUsedCarsSource(ListingSource):
    """BE FORWARD / Japan Used Cars - Japón (export global)"""

    name = "BE FORWARD"
    country = "Japan"
    country_code = "JP"
    base_url = "https://www.beforward.jp"

    async def search(self, make: str, model: str, year: Optional[int] = None) -> list[CarListing]:
        search_url = f"{self.base_url}/stocklist/make/{make}/model/{model}"
        if year:
            search_url += f"/year_from/{year}/year_to/{year}"
        return [CarListing(
            title=f"{make} {model} {year or ''} (Japan Export)".strip(),
            price=None,
            country="Japan",
            country_code="JP",
            currency="JPY",
            year=year,
            url=search_url,
            source=f"{self.name} (link directo)",
        )]


class CarsCoZaSource(ListingSource):
    """Cars.co.za - Sudáfrica"""

    name = "Cars.co.za"
    country = "South Africa"
    country_code = "ZA"
    base_url = "https://www.cars.co.za"

    async def search(self, make: str, model: str, year: Optional[int] = None) -> list[CarListing]:
        search_url = f"{self.base_url}/usedcars/{make}/{model}/"
        if year:
            search_url += f"?year_from={year}&year_to={year}"
        return [CarListing(
            title=f"{make} {model} {year or ''}".strip(),
            price=None,
            country="South Africa",
            country_code="ZA",
            currency="ZAR",
            year=year,
            url=search_url,
            source=f"{self.name} (link directo)",
        )]


class CarSaleAUSource(ListingSource):
    """CarSales - Australia"""

    name = "CarSales"
    country = "Australia"
    country_code = "AU"
    base_url = "https://www.carsales.com.au"

    async def search(self, make: str, model: str, year: Optional[int] = None) -> list[CarListing]:
        search_url = f"{self.base_url}/cars/{make.lower()}/{model.lower().replace(' ', '-')}/"
        if year:
            search_url += f"?year={year}"
        return [CarListing(
            title=f"{make} {model} {year or ''}".strip(),
            price=None,
            country="Australia",
            country_code="AU",
            currency="AUD",
            year=year,
            url=search_url,
            source=f"{self.name} (link directo)",
        )]


class OtomotoSource(ListingSource):
    """OTOMOTO - Polonia"""

    name = "OTOMOTO"
    country = "Poland"
    country_code = "PL"
    base_url = "https://www.otomoto.pl"

    async def search(self, make: str, model: str, year: Optional[int] = None) -> list[CarListing]:
        search_url = f"{self.base_url}/osobowe/{make.lower()}/{model.lower().replace(' ', '-')}/"
        if year:
            search_url += f"?search%5Bfilter_float_year%3Afrom%5D={year}&search%5Bfilter_float_year%3Ato%5D={year}"
        return [CarListing(
            title=f"{make} {model} {year or ''}".strip(),
            price=None,
            country="Poland",
            country_code="PL",
            currency="PLN",
            year=year,
            url=search_url,
            source=f"{self.name} (link directo)",
        )]


class DubaiCarsSource(ListingSource):
    """Dubizzle/DubaiCars - Emiratos Árabes"""

    name = "Dubizzle"
    country = "UAE"
    country_code = "AE"
    base_url = "https://www.dubizzle.com"

    async def search(self, make: str, model: str, year: Optional[int] = None) -> list[CarListing]:
        search_url = f"{self.base_url}/motors/used-cars/{make.lower()}/{model.lower().replace(' ', '-')}/"
        if year:
            search_url += f"?year__gte={year}&year__lte={year}"
        return [CarListing(
            title=f"{make} {model} {year or ''}".strip(),
            price=None,
            country="UAE",
            country_code="AE",
            currency="AED",
            year=year,
            url=search_url,
            source=f"{self.name} (link directo)",
        )]


# ---- Registrar todas las fuentes ----
register_source(AutoScout24Source())
register_source(MobileDeSource())
register_source(CarsComSource())
register_source(AutoTraderUKSource())
register_source(MercadoLibreSource())
register_source(CarGurusSource())
register_source(CopartSource())
register_source(JapanUsedCarsSource())
register_source(CarsCoZaSource())
register_source(CarSaleAUSource())
register_source(OtomotoSource())
register_source(DubaiCarsSource())


# ---- Búsqueda en todas las fuentes ----
async def search_all_sources(make: str, model: str, year: Optional[int] = None) -> list[CarListing]:
    """Buscar en todas las fuentes registradas en paralelo."""
    tasks = [source.search(make, model, year) for source in _sources]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    all_listings = []
    for result in results:
        if isinstance(result, list):
            all_listings.extend(result)
    return all_listings


def get_price_comparison(listings: list[CarListing]) -> list[PriceComparison]:
    """Generar comparación de precios por país."""
    country_data: dict[str, list[float]] = {}
    country_sources: dict[str, str] = {}

    for listing in listings:
        if listing.price_usd and listing.price_usd > 0:
            key = listing.country
            if key not in country_data:
                country_data[key] = []
                country_sources[key] = listing.source
            country_data[key].append(listing.price_usd)

    comparisons = []
    for country, prices in country_data.items():
        comparisons.append(PriceComparison(
            country=country,
            country_code=next(
                (l.country_code for l in listings if l.country == country), "XX"
            ),
            avg_price_usd=round(sum(prices) / len(prices), 2),
            min_price_usd=round(min(prices), 2),
            max_price_usd=round(max(prices), 2),
            listing_count=len(prices),
            source=country_sources.get(country, ""),
        ))

    return sorted(comparisons, key=lambda x: x.avg_price_usd or 0)
