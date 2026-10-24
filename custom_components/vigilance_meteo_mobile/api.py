import asyncio
from .const import API_URL

class InvalidAuth(Exception):
    """L'accès Météo-France a été refusé."""

def extract_product(data):
    if not isinstance(data, dict):
        raise ValueError("Réponse JSON non reconnue")
    product = data.get("product")
    if product is None and isinstance(data.get("content"), dict):
        product = data["content"].get("product")
    if not isinstance(product, dict) or not isinstance(product.get("periods"), list):
        raise ValueError("Structure product/periods absente")
    return product

async def async_fetch(session, key):
    async with asyncio.timeout(30):
        async with session.get(API_URL, headers={"accept": "application/json", "apikey": key}) as response:
            if response.status in (401, 403):
                raise InvalidAuth("Clé ou accès API refusé")
            response.raise_for_status()
            return extract_product(await response.json())
