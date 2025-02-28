import time
import requests
from typing import Dict, Any
import os
from .models import ProductData

async def fetch_from_soax_api(link: str) -> ProductData:
    """Fetch data using SOAX API for Amazon links."""
    print("Using SOAX scraping API for Amazon link.")
    api_url = f"https://scraping.soax.com/v1/request?param={link}&function=getProduct&sync=true"
    headers = {"X-SOAX-API-Secret": os.getenv("X_SOAX_API_SECRET")}

    try:
        response = requests.get(api_url, headers=headers, timeout=60)
        response.raise_for_status()
        result = response.json()
        return process_soax_response(result, link)
    except requests.exceptions.RequestException as e:
        print(f"SOAX API error: {e}")
        return ProductData(
            title="Untitled",
            images=[],
            url=link,
            price="N/A"
        )

def process_soax_response(result: Dict[str, Any], link: str) -> ProductData:
    """Process the SOAX API response."""
    if result.get("data", {}).get("status") != "done":
        return ProductData(
            title="Untitled",
            images=[],
            url=link,
            price="N/A"
        )

    product_data = result.get("data", {}).get("value", {})
    extras = product_data.get("extras", {})
    images_small = extras.get("imagesSmall", [])

    # Ensure `images_small` is a list
    if isinstance(images_small, dict):
        images_small = list(images_small.values())

    product_images = [
        url for url in images_small if isinstance(url, str) and url.endswith(".jpg")
    ]
    
    return ProductData(
        title=product_data.get("title", "Untitled"),
        images=product_images,
        price=product_data.get("price", "N/A"),
        url=product_data.get("url", link)
    ) 